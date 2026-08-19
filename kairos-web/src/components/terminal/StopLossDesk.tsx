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
    <div className="w-full font-mono flex flex-col gap-6 py-4">
      {/* Primary Value */}
      <div>
        <div className="text-[10px] text-text-tertiary uppercase tracking-widest mb-2">
          Trailing Stop
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-3xl sm:text-4xl font-black text-text-primary">
            {formatCurrency(liveStop)}
          </span>
          <span className="text-sm text-signal-exit font-bold">
            -{formatPercent(Math.abs(liveCushion))} cushion
          </span>
        </div>
      </div>

      {/* ATR Telemetry & Slider */}
      <div className="space-y-6 max-w-sm">
        <div className="flex items-center justify-between text-xs border-b border-border-subtle pb-2">
          <span className="text-text-tertiary uppercase">ATR(14)</span>
          <span className="text-text-primary font-bold">{formatCurrency(telemetry.atr_14)}</span>
        </div>
        <div className="flex items-center justify-between text-xs border-b border-border-subtle pb-2">
          <span className="text-text-tertiary uppercase">22-Day Peak</span>
          <span className="text-text-primary font-bold">{formatCurrency(telemetry.highest_high_22)}</span>
        </div>

        {/* Precision ATR Multiplier Control */}
        <div className="pt-2">
          <div className="flex justify-between items-center text-xs mb-3">
            <span className="text-text-tertiary uppercase text-[10px] tracking-widest">Volatility Multiplier</span>
            <span className="text-text-primary font-bold">{multiplier.toFixed(1)}× ATR</span>
          </div>
          
          <div className="relative h-4 flex items-center group">
            {/* Custom Precision Track */}
            <div className="absolute w-full h-[1px] bg-border-active" />
            
            {/* Custom Thumb indicator driven by value */}
            <div 
              className="absolute h-2.5 w-2.5 bg-text-primary rounded-full transition-all duration-75 pointer-events-none group-hover:scale-125"
              style={{ left: `calc(${((multiplier - 1.0) / (4.0 - 1.0)) * 100}% - 5px)` }}
            />

            {/* Invisible native range input for interaction */}
            <input
              type="range"
              min="1.0"
              max="4.0"
              step="0.1"
              value={multiplier}
              onChange={handleSliderChange}
              className="absolute w-full h-full opacity-0 cursor-ew-resize m-0 p-0"
              aria-label="Volatility Multiplier"
            />
          </div>
          <div className="flex justify-between text-[10px] text-text-tertiary mt-2">
            <span>1.0× Tight</span>
            <span>2.5× Standard</span>
            <span>4.0× Wide</span>
          </div>
        </div>
      </div>
    </div>
  );
}
