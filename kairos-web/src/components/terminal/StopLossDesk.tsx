"use client";

import React, { useState } from "react";
import { formatCurrency, formatPercent } from "@/lib/formatters";
import { StopLossTelemetry } from "@/types/diagnostic";

interface StopLossDeskProps {
  telemetry: StopLossTelemetry;
  baseMultiplier: number;
  onMultiplierChange?: (newMultiplier: number) => void;
}

export function StopLossDesk({
  telemetry,
  baseMultiplier = 2.2,
  onMultiplierChange,
}: StopLossDeskProps) {
  const [multiplier, setMultiplier] = useState(baseMultiplier);

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    setMultiplier(val);
    onMultiplierChange?.(val);
  };

  // Re-calculate live stop estimate for interactive slider
  const liveStop = telemetry.highest_high_22 - multiplier * telemetry.atr_14;
  const liveCushion = ((telemetry.current_price - liveStop) / telemetry.current_price) * 100;

  return (
    <div className="w-full border border-border-subtle bg-bg-secondary/40 p-5 font-mono">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-border-subtle mb-4">
        <span className="text-xs uppercase text-text-tertiary">
          // STOP-LOSS DESK
        </span>
        <span className="text-[10px] px-1.5 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary">
          MONOTONIC CHANDELIER
        </span>
      </div>

      {/* Primary Value */}
      <div className="mb-4">
        <div className="text-xs text-text-tertiary uppercase mb-1">
          TRAILED EXIT FLOOR
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-2xl sm:text-3xl font-black text-text-primary">
            {formatCurrency(liveStop)}
          </span>
          <span className="text-xs text-text-secondary">
            (-{formatPercent(Math.abs(liveCushion))} CUSHION)
          </span>
        </div>
      </div>

      {/* ATR Telemetry */}
      <div className="grid grid-cols-2 gap-3 py-3 border-t border-b border-border-subtle text-xs text-text-secondary mb-4">
        <div>
          <span className="text-text-tertiary block text-[10px] uppercase">14-PERIOD ATR</span>
          <span className="text-text-primary font-bold">{formatCurrency(telemetry.atr_14)}</span>
        </div>
        <div>
          <span className="text-text-tertiary block text-[10px] uppercase">22-DAY PEAK</span>
          <span className="text-text-primary font-bold">{formatCurrency(telemetry.highest_high_22)}</span>
        </div>
      </div>

      {/* Interactive ATR Multiplier Slider */}
      <div>
        <div className="flex justify-between text-xs mb-1.5">
          <span className="text-text-tertiary uppercase">VOLATILITY MULTIPLIER</span>
          <span className="text-text-primary font-bold">{multiplier.toFixed(1)}x ATR</span>
        </div>
        <input
          type="range"
          min="1.0"
          max="4.0"
          step="0.1"
          value={multiplier}
          onChange={handleSliderChange}
          className="w-full h-1 bg-grey-700 appearance-none cursor-pointer accent-text-primary"
        />
        <div className="flex justify-between text-[10px] text-text-tertiary mt-1">
          <span>1.0x (TIGHT)</span>
          <span>2.5x (STANDARD)</span>
          <span>4.0x (WIDE)</span>
        </div>
      </div>
    </div>
  );
}
