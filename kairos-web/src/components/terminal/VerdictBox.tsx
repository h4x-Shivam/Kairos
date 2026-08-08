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

  // Determine Severity Styling Ladder (UI_UX.md Section 5)
  const getVerdictStyle = () => {
    if (isTier1Critical) {
      return "bg-signal-critical text-text-primary border-signal-critical";
    }
    switch (action) {
      case "HOLD":
        return "bg-transparent text-signal-good border-signal-good";
      case "TIGHTEN_STOP":
        return "bg-transparent text-text-primary border-grey-500";
      case "TRIM_25":
        return "bg-grey-500 text-text-primary border-grey-500";
      case "TRIM_50":
        return "bg-grey-900 text-text-primary border-grey-700 font-black";
      case "EXIT_FULLY":
        return "bg-bg-primary text-text-primary border-border-active tracking-wider font-black";
      default:
        return "bg-transparent text-text-primary border-border-subtle";
    }
  };

  const getVerdictLabel = () => {
    if (isTier1Critical) return "TIER 1 CRITICAL";
    return action.replace(/_/g, " ");
  };

  return (
    <div
      className={`relative w-full border p-6 transition-all ${
        isTier1Critical
          ? "border-signal-critical bg-signal-critical/10"
          : "border-border-subtle bg-bg-secondary/60"
      }`}
    >
      {/* Top Header: Metadata & Horizon Toggle */}
      <div className="flex items-center justify-between gap-2 mb-4 pb-3 border-b border-border-subtle flex-wrap">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono uppercase text-text-tertiary">
            // DIAGNOSTIC VERDICT
          </span>
          {isTier1Critical && (
            <span className="text-[10px] font-mono px-1.5 py-0.5 bg-signal-critical text-text-primary uppercase font-bold">
              GOVERNANCE BYPASS
            </span>
          )}
        </div>

        {/* Horizon Toggle */}
        <div className="flex items-center gap-1 border border-border-subtle bg-bg-primary p-0.5 text-[10px] font-mono">
          <button
            type="button"
            onClick={() => onToggleHorizon?.("SWING")}
            className={`px-2 py-0.5 transition-colors ${
              horizonMode === "SWING"
                ? "bg-grey-700 text-text-primary font-bold"
                : "text-text-tertiary hover:text-text-secondary"
            }`}
          >
            SWING
          </button>
          <button
            type="button"
            onClick={() => onToggleHorizon?.("COMPOUNDER")}
            className={`px-2 py-0.5 transition-colors ${
              horizonMode === "COMPOUNDER"
                ? "bg-grey-700 text-text-primary font-bold"
                : "text-text-tertiary hover:text-text-secondary"
            }`}
          >
            COMPOUNDER
          </button>
        </div>
      </div>

      {/* Dominant Verdict Block */}
      <div className="my-4">
        <div
          className={`inline-block px-5 py-2.5 border text-3xl sm:text-4xl md:text-5xl font-mono tracking-tight ${getVerdictStyle()}`}
        >
          {getVerdictLabel()}
        </div>
      </div>

      {/* Composite Score & Explanatory Reasoning */}
      <div className="space-y-3 mt-4">
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-2xl sm:text-3xl font-black text-text-primary">
            {scores.s_composite.toFixed(1)}
          </span>
          <span className="font-mono text-xs text-text-tertiary">/ 100 COMPOSITE SCORE</span>
        </div>

        <p className="text-xs sm:text-sm font-sans text-text-secondary leading-relaxed">
          {explanation}
        </p>

        {/* 2D Precedence Weights & Rule Tag */}
        <div className="pt-3 border-t border-border-subtle flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[11px] font-mono text-text-tertiary">
          <div>
            WEIGHTS: FUND {(weights.w_fund * 100).toFixed(0)}% · TECH {(weights.w_tech * 100).toFixed(0)}% · QUANT {(weights.w_quant * 100).toFixed(0)}% · NEWS {(weights.w_news * 100).toFixed(0)}%
          </div>
          <div className="flex items-center gap-2">
            <span className="px-1.5 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary">
              {ruleApplied}
            </span>
            <span>{formatTimestamp(evaluatedEpoch)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
