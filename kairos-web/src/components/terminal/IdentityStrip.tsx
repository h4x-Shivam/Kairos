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
  dayChangePct = -1.42,
  dayHigh = 956.0,
  dayLow = 938.1,
  beta = 1.12,
}: IdentityStripProps) {
  return (
    <div className="w-full border-b border-border-subtle bg-bg-secondary/40 px-4 sm:px-8 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-4">
      {/* Left: Identity Metadata */}
      <div className="flex items-baseline flex-wrap gap-3">
        <h1 className="font-mono text-xl sm:text-2xl font-black text-text-primary tracking-tight">
          {symbol}
        </h1>
        <span className="text-sm font-sans text-text-secondary">
          {companyName}
        </span>
        <span className="text-[10px] font-mono px-2 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary uppercase">
          {marketCapBucket}
        </span>
        <span className="text-xs font-mono text-text-tertiary">
          BETA {beta.toFixed(2)}
        </span>
      </div>

      {/* Right: Live Telemetry & Pricing */}
      <div className="flex items-baseline gap-4 sm:gap-6 font-mono text-sm">
        <div className="flex items-baseline gap-2">
          <span className="text-xs text-text-tertiary uppercase">LTP</span>
          <span className="text-lg sm:text-xl font-bold text-text-primary">
            {formatCurrency(currentPrice)}
          </span>
          <span className={`text-xs ${dayChangePct >= 0 ? "text-text-primary" : "text-text-secondary"}`}>
            ({formatPercent(dayChangePct, true)})
          </span>
        </div>

        <div className="hidden sm:flex items-center gap-3 text-xs text-text-tertiary border-l border-border-subtle pl-4">
          <span>H: {formatCurrency(dayHigh, false)}</span>
          <span>L: {formatCurrency(dayLow, false)}</span>
        </div>
      </div>
    </div>
  );
}
