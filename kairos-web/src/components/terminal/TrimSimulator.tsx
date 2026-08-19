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
  const [buyDate, setBuyDate] = useState(() => {
    const d = new Date();
    d.setFullYear(d.getFullYear() - 1);
    return d.toISOString().split("T")[0];
  });

  // Calculate holding months from buy date
  const parsedBuyDate = new Date(buyDate);
  const now = new Date();
  const holdingMonths = Math.max(1, (now.getFullYear() - parsedBuyDate.getFullYear()) * 12 + (now.getMonth() - parsedBuyDate.getMonth()));

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
    <div className="w-full font-mono flex flex-col gap-6 py-4 border-b border-border-subtle pb-8">
      <div className="flex items-center justify-between pb-2 border-b border-border-subtle">
        <span className="text-[10px] uppercase text-text-tertiary tracking-widest">
          Execution Simulator
        </span>
        <span className="text-[10px] text-text-tertiary">
          POST-TAX (FINANCE ACT 2024)
        </span>
      </div>

      {/* Input Controls */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 mb-2">
        <div className="flex flex-col gap-1">
          <label className="text-[10px] text-text-tertiary uppercase tracking-widest">
            Shares Held
          </label>
          <input
            type="number"
            value={holdingShares}
            onChange={(e) => setHoldingShares(Math.max(1, parseInt(e.target.value) || 0))}
            className="w-full bg-transparent border-b border-border-subtle text-text-primary text-sm py-1.5 font-mono focus:border-border-active focus:outline-none transition-colors"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-[10px] text-text-tertiary uppercase tracking-widest">
            Buy Price (₹)
          </label>
          <input
            type="number"
            value={buyPrice}
            onChange={(e) => setBuyPrice(Math.max(1, parseFloat(e.target.value) || 0))}
            className="w-full bg-transparent border-b border-border-subtle text-text-primary text-sm py-1.5 font-mono focus:border-border-active focus:outline-none transition-colors"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-[10px] text-text-tertiary uppercase tracking-widest">
            Buy Date
          </label>
          <input
            type="date"
            value={buyDate}
            onChange={(e) => setBuyDate(e.target.value)}
            className="w-full bg-transparent border-b border-border-subtle text-text-primary text-sm py-1.5 font-mono focus:border-border-active focus:outline-none transition-colors"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-[10px] text-text-tertiary uppercase tracking-widest">
            Trim Fraction
          </label>
          <div className="flex gap-2 pt-1">
            {[25, 50, 100].map((pct) => (
              <button
                key={pct}
                type="button"
                onClick={() => setTrimPct(pct)}
                className={`flex-1 py-1 text-[11px] rounded transition-colors ${
                  trimPct === pct
                    ? "bg-bg-primary border border-border-active text-text-primary font-bold shadow-sm"
                    : "bg-bg-secondary border border-border-subtle text-text-secondary hover:text-text-primary"
                }`}
              >
                {pct}%
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Tabular Output Ledger */}
      <div className="border border-border-subtle bg-bg-secondary p-4 mt-2 divide-y divide-border-subtle/50 text-xs">
        <div className="flex justify-between items-center py-2.5 pt-1">
          <span className="text-text-secondary uppercase">Shares Sold / Retained</span>
          <span className="text-text-primary font-bold tabular-nums">
            {sharesToSell} / {sharesRetained}
          </span>
        </div>

        <div className="flex justify-between items-center py-2.5">
          <span className="text-text-secondary uppercase">Gross Cash Proceeds</span>
          <span className="text-text-primary font-bold tabular-nums">
            {formatCurrency(grossProceeds)}
          </span>
        </div>

        <div className="flex justify-between items-center py-2.5">
          <span className="text-text-secondary uppercase">Realized Capital Gain</span>
          <span className="text-text-primary font-bold tabular-nums">
            {formatCurrency(capitalGain)}
          </span>
        </div>

        <div className="flex justify-between items-center py-2.5">
          <span className="text-text-secondary uppercase">Estimated Tax ({taxType})</span>
          <span className="text-signal-exit tabular-nums">
            - {formatCurrency(estimatedTax)}
          </span>
        </div>

        <div className="flex justify-between items-center py-3 border-t border-border-active">
          <span className="text-text-primary uppercase font-bold">Net Cash Added to Wallet</span>
          <span className="text-text-primary text-lg font-black tabular-nums">
            {formatCurrency(netCash)}
          </span>
        </div>
      </div>

      <div className="flex justify-between items-center py-2 text-xs text-text-secondary">
        <span className="uppercase">New Effective Breakeven</span>
        <span className="text-text-primary font-bold tabular-nums">
          {formatCurrency(newBreakeven)} <span className="text-text-tertiary font-normal">/ share</span> ({formatPercent(downsideCushion)} cushion)
        </span>
      </div>
    </div>
  );
}
