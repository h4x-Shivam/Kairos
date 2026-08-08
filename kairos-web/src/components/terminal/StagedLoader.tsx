"use client";

import React from "react";
import { StageType } from "@/types/diagnostic";

interface StagedLoaderProps {
  symbol: string;
  stage: StageType;
  progress: number;
  message: string;
}

export function StagedLoader({
  symbol,
  stage,
  progress,
  message,
}: StagedLoaderProps) {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center px-4 max-w-2xl mx-auto text-center">
      {/* Symbol Pill */}
      <div className="mb-6 inline-flex items-center gap-2 px-3 py-1 border border-border-subtle bg-bg-secondary text-xs font-mono text-text-secondary">
        <span className="w-1.5 h-1.5 rounded-full bg-text-primary animate-pulse" />
        <span>ANALYZING // {symbol}</span>
      </div>

      {/* Dominant Stage Name (Heavy Condensed Typography) */}
      <h2 className="text-3xl sm:text-4xl md:text-5xl font-mono font-black tracking-tight text-text-primary uppercase mb-4 transition-all duration-300">
        {stage.replace(/_/g, " ")}
      </h2>

      {/* Explanatory Stage Description */}
      <p className="text-sm sm:text-base font-sans text-text-secondary max-w-md mx-auto mb-10 h-12 flex items-center justify-center transition-opacity duration-300">
        {message}
      </p>

      {/* Minimalist Progress Track */}
      <div className="w-full max-w-md bg-grey-700 h-[2px] relative overflow-hidden mb-3">
        <div
          className="bg-text-primary h-full transition-all duration-300 ease-out"
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
      </div>

      {/* Progress Telemetry */}
      <div className="w-full max-w-md flex justify-between items-center text-[11px] font-mono text-text-tertiary">
        <span>TELEMETRY STREAM</span>
        <span>[{progress}%]</span>
      </div>
    </div>
  );
}
