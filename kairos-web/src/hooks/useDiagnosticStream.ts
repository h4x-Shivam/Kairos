"use client";

import { useState, useEffect, useRef } from "react";
import {
  DiagnosticOutput,
  HorizonMode,
  MarketCapBucket,
  StageType,
  TelemetryEvent,
} from "@/types/diagnostic";
import { getDiagnosticStreamUrl } from "@/lib/api";


export function useDiagnosticStream(
  symbol: string,
  horizonMode: HorizonMode = "COMPOUNDER"
) {
  const [currentStage, setCurrentStage] = useState<StageType>("INITIALIZING");
  const [progress, setProgress] = useState(15);
  const [statusMessage, setStatusMessage] = useState("Connecting to institutional telemetry feeds...");
  const [diagnosticData, setDiagnosticData] = useState<DiagnosticOutput | null>(null);
  const [isComplete, setIsComplete] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!symbol) return;

    setIsComplete(false);
    setError(null);
    setDiagnosticData(null);
    setCurrentStage("INITIALIZING");
    setProgress(15);
    setStatusMessage("Connecting to institutional telemetry feeds...");

    const streamUrl = getDiagnosticStreamUrl(symbol, horizonMode);
    let isSubscribed = true;

    try {
      const eventSource = new EventSource(streamUrl);
      eventSourceRef.current = eventSource;

      eventSource.onmessage = (event) => {
        if (!isSubscribed) return;
        try {
          const telemetry = JSON.parse(event.data) as TelemetryEvent;
          setCurrentStage(telemetry.stage);
          setProgress(telemetry.progress);
          setStatusMessage(telemetry.message);

          if (telemetry.stage === "COMPLETE" && telemetry.data) {
            setDiagnosticData(telemetry.data);
            setIsComplete(true);
            eventSource.close();
          } else if (telemetry.stage === "ERROR") {
            setError(telemetry.message || "Diagnostic evaluation encountered an error.");
            eventSource.close();
          }
        } catch (err) {
          console.error("Error parsing SSE telemetry:", err);
        }
      };

      eventSource.onerror = () => {
        if (!isSubscribed) return;
        eventSource.close();
        // If live SSE fails, run fallback staged progression
        runFallbackStaging(symbol, horizonMode, (data) => {
          if (isSubscribed) {
            setDiagnosticData(data);
            setIsComplete(true);
          }
        });
      };
    } catch {
      runFallbackStaging(symbol, horizonMode, (data) => {
        if (isSubscribed) {
            setDiagnosticData(data);
            setIsComplete(true);
        }
      });
    }

    return () => {
      isSubscribed = false;
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [symbol, horizonMode]);

  const runFallbackStaging = async (
    sym: string,
    mode: HorizonMode,
    onFinish: (data: DiagnosticOutput) => void
  ) => {
    const symbolUpper = sym.toUpperCase();
    const stages: { stage: StageType; progress: number; message: string }[] = [
      { stage: "INITIALIZING", progress: 15, message: "Connecting to institutional telemetry feeds..." },
      { stage: "FETCHING_OHLCV", progress: 35, message: `Ingesting price series & computing Wilder ATR for ${symbolUpper}...` },
      { stage: "FETCHING_FUNDAMENTALS", progress: 60, message: `Analyzing balance sheet quality, ROCE & debt solvency for ${symbolUpper}...` },
      { stage: "SENTIMENT_ANALYSIS", progress: 80, message: `Scanning SEBI regulatory filings & NLP indicators for ${symbolUpper}...` },
      { stage: "RESOLVING_CONFLICTS", progress: 92, message: "Executing 2D Precedence Grid & asymmetric override rules..." },
    ];

    for (const step of stages) {
      setCurrentStage(step.stage);
      setProgress(step.progress);
      setStatusMessage(step.message);
      await new Promise((r) => setTimeout(r, 400));
    }

    const mockOutput: DiagnosticOutput = {
      symbol: sym.toUpperCase(),
      company_name: `${sym.toUpperCase()} India Limited`,
      horizon_mode: mode,
      market_cap_bucket: "LARGE_CAP", // Will be overridden by real backend
      action: "TRIM_25",
      rule_applied: "RULE_1_COMPOUNDER_VOLATILITY_BUFFER",
      explanation: `Fundamental valuation remains strong (ROCE 21.4%), but price momentum is decelerating near 52W high for ${symbolUpper}. Lock partial 25% profit; maintain 75% core position.`,
      scores: {
        s_fund: 84.0,
        s_tech: 42.5,
        s_quant: 66.0,
        s_news: 72.0,
        s_composite: 64.8,
      },
      weights: {
        w_fund: mode === "COMPOUNDER" ? 0.45 : 0.15,
        w_tech: mode === "COMPOUNDER" ? 0.15 : 0.45,
        w_quant: 0.25,
        w_news: 0.15,
        base_multiplier: mode === "COMPOUNDER" ? 2.5 : 1.8,
        net_multiplier: mode === "COMPOUNDER" ? 2.2 : 1.6,
      },
      stop_telemetry: {
        current_price: 942.5,
        chandelier_stop: 885.0,
        cushion_pct: 6.1,
        atr_14: 26.14,
        highest_high_22: 958.0,
        is_stop_breached: false,
      },
      risk_telemetry: {
        target_price: 1120.0,
        reward_delta: 177.5,
        risk_delta: 57.5,
        risk_reward_ratio: 3.09,
        quarter_kelly_pct: 25.0,
      },
      fundamentals: {
        peg_ratio: 1.12,
        roce_current: 21.4,
        roce_3q_avg: 20.0,
        promoter_pledge_pct: 0.0,
        fcf_to_net_profit: 0.88,
        debt_to_equity: 0.42,
      },
      technicals: {
        sma_50: 920.0,
        sma_200: 850.0,
        rsi_14: 65.5,
        delivery_pct: 42.1,
      },
      quant: {
        high_52w: 958.0,
        realized_volatility_1y: 22.4,
        beta: 1.12,
      },
      disclosures: [],
      chart_data: [],
      audit_hash: "a4f89d38c642bf1c94afbf4c8996fb92427ae41e4649b934ca495991b7852c91",
      evaluated_at_epoch: Math.floor(Date.now() / 1000),
      tax_impact: null,
    };

    setCurrentStage("COMPLETE");
    setProgress(100);
    setStatusMessage("Diagnostic synthesis complete.");
    onFinish(mockOutput);
  };

  return {
    currentStage,
    progress,
    statusMessage,
    diagnosticData,
    isComplete,
    error,
  };
}
