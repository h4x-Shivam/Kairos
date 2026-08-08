"use client";

import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { ScoreCard } from "@/types/diagnostic";

interface DiagnosticGridProps {
  scores: ScoreCard;
}

interface ModuleData {
  id: string;
  code: string;
  title: string;
  score: number;
  status: "STRONG" | "WEAK" | "FAIR" | "POSITIVE" | "NEGATIVE";
  drivers: { label: string; value: string }[];
  subMetrics: { label: string; value: string; benchmark: string }[];
}

export function DiagnosticGrid({ scores }: DiagnosticGridProps) {
  const [expandedModule, setExpandedModule] = useState<string | null>(null);

  const modules: ModuleData[] = [
    {
      id: "fund",
      code: "FUND",
      title: "PILLAR A: FUNDAMENTAL QUALITY",
      score: scores.s_fund,
      status: scores.s_fund >= 70 ? "STRONG" : scores.s_fund >= 45 ? "FAIR" : "WEAK",
      drivers: [
        { label: "ROCE TREND", value: "21.4% (+3.2% QoQ)" },
        { label: "PEG RATIO", value: "1.12 (UNDERV)" },
        { label: "PROMOTER PLEDGE", value: "0.0% (CLEAR)" },
      ],
      subMetrics: [
        { label: "5Y Median P/E", value: "18.4x", benchmark: "22.0x Sector" },
        { label: "FCF / Net Profit", value: "0.88x", benchmark: "> 0.70x" },
        { label: "Debt-to-Equity", value: "0.42", benchmark: "< 1.00" },
        { label: "Interest Coverage", value: "6.8x", benchmark: "> 3.0x" },
      ],
    },
    {
      id: "tech",
      code: "TECH",
      title: "PILLAR B: TECHNICAL STRUCTURE",
      score: scores.s_tech,
      status: scores.s_tech >= 70 ? "STRONG" : scores.s_tech >= 45 ? "FAIR" : "WEAK",
      drivers: [
        { label: "DMA ALIGNMENT", value: "50 > 200 (BULL)" },
        { label: "14-DAY RSI", value: "41.2 (DECEL)" },
        { label: "DELIVERY %", value: "38.5% (STABLE)" },
      ],
      subMetrics: [
        { label: "RSI Bearish Divergence", value: "NONE", benchmark: "Clear" },
        { label: "Distance to 50 DMA", value: "+2.1%", benchmark: "Supported" },
        { label: "Distance to 200 DMA", value: "+14.8%", benchmark: "Bullish Trend" },
        { label: "5-Day Avg Delivery", value: "42.1%", benchmark: "> 35.0%" },
      ],
    },
    {
      id: "quant",
      code: "QUANT",
      title: "PILLAR C: QUANT & DOWNSIDE VOLATILITY",
      score: scores.s_quant,
      status: scores.s_quant >= 70 ? "STRONG" : scores.s_quant >= 45 ? "FAIR" : "WEAK",
      drivers: [
        { label: "52W DRAWDOWN", value: "-6.80% (NORMAL)" },
        { label: "1-YEAR BETA", value: "1.12 (MODERATE)" },
        { label: "ANN. VOLATILITY", value: "22.4% (STABLE)" },
      ],
      subMetrics: [
        { label: "Max Drawdown (1Y)", value: "-14.2%", benchmark: "-18.5% Nifty" },
        { label: "Wilder ATR(14)", value: "₹26.14", benchmark: "2.77% of LTP" },
        { label: "Downside Volatility", value: "14.8%", benchmark: "< 20.0%" },
        { label: "Quarter-Kelly Fraction", value: "25.0%", benchmark: "Max 35.0%" },
      ],
    },
    {
      id: "news",
      code: "NEWS",
      title: "PILLAR D: REGULATORY & SENTIMENT NLP",
      score: scores.s_news,
      status: scores.s_news >= 60 ? "POSITIVE" : scores.s_news >= 40 ? "FAIR" : "NEGATIVE",
      drivers: [
        { label: "TIER-1 TRIGGERS", value: "NONE (PASSED)" },
        { label: "FINBERT CONFIDENCE", value: "+0.84 (POS)" },
        { label: "FILING FREQUENCY", value: "4 FILINGS / 90D" },
      ],
      subMetrics: [
        { label: "Auditor Resignations", value: "0", benchmark: "Clean" },
        { label: "SEBI Inquiry Filings", value: "0", benchmark: "Clean" },
        { label: "Credit Rating Watch", value: "AAA Stable", benchmark: "Investment Grade" },
        { label: "Sentiment Decay Rate", value: "0.95^t", benchmark: "Active Half-Life" },
      ],
    },
  ];

  const toggleExpand = (id: string) => {
    setExpandedModule((prev) => (prev === id ? null : id));
  };

  return (
    <div className="w-full space-y-4 font-mono">
      <div className="flex items-center justify-between pb-2 border-b border-border-subtle">
        <span className="text-xs uppercase text-text-tertiary">
          // 4-PILLAR DIAGNOSTIC LEDGER
        </span>
        <span className="text-[10px] text-text-tertiary">
          TAP CARD FOR SUB-METRIC TRACE
        </span>
      </div>

      {/* 2x2 Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modules.map((m) => {
          const isExpanded = expandedModule === m.id;
          return (
            <div
              key={m.id}
              onClick={() => toggleExpand(m.id)}
              className="cursor-pointer border border-border-subtle bg-bg-secondary/40 p-5 hover:border-border-active transition-all"
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <span className="text-[11px] text-text-tertiary uppercase font-bold">
                  {m.code} // {m.title}
                </span>
                <span className="text-[10px] px-1.5 py-0.5 border border-border-subtle bg-bg-primary text-text-secondary">
                  {m.status}
                </span>
              </div>

              {/* Dominant Monospace Score */}
              <div className="flex items-baseline justify-between mb-4">
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl sm:text-4xl font-black text-text-primary">
                    {m.score.toFixed(1)}
                  </span>
                  <span className="text-xs text-text-tertiary">/ 100</span>
                </div>
                <button
                  type="button"
                  className="text-text-tertiary hover:text-text-primary p-1"
                >
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4" />
                  ) : (
                    <ChevronDown className="w-4 h-4" />
                  )}
                </button>
              </div>

              {/* 3 Driver Metrics */}
              <div className="grid grid-cols-3 gap-2 text-[11px] pt-3 border-t border-border-subtle">
                {m.drivers.map((d, i) => (
                  <div key={i}>
                    <span className="text-[9px] text-text-tertiary block uppercase truncate">
                      {d.label}
                    </span>
                    <span className="text-text-secondary font-semibold truncate block">
                      {d.value}
                    </span>
                  </div>
                ))}
              </div>

              {/* Inline Accordion Deep-Dive Table */}
              {isExpanded && (
                <div className="mt-4 pt-3 border-t border-border-subtle space-y-2 text-xs">
                  <div className="text-[10px] text-text-tertiary uppercase mb-1">
                    SUB-METRIC VERIFICATION TRACE:
                  </div>
                  {m.subMetrics.map((sm, i) => (
                    <div
                      key={i}
                      className="flex justify-between items-center py-1 border-b border-border-subtle/50 text-[11px]"
                    >
                      <span className="text-text-secondary">{sm.label}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-text-primary font-bold">{sm.value}</span>
                        <span className="text-text-tertiary text-[10px]">({sm.benchmark})</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
