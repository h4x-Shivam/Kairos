"use client";

import React from "react";
import {
  HorizonMode,
  OverrideRule,
  PrecedenceWeights,
  PrimaryAction,
  ScoreCard,
} from "@/types/diagnostic";
import { formatTimestamp } from "@/lib/formatters";

interface VerdictBoxProps {
  action: PrimaryAction;
  ruleApplied: OverrideRule;
  scores: ScoreCard;
  weights: PrecedenceWeights;
  explanation: string;
  evaluatedEpoch: number;
  horizonMode: HorizonMode;
  onToggleHorizon?: (mode: HorizonMode) => void;
}

export function VerdictBox({
  action,
  ruleApplied,
  scores,
  weights,
  explanation,
  evaluatedEpoch,
  horizonMode,
  onToggleHorizon,
}: VerdictBoxProps) {
  const isTier1Critical = ruleApplied === "TIER_1_HARD_GOVERNANCE_BYPASS";

  const getIndicatorColor = () => {
    if (isTier1Critical) return "bg-signal-critical";
    switch (action) {
      case "HOLD":
        return "bg-signal-hold";
      case "TIGHTEN_STOP":
        return "bg-signal-tighten";
      case "TRIM_25":
        return "bg-signal-trim25";
      case "TRIM_50":
        return "bg-signal-trim50";
      case "EXIT_FULLY":
        return "bg-signal-exit";
      default:
        return "bg-grey-500";
    }
  };

  const getVerdictLabel = () => {
    if (isTier1Critical) return "TIER 1 CRITICAL";
    return action.replace(/_/g, " ");
  };

  return (
    <div className="w-full flex flex-col gap-6 py-6 border-b border-border-subtle">
      <div className="flex flex-col gap-1">
        <span className="text-xs font-mono font-bold tracking-widest text-text-tertiary uppercase">
          Diagnostic Verdict
        </span>
        
        <div className="flex items-center gap-4 mt-2">
          <div className={`w-3 h-3 rounded-full ${getIndicatorColor()}`} />
          <h2 className={`font-sans text-4xl sm:text-5xl md:text-6xl font-black uppercase tracking-tight text-text-primary`}>
            {getVerdictLabel()}
          </h2>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center gap-6 mt-2">
        <div className="flex items-baseline gap-2">
          <span className="font-mono text-3xl font-black text-text-primary">
            {scores.s_composite.toFixed(1)}
          </span>
          <span className="font-mono text-xs text-text-tertiary">/ 100</span>
        </div>

        <div className="w-px h-8 bg-border-subtle hidden sm:block" />

        <p className="text-sm md:text-base font-sans text-text-secondary leading-relaxed max-w-3xl">
          {explanation}
        </p>
      </div>
      
      {isTier1Critical && (
        <div className="inline-block px-3 py-1 bg-signal-critical/10 border border-signal-critical text-signal-critical text-xs font-bold uppercase mt-2 w-max">
          Governance Bypass Engaged
        </div>
      )}
    </div>
  );
}
