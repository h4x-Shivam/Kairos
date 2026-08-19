"use client";

import React from "react";
import { formatCurrency, formatPercent } from "@/lib/formatters";
import { MarketCapBucket } from "@/types/diagnostic";

interface IdentityStripProps {
  symbol: string;
  companyName: string;
  marketCapBucket: MarketCapBucket;
  currentPrice: number;
  dayChangePct?: number;
  dayHigh?: number;
  dayLow?: number;
  beta?: number;
}

export function IdentityStrip({
  symbol,
  companyName,
  marketCapBucket,
  currentPrice,
  dayHigh,
  dayLow,
  beta,
}: IdentityStripProps) {
  const isStale =
    dayHigh !== undefined &&
    dayLow !== undefined &&
    (currentPrice < dayLow || currentPrice > dayHigh);
  return (
    <div className="w-full bg-bg-primary px-4 sm:px-8 py-8 flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-border-subtle">
      {/* Left: Identity Typography */}
      <div className="flex flex-col gap-2">
        <h1 className="font-sans text-3xl sm:text-4xl md:text-5xl font-black text-text-primary tracking-tight uppercase">
          {companyName}
        </h1>
        <div className="flex items-center gap-3 font-mono text-sm text-text-secondary">
          <span className="font-bold text-text-primary">{symbol}</span>
          <span>&middot;</span>
          <span className="capitalize">{marketCapBucket.replace('_', ' ').toLowerCase()}</span>
          {beta !== undefined && (
            <>
              <span>&middot;</span>
              <span>Beta {beta.toFixed(2)}</span>
            </>
          )}
          {isStale && (
            <span className="text-[10px] px-2 py-0.5 border border-signal-exit text-signal-exit font-bold uppercase animate-pulse ml-2">
              [STALE DATA]
            </span>
          )}
        </div>
      </div>

      {/* Right: Live Pricing */}
      <div className="flex flex-col md:items-end gap-1 font-mono">
        <div className="flex items-baseline gap-2">
          <span className="text-4xl sm:text-5xl font-black text-text-primary tracking-tight">
            {formatCurrency(currentPrice)}
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs text-text-tertiary">
          <span>Today&apos;s Range</span>
          {dayLow !== undefined && dayHigh !== undefined ? (
            <span className="text-text-secondary">
              {formatCurrency(dayLow, false)} &mdash; {formatCurrency(dayHigh, false)}
            </span>
          ) : (
            <span>N/A</span>
          )}
        </div>
      </div>
    </div>
  );
}
