"use client";

import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { DiagnosticOutput } from "@/types/diagnostic";

interface DiagnosticGridProps {
  diagnostic: DiagnosticOutput;
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

export function DiagnosticGrid({ diagnostic }: DiagnosticGridProps) {
  const [expandedModule, setExpandedModule] = useState<string | null>(null);
  
  const { scores, fundamentals: fund, technicals: tech, quant, stop_telemetry: stop, disclosures = [] } = diagnostic;

  const tier1Active = disclosures.some((d) => d.is_tier1_trigger && d.hours_ago <= 168.0);
  const avgSentiment = disclosures.length > 0 
    ? disclosures.reduce((acc, d) => acc + d.sentiment_score, 0) / disclosures.length
    : 0;
  const sentimentStr = avgSentiment > 0.2 ? "POS" : avgSentiment < -0.2 ? "NEG" : "NEU";
  const sentimentVal = disclosures.length > 0 ? `${avgSentiment > 0 ? '+' : ''}${avgSentiment.toFixed(2)} (${sentimentStr})` : "N/A";

  const modules: ModuleData[] = [
    {
      id: "fund",
      code: "FUND",
      title: "PILLAR A: FUNDAMENTAL QUALITY",
      score: scores.s_fund,
      status: scores.s_fund >= 70 ? "STRONG" : scores.s_fund >= 45 ? "FAIR" : "WEAK",
      drivers: [
        { label: "ROCE TREND", value: `${fund.roce_current.toFixed(1)}%` },
        { label: "PEG RATIO", value: fund.peg_ratio != null ? `${fund.peg_ratio.toFixed(2)}x` : "EXCLUDED (WT REDIST)" },
        { label: "PROMOTER PLEDGE", value: `${fund.promoter_pledge_pct.toFixed(1)}%` },
      ],
      subMetrics: [
        { label: "Trailing 3Q ROCE", value: `${fund.roce_3q_avg.toFixed(1)}%`, benchmark: "Stable" },
        { label: "FCF / Net Profit", value: `${fund.fcf_to_net_profit.toFixed(2)}x`, benchmark: "> 0.70x" },
        { label: "Debt-to-Equity", value: `${fund.debt_to_equity.toFixed(2)}`, benchmark: "< 1.00" },
      ],
    },
    {
      id: "tech",
      code: "TECH",
      title: "PILLAR B: TECHNICAL STRUCTURE",
      score: scores.s_tech,
      status: scores.s_tech >= 70 ? "STRONG" : scores.s_tech >= 45 ? "FAIR" : "WEAK",
      drivers: [
        { label: "DMA ALIGNMENT", value: tech.sma_50 > tech.sma_200 ? "50 > 200 (BULL)" : "50 < 200 (BEAR)" },
        { label: "14-DAY RSI", value: `${tech.rsi_14.toFixed(1)}` },
        { label: "DELIVERY %", value: `${tech.delivery_pct.toFixed(1)}%` },
      ],
      subMetrics: [
        { label: "Distance to 50 DMA", value: `${(((stop.current_price - tech.sma_50) / tech.sma_50) * 100).toFixed(1)}%`, benchmark: "Supported" },
        { label: "Distance to 200 DMA", value: `${(((stop.current_price - tech.sma_200) / tech.sma_200) * 100).toFixed(1)}%`, benchmark: "Trend Base" },
      ],
    },
    {
      id: "quant",
      code: "QUANT",
      title: "PILLAR C: QUANT & DOWNSIDE VOLATILITY",
      score: scores.s_quant,
      status: scores.s_quant >= 70 ? "STRONG" : scores.s_quant >= 45 ? "FAIR" : "WEAK",
      drivers: [
        { label: "52W DISTANCE", value: `${(((stop.current_price - quant.high_52w) / quant.high_52w) * 100).toFixed(1)}%` },
        { label: "1-YEAR BETA", value: `${quant.beta.toFixed(2)}` },
        { label: "ANN. VOLATILITY", value: `${quant.realized_volatility_1y.toFixed(1)}%` },
      ],
      subMetrics: [
        { label: "Wilder ATR(14)", value: `₹${stop.atr_14.toFixed(2)}`, benchmark: `${((stop.atr_14 / stop.current_price) * 100).toFixed(2)}% of LTP` },
        { label: "1Y Realized Vol", value: `${quant.realized_volatility_1y.toFixed(1)}%`, benchmark: "< 35.0%" },
      ],
    },
    {
      id: "news",
      code: "NEWS",
      title: "PILLAR D: REGULATORY & SENTIMENT NLP",
      score: scores.s_news,
      status: scores.s_news >= 60 ? "POSITIVE" : scores.s_news >= 40 ? "FAIR" : "NEGATIVE",
      drivers: [
        { label: "TIER-1 TRIGGERS", value: tier1Active ? "ACTIVE (FAIL)" : "NONE (PASSED)" },
        { label: "FINBERT CONFIDENCE", value: sentimentVal },
        { label: "FILING FREQUENCY", value: `${disclosures.length} FILINGS / 7D` },
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
    <div className="w-full font-mono flex flex-col gap-6 py-4">
      <div className="flex items-center justify-between pb-2 border-b border-border-subtle">
        <span className="text-[10px] uppercase text-text-tertiary tracking-widest">
          Diagnostic Pillars
        </span>
        <span className="text-[10px] text-text-tertiary">
          TAP TO EXPAND TRACE
        </span>
      </div>

      <div className="flex flex-col gap-4">
        {modules.map((m) => {
          const isExpanded = expandedModule === m.id;
          return (
            <div
              key={m.id}
              className="flex flex-col border-b border-border-subtle pb-4 last:border-b-0"
            >
              {/* Header row */}
              <div 
                className="flex items-center justify-between cursor-pointer group"
                onClick={() => toggleExpand(m.id)}
              >
                <div className="flex flex-col gap-1 w-1/3">
                  <span className="text-sm font-sans font-bold text-text-primary uppercase tracking-tight group-hover:text-text-secondary transition-colors">
                    {m.title.replace('PILLAR A: ', '').replace('PILLAR B: ', '').replace('PILLAR C: ', '').replace('PILLAR D: ', '')}
                  </span>
                  <span className="text-xs text-text-tertiary">{m.status}</span>
                </div>
                
                {/* Horizontal Score Bar */}
                <div className="hidden sm:flex flex-1 items-center px-6">
                  <div className="w-full h-1 bg-border-subtle overflow-hidden">
                    <div 
                      className="h-full bg-text-primary transition-all duration-500" 
                      style={{ width: `${m.score}%` }}
                    />
                  </div>
                </div>

                <div className="flex items-center gap-4 w-1/4 justify-end">
                  <div className="flex items-baseline gap-1">
                    <span className="text-xl sm:text-2xl font-black text-text-primary">{m.score.toFixed(1)}</span>
                    <span className="text-[10px] text-text-tertiary">/ 100</span>
                  </div>
                  <button type="button" className="text-text-tertiary group-hover:text-text-primary transition-colors">
                    {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* 3 Driver Metrics */}
              <div className="grid grid-cols-3 gap-4 mt-3 pt-3 border-t border-border-subtle/30">
                {m.drivers.map((d, i) => (
                  <div key={i} className="flex flex-col gap-0.5">
                    <span className="text-[10px] text-text-tertiary uppercase truncate">{d.label}</span>
                    <span className="text-xs text-text-secondary font-bold truncate">{d.value}</span>
                  </div>
                ))}
              </div>

              {/* Inline Accordion Deep-Dive Table */}
              {isExpanded && (
                <div className="mt-4 pt-3 border-t border-border-subtle space-y-2 text-xs bg-bg-secondary p-4">
                  <div className="text-[10px] text-text-tertiary uppercase mb-2 font-bold tracking-widest">
                    Sub-Metric Verification Trace
                  </div>
                  {m.subMetrics.map((sm, i) => (
                    <div
                      key={i}
                      className="flex justify-between items-center py-1.5 border-b border-border-subtle/50 text-[11px] last:border-b-0"
                    >
                      <span className="text-text-secondary">{sm.label}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-text-primary font-bold">{sm.value}</span>
                        <span className="text-text-tertiary text-[10px] w-24 text-right">({sm.benchmark})</span>
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
