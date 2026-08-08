"use client";

import React, { useState } from "react";
import { formatCurrency, formatPercent } from "@/lib/formatters";

interface TrimSimulatorProps {
  currentPrice: number;
}

export function TrimSimulator({ currentPrice }: TrimSimulatorProps) {
  const [holdingShares, setHoldingShares] = useState(100);
  const [buyPrice, setBuyPrice] = useState(Math.round(currentPrice * 0.78));
  const [trimPct, setTrimPct] = useState(25);
  const [holdingMonths, setHoldingMonths] = useState(14);

  // Real-time calculation logic based on Indian Finance Act 2024
  const sharesToSell = Math.max(1, Math.round(holdingShares * (trimPct / 100)));
  const sharesRetained = holdingShares - sharesToSell;
  const grossProceeds = sharesToSell * currentPrice;
  const costBasis = sharesToSell * buyPrice;
  const capitalGain = Math.max(0, grossProceeds - costBasis);

  const isLtcg = holdingMonths >= 12;
  const taxType = isLtcg ? "LTCG (12.5%)" : "STCG (20.0%)";
  const taxableGain = isLtcg ? Math.max(0, capitalGain - 125000) : capitalGain;
  const taxRate = isLtcg ? 0.125 : 0.2;
  const estimatedTax = taxableGain * taxRate;
  const netCash = grossProceeds - estimatedTax;

  // New effective breakeven price on retained shares
  const remainingCost = holdingShares * buyPrice - netCash;
  const newBreakeven = sharesRetained > 0 ? Math.max(0, remainingCost / sharesRetained) : 0;
  const downsideCushion = newBreakeven > 0 ? ((currentPrice - newBreakeven) / currentPrice) * 100 : 100;

  return (
    <div className="w-full border border-border-subtle bg-bg-secondary/40 p-5 font-mono">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-border-subtle mb-4">
        <span className="text-xs uppercase text-text-tertiary">
          // EXECUTION SIMULATOR (WHAT IF I TRIM NOW?)
        </span>
        <span className="text-[10px] px-1.5 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary">
          FINANCE ACT 2024 POST-TAX
        </span>
      </div>

      {/* Input Controls */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
        <div>
          <label className="text-[10px] text-text-tertiary uppercase block mb-1">
            SHARES HELD
          </label>
          <input
            type="number"
            value={holdingShares}
            onChange={(e) => setHoldingShares(Math.max(1, parseInt(e.target.value) || 0))}
            className="w-full bg-bg-primary border border-border-subtle text-text-primary text-xs px-3 py-2 focus:border-border-active focus:outline-none"
          />
        </div>

        <div>
          <label className="text-[10px] text-text-tertiary uppercase block mb-1">
            BUY PRICE (₹)
          </label>
          <input
            type="number"
            value={buyPrice}
            onChange={(e) => setBuyPrice(Math.max(1, parseFloat(e.target.value) || 0))}
            className="w-full bg-bg-primary border border-border-subtle text-text-primary text-xs px-3 py-2 focus:border-border-active focus:outline-none"
          />
        </div>

        <div>
          <label className="text-[10px] text-text-tertiary uppercase block mb-1">
            HOLDING (MONTHS)
          </label>
          <input
            type="number"
            value={holdingMonths}
            onChange={(e) => setHoldingMonths(Math.max(1, parseInt(e.target.value) || 0))}
            className="w-full bg-bg-primary border border-border-subtle text-text-primary text-xs px-3 py-2 focus:border-border-active focus:outline-none"
          />
        </div>

        <div>
          <label className="text-[10px] text-text-tertiary uppercase block mb-1">
            TRIM FRACTION
          </label>
          <div className="flex gap-1">
            {[25, 50, 100].map((pct) => (
              <button
                key={pct}
                type="button"
                onClick={() => setTrimPct(pct)}
                className={`flex-1 py-1.5 text-xs transition-colors border ${
                  trimPct === pct
                    ? "border-text-primary bg-grey-700 text-text-primary font-bold"
                    : "border-border-subtle bg-bg-primary text-text-secondary"
                }`}
              >
                {pct}%
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Tabular Output Ledger (Strict Grayscale Monospace) */}
      <div className="border-t border-border-subtle pt-4 divide-y divide-border-subtle/60 text-xs">
        <div className="flex justify-between py-1.5">
          <span className="text-text-secondary">SHARES TO SELL / RETAINED</span>
          <span className="text-text-primary font-bold">
            {sharesToSell} Sold / {sharesRetained} Retained
          </span>
        </div>

        <div className="flex justify-between py-1.5">
          <span className="text-text-secondary">GROSS CASH PROCEEDS</span>
          <span className="text-text-primary font-bold">
            {formatCurrency(grossProceeds)}
          </span>
        </div>

        <div className="flex justify-between py-1.5">
          <span className="text-text-secondary">REALIZED CAPITAL GAIN</span>
          <span className="text-text-primary font-bold">
            {formatCurrency(capitalGain)}
          </span>
        </div>

        <div className="flex justify-between py-1.5">
          <span className="text-text-secondary">ESTIMATED TAX ({taxType})</span>
          <span className="text-text-secondary">
            - {formatCurrency(estimatedTax)}
          </span>
        </div>

        <div className="flex justify-between py-2 border-t border-b border-border-subtle font-bold">
          <span className="text-text-primary">NET CASH ADDED TO WALLET</span>
          <span className="text-text-primary text-sm">
            {formatCurrency(netCash)}
          </span>
        </div>

        <div className="flex justify-between py-2 text-text-secondary">
          <span>NEW EFFECTIVE BREAKEVEN PRICE</span>
          <span className="text-text-primary font-bold">
            {formatCurrency(newBreakeven)} / share ({formatPercent(downsideCushion)} Cushion)
          </span>
        </div>
      </div>
    </div>
  );
}
