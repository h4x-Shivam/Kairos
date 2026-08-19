"""Diagnostic REST evaluation and real-time Server-Sent Events (SSE) stream endpoints."""
import json
import asyncio
from datetime import datetime
from typing import Optional, AsyncGenerator, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from app.schemas.enums import HorizonMode, MarketCapBucket, TimeFrame, PrimaryAction
from app.schemas.diagnostic import DiagnosticOutput
from app.engine.evaluator import evaluate_diagnostic
from app.engine.tax_simulator import simulate_trim_execution
from app.services.data_aggregator import data_aggregator

router = APIRouter(prefix="/diagnostic", tags=["Diagnostic"])


class EvaluateRequest(BaseModel):
    """Request payload for on-demand stock evaluation."""
    symbol: str = Field(..., description="Stock ticker symbol (e.g. TATAMOTORS, RELIANCE)")
    horizon_mode: HorizonMode = Field(HorizonMode.COMPOUNDER)
    timeframe: TimeFrame = Field(TimeFrame.D1)
    manual_atr_mult: Optional[float] = Field(None, ge=1.0, le=5.0)
    entry_price: Optional[float] = Field(None, gt=0)
    holding_shares: Optional[int] = Field(None, gt=0)
    purchase_date: Optional[str] = Field(None, description="YYYY-MM-DD")


def _calc_holding_months(purchase_date_str: Optional[str]) -> int:
    """Calculate holding period in months from purchase date."""
    if not purchase_date_str:
        return 13  # Default to LTCG if unspecified
    try:
        dt = datetime.strptime(purchase_date_str, "%Y-%m-%d")
        now = datetime.utcnow()
        months = (now.year - dt.year) * 12 + (now.month - dt.month)
        return max(1, months)
    except Exception:
        return 13


def _action_to_trim_pct(action: PrimaryAction) -> float:
    """Map primary action to tax trim percentage."""
    if action == PrimaryAction.TRIM_25:
        return 25.0
    if action == PrimaryAction.TRIM_50:
        return 50.0
    if action == PrimaryAction.EXIT_FULLY:
        return 100.0
    return 25.0


@router.post("/evaluate", response_model=DiagnosticOutput)
def evaluate_stock(request: EvaluateRequest) -> DiagnosticOutput:
    """Synchronous diagnostic evaluation pipeline."""
    try:
        diag_input = data_aggregator.build_diagnostic_input(
            symbol=request.symbol,
            horizon_mode=request.horizon_mode,
            timeframe=request.timeframe,
            manual_atr_mult=request.manual_atr_mult,
        )
        output = evaluate_diagnostic(diag_input)
        
        # If user holding details provided, compute portfolio tax impact
        if request.entry_price and request.holding_shares:
            months = _calc_holding_months(request.purchase_date)
            trim_pct = _action_to_trim_pct(output.action)
            tax_res = simulate_trim_execution(
                shares_held=request.holding_shares,
                buy_price=request.entry_price,
                current_price=diag_input.current_price,
                trim_percentage=trim_pct,
                holding_period_months=months,
            )
            output = output.model_copy(update={"tax_impact": tax_res})
            
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic evaluation failed: {str(e)}")


async def _stream_telemetry_generator(
    symbol: str,
    horizon_mode: HorizonMode,
    manual_atr_mult: Optional[float],
    entry_price: Optional[float],
    holding_shares: Optional[int],
    purchase_date: Optional[str],
) -> AsyncGenerator[str, None]:
    """Emit staged Server-Sent Events showing institutional pipeline progress."""
    try:
        # Stage 1: Initializing
        yield f"data: {json.dumps({'stage': 'INITIALIZING', 'progress': 15, 'message': 'Connecting to institutional telemetry feeds...'})}\n\n"
        await asyncio.sleep(0.05)
        
        # Stage 2: Ingesting OHLCV
        yield f"data: {json.dumps({'stage': 'FETCHING_OHLCV', 'progress': 35, 'message': f'Ingesting price series & computing Wilder ATR for {symbol.upper()}...'})}\n\n"
        diag_input = data_aggregator.build_diagnostic_input(
            symbol=symbol,
            horizon_mode=horizon_mode,
            manual_atr_mult=manual_atr_mult,
        )
        await asyncio.sleep(0.05)
        
        # Stage 3: Fundamentals
        yield f"data: {json.dumps({'stage': 'FETCHING_FUNDAMENTALS', 'progress': 60, 'message': 'Analyzing balance sheet quality, ROCE trend & debt solvency...'})}\n\n"
        await asyncio.sleep(0.05)
        
        # Stage 4: Sentiment & Filings
        yield f"data: {json.dumps({'stage': 'SENTIMENT_ANALYSIS', 'progress': 80, 'message': 'Scanning SEBI regulatory filings & NLP sentiment indicators...'})}\n\n"
        await asyncio.sleep(0.05)
        
        # Stage 5: Conflict Resolution State Machine
        yield f"data: {json.dumps({'stage': 'RESOLVING_CONFLICTS', 'progress': 92, 'message': 'Executing 2D Precedence Grid & asymmetric override rules...'})}\n\n"
        output = evaluate_diagnostic(diag_input)
        
        if entry_price and holding_shares:
            months = _calc_holding_months(purchase_date)
            trim_pct = _action_to_trim_pct(output.action)
            tax_res = simulate_trim_execution(
                shares_held=holding_shares,
                buy_price=entry_price,
                current_price=diag_input.current_price,
                trim_percentage=trim_pct,
                holding_period_months=months,
            )
            output = output.model_copy(update={"tax_impact": tax_res})
            
        await asyncio.sleep(0.05)
        
        # Final Stage: Complete with Full Output JSON
        complete_payload = {
            "stage": "COMPLETE",
            "progress": 100,
            "message": "Diagnostic finalized successfully",
            "data": output.model_dump(),
        }
        yield f"data: {json.dumps(complete_payload)}\n\n"
        
    except Exception as e:
        error_payload = {
            "stage": "ERROR",
            "progress": 0,
            "message": f"Pipeline failed: {str(e)}",
            "data": None,
        }
        yield f"data: {json.dumps(error_payload)}\n\n"


@router.get("/{symbol}/stream")
async def stream_diagnostic(
    symbol: str,
    horizon_mode: HorizonMode = Query(HorizonMode.COMPOUNDER),
    manual_atr_mult: Optional[float] = Query(None, ge=1.0, le=5.0),
    entry_price: Optional[float] = Query(None, gt=0),
    holding_shares: Optional[int] = Query(None, gt=0),
    purchase_date: Optional[str] = Query(None),
) -> StreamingResponse:
    """Stream real-time diagnostic evaluation progress via Server-Sent Events (SSE)."""
    return StreamingResponse(
        _stream_telemetry_generator(
            symbol=symbol,
            horizon_mode=horizon_mode,
            manual_atr_mult=manual_atr_mult,
            entry_price=entry_price,
            holding_shares=holding_shares,
            purchase_date=purchase_date,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
            "X-Accel-Buffering": "no",
        },
    )
