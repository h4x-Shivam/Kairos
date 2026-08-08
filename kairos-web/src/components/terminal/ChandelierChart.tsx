"use client";

import React, { useState } from "react";
import { formatCurrency } from "@/lib/formatters";

interface ChandelierChartProps {
  symbol: string;
  currentPrice: number;
  stopPrice: number;
  targetPrice: number;
}

export function ChandelierChart({
  symbol,
  currentPrice,
  stopPrice,
  targetPrice,
}: ChandelierChartProps) {
  const [timeframe, setTimeframe] = useState<"15m" | "1D" | "1W">("1D");

  // Synthetic price points demonstrating monotonic Chandelier ratchet
  const base = currentPrice * 0.92;
  const candleData = [
    { o: base, h: base + 15, l: base - 10, c: base + 8, stop: base - 25 },
    { o: base + 8, h: base + 22, l: base + 5, c: base + 18, stop: base - 25 },
    { o: base + 18, h: base + 35, l: base + 12, c: base + 30, stop: base - 15 },
    { o: base + 30, h: base + 42, l: base + 20, c: base + 25, stop: base - 15 },
    { o: base + 25, h: base + 45, l: base + 22, c: base + 40, stop: base - 5 },
    { o: base + 40, h: base + 58, l: base + 35, c: base + 52, stop: base + 10 },
    { o: base + 52, h: base + 65, l: base + 48, c: base + 60, stop: base + 25 },
    { o: base + 60, h: base + 70, l: base + 55, c: base + 62, stop: base + 25 },
    { o: base + 62, h: base + 85, l: base + 60, c: currentPrice, stop: stopPrice },
  ];

  const minPrice = Math.min(...candleData.map((c) => Math.min(c.l, c.stop))) * 0.98;
  const maxPrice = Math.max(...candleData.map((c) => Math.max(c.h, targetPrice))) * 1.02;
  const priceRange = maxPrice - minPrice || 1;

  const getY = (price: number) => {
    return 200 - ((price - minPrice) / priceRange) * 180;
  };

  return (
    <div className="w-full border border-border-subtle bg-bg-secondary/40 p-5 font-mono">
      {/* Chart Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle mb-4">
        <div className="flex items-center gap-3">
          <span className="text-xs uppercase text-text-tertiary">
            // CHANDELIER VOLATILITY RATCHET
          </span>
          <span className="text-[10px] px-1.5 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary">
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
          {/* Target Price Line (Dashed Grayscale) */}
          <line
            x1="0"
            y1={getY(targetPrice)}
            x2="500"
            y2={getY(targetPrice)}
            stroke="#737373"
            strokeWidth="1"
            strokeDasharray="4 4"
          />

          {/* 50 DMA Baseline Curve */}
          <path
            d={`M 0 ${getY(base)} Q 250 ${getY(base + 30)} 500 ${getY(currentPrice * 0.97)}`}
            fill="none"
            stroke="#404040"
            strokeWidth="1.5"
          />

          {/* Ratcheting Chandelier Stop Step-Line */}
          <polyline
            points={candleData
              .map((c, i) => `${i * 55 + 25},${getY(c.stop)} ${i * 55 + 65},${getY(c.stop)}`)
              .join(" ")}
            fill="none"
            stroke="#B3B3B3"
            strokeWidth="2"
          />

          {/* Candlesticks */}
          {candleData.map((c, idx) => {
            const x = idx * 55 + 40;
            const isUp = c.c >= c.o;
            const openY = getY(c.o);
            const closeY = getY(c.c);
            const highY = getY(c.h);
            const lowY = getY(c.l);
            const topY = Math.min(openY, closeY);
            const bodyHeight = Math.max(2, Math.abs(openY - closeY));

            return (
              <g key={idx}>
                {/* Wick */}
                <line
                  x1={x}
                  y1={highY}
                  x2={x}
                  y2={lowY}
                  stroke="#737373"
                  strokeWidth="1"
                />
                {/* Candle Body */}
                <rect
                  x={x - 6}
                  y={topY}
                  width="12"
                  height={bodyHeight}
                  fill={isUp ? "#F5F5F5" : "#1A1A1A"}
                  stroke="#737373"
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
