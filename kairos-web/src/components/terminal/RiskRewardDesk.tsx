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
    <div className="w-full font-mono flex flex-col gap-6 py-4 border-l-0 lg:border-l lg:border-border-subtle lg:pl-6">
      {/* Primary Value */}
      <div>
        <div className="text-[10px] text-text-tertiary uppercase tracking-widest mb-2">
          Analyst Target Price
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-3xl sm:text-4xl font-black text-text-primary">
            {formatCurrency(activeTarget)}
          </span>
          <span className="text-sm text-signal-hold font-bold">
            +{formatPercent(((activeTarget - currentPrice) / currentPrice) * 100)} potential
          </span>
        </div>
      </div>

      {/* R:R and Kelly Grid */}
      <div className="space-y-6 max-w-sm">
        <div className="flex items-center justify-between text-xs border-b border-border-subtle pb-2">
          <span className="text-text-tertiary uppercase">Risk / Reward</span>
          <span className="text-text-primary font-bold">1 : {rrRatio}</span>
        </div>
        <div className="flex items-center justify-between text-xs border-b border-border-subtle pb-2">
          <span className="text-text-tertiary uppercase">Fractional Kelly</span>
          <span className="text-text-primary font-bold">{telemetry.quarter_kelly_pct.toFixed(1)}% size</span>
        </div>
        
        {/* Custom Target Override Input */}
        <div className="pt-2">
          <label className="flex justify-between items-center text-xs mb-3 text-text-tertiary uppercase text-[10px] tracking-widest">
            Set Custom Target (₹)
          </label>
          <input
            type="number"
            placeholder={telemetry.target_price.toString()}
            onChange={(e) => {
              const val = parseFloat(e.target.value);
              setCustomTarget(isNaN(val) || val <= 0 ? null : val);
            }}
            className="w-full bg-transparent border-b border-border-subtle text-text-primary text-sm py-1.5 font-mono focus:border-border-active focus:outline-none transition-colors"
          />
        </div>
      </div>
    </div>
  );
}
