"use client";

import React, { useState } from "react";
import { formatCurrency, formatPercent } from "@/lib/formatters";
import { RiskRewardTelemetry } from "@/types/diagnostic";

interface RiskRewardDeskProps {
  telemetry: RiskRewardTelemetry;
  currentPrice: number;
}

export function RiskRewardDesk({
  telemetry,
  currentPrice,
}: RiskRewardDeskProps) {
  const [customTarget, setCustomTarget] = useState<number | null>(null);

  const activeTarget = customTarget || telemetry.target_price;
  const rewardDelta = Math.max(0, activeTarget - currentPrice);
  const riskDelta = telemetry.risk_delta;
  const rrRatio = riskDelta > 0 ? (rewardDelta / riskDelta).toFixed(2) : "0.00";

  return (
    <div className="w-full border border-border-subtle bg-bg-secondary/40 p-5 font-mono">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-border-subtle mb-4">
        <span className="text-xs uppercase text-text-tertiary">
          // RISK / REWARD & SIZING
        </span>
        <span className="text-[10px] px-1.5 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary">
          ANALYST CONSENSUS
        </span>
      </div>

      {/* Target Price */}
      <div className="mb-4">
        <div className="text-xs text-text-tertiary uppercase mb-1">
          ANALYST TARGET PRICE
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-2xl sm:text-3xl font-black text-text-primary">
            {formatCurrency(activeTarget)}
          </span>
          <span className="text-xs text-text-secondary">
            (+{formatPercent(((activeTarget - currentPrice) / currentPrice) * 100)} POTENTIAL)
          </span>
        </div>
      </div>

      {/* R:R and Kelly Grid */}
      <div className="grid grid-cols-2 gap-3 py-3 border-t border-b border-border-subtle text-xs mb-4">
        <div>
          <span className="text-text-tertiary block text-[10px] uppercase">R:R RATIO</span>
          <span className="text-text-primary font-bold">1 : {rrRatio}</span>
        </div>
        <div>
          <span className="text-text-tertiary block text-[10px] uppercase">FRACTIONAL KELLY</span>
          <span className="text-text-primary font-bold">{telemetry.quarter_kelly_pct.toFixed(1)}% SIZE</span>
        </div>
      </div>

      {/* Custom Target Override Input */}
      <div>
        <span className="text-text-tertiary block text-[10px] uppercase mb-1">
          SET CUSTOM TARGET (₹)
        </span>
        <input
          type="number"
          placeholder={telemetry.target_price.toString()}
          onChange={(e) => {
            const val = parseFloat(e.target.value);
            setCustomTarget(isNaN(val) || val <= 0 ? null : val);
          }}
          className="w-full bg-bg-primary border border-border-subtle text-text-primary text-xs px-3 py-2 font-mono focus:border-border-active focus:outline-none"
        />
      </div>
    </div>
  );
}
