"use client";

import React, { useState } from "react";
import { formatCurrency } from "@/lib/formatters";

import { ChartDataPoint } from "@/types/diagnostic";

interface ChandelierChartProps {
  symbol: string;
  currentPrice: number;
  stopPrice: number;
  targetPrice: number;
  chartData: ChartDataPoint[];
}

export function ChandelierChart({
  symbol,
  currentPrice,
  stopPrice,
  targetPrice,
  chartData,
}: ChandelierChartProps) {
  const [timeframe, setTimeframe] = useState<"15m" | "1D" | "1W">("1D");

  // Use real chart data if available, fallback safely if not
  const candles = chartData && chartData.length > 0 ? chartData : [];
  
  // Need min/max to scale the Y axis
  const minPrice = candles.length > 0 
    ? Math.min(...candles.map((c) => Math.min(c.low, c.stop))) * 0.98 
    : currentPrice * 0.9;
  const maxPrice = candles.length > 0 
    ? Math.max(...candles.map((c) => Math.max(c.high, targetPrice))) * 1.02
    : currentPrice * 1.1;
    
  const priceRange = maxPrice - minPrice || 1;

  const getY = (price: number) => {
    return 200 - ((price - minPrice) / priceRange) * 180;
  };

  return (
    <div className="w-full font-mono flex flex-col gap-6 py-4">
      {/* Chart Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-border-subtle">
        <div className="flex items-center gap-3">
          <span className="text-[10px] uppercase text-text-tertiary tracking-widest">
            Chandelier Volatility Ratchet
          </span>
          <span className="text-[10px] text-text-tertiary">
            {symbol} • {timeframe}
          </span>
        </div>

        {/* Timeframe Switcher */}
        <div className="flex items-center gap-1 border border-border-subtle bg-bg-primary p-0.5 text-[10px]">
          {(["15m", "1D", "1W"] as const).map((tf) => (
            <button
              key={tf}
              type="button"
              onClick={() => setTimeframe(tf)}
              className={`px-2 py-0.5 transition-colors ${
                timeframe === tf
                  ? "bg-grey-700 text-text-primary font-bold"
                  : "text-text-tertiary hover:text-text-secondary"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* SVG Canvas Chart */}
      <div className="relative w-full h-56 sm:h-64">
        <svg className="w-full h-full" viewBox="0 0 500 220" preserveAspectRatio="none">
          {/* Target Price Line */}
          <line
            x1="0"
            y1={getY(targetPrice)}
            x2="500"
            y2={getY(targetPrice)}
            stroke="#9CA3AF"
            strokeWidth="1"
            strokeDasharray="4 4"
          />

          {/* 50 DMA Baseline Curve */}
          <path
            d={`M 0 ${getY(candles.length > 0 ? candles[0].close * 0.95 : currentPrice)} Q 250 ${getY(currentPrice * 0.95)} 500 ${getY(currentPrice * 0.97)}`}
            fill="none"
            stroke="#E5E7EB"
            strokeWidth="1.5"
          />

          {/* Ratcheting Chandelier Stop Step-Line */}
          <polyline
            points={candles
              .map((c, i) => {
                const xSpacing = 500 / Math.max(1, candles.length);
                const xStart = i * xSpacing;
                const xEnd = (i + 1) * xSpacing;
                return `${xStart},${getY(c.stop)} ${xEnd},${getY(c.stop)}`;
              })
              .join(" ")}
            fill="none"
            stroke="#D1D5DB"
            strokeWidth="2"
          />

          {/* Candlesticks */}
          {candles.map((c, idx) => {
            const xSpacing = 500 / Math.max(1, candles.length);
            const x = (idx + 0.5) * xSpacing;
            const isUp = c.close >= c.open;
            const openY = getY(c.open);
            const closeY = getY(c.close);
            const highY = getY(c.high);
            const lowY = getY(c.low);
            const topY = Math.min(openY, closeY);
            const bodyHeight = Math.max(2, Math.abs(openY - closeY));
            const candleWidth = Math.max(2, xSpacing * 0.6);

            return (
              <g key={idx}>
                {/* Wick */}
                <line
                  x1={x}
                  y1={highY}
                  x2={x}
                  y2={lowY}
                  stroke="#4B5563"
                  strokeWidth="1"
                />
                {/* Candle Body */}
                <rect
                  x={x - candleWidth / 2}
                  y={topY}
                  width={candleWidth}
                  height={bodyHeight}
                  fill={isUp ? "#FFFFFF" : "#111111"}
                  stroke="#111111"
                  strokeWidth="1"
                />
              </g>
            );
          })}
        </svg>

        {/* Floating Legend Badges */}
        <div className="absolute top-2 right-2 flex flex-col items-end gap-1 text-[10px] bg-bg-primary/90 border border-border-subtle p-2">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-grey-300" />
            <span className="text-text-secondary">CHANDELIER FLOOR: {formatCurrency(stopPrice)}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 border-t border-dashed border-grey-500" />
            <span className="text-text-tertiary">TARGET: {formatCurrency(targetPrice)}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-grey-700" />
            <span className="text-text-tertiary">50 DMA BASELINE</span>
          </div>
        </div>
      </div>
    </div>
  );
}
