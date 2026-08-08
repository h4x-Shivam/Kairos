"use client";

import React from "react";
import { Navbar } from "@/components/ui/Navbar";
import { GridBackground } from "@/components/ui/GridBackground";
import { SearchCommand } from "@/components/ui/SearchCommand";
import { useHorizonMode } from "@/hooks/useHorizonMode";
import { ShieldCheck, TrendingDown, GitMerge, Lock } from "lucide-react";

export default function HomePage() {
  const { horizonMode, toggleHorizonMode } = useHorizonMode();

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary flex flex-col font-sans">
      <Navbar horizonMode={horizonMode} onToggleHorizon={toggleHorizonMode} />

      <main className="flex-1">
        {/* Section 4.1: Hero Section */}
        <GridBackground className="flex flex-col items-center justify-center pt-20 pb-24 px-4 sm:px-8 text-center">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Version Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 border border-border-subtle bg-bg-secondary text-xs font-mono text-text-secondary">
              <span className="w-1.5 h-1.5 rounded-full bg-signal-good" />
              <span>KAIROS QUANT DIAGNOSTIC ENGINE</span>
            </div>

            {/* Display Headline */}
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-mono font-black tracking-tight text-text-primary uppercase leading-none">
              Know when to sell — before the market tells you.
            </h1>

            {/* Subhead */}
            <p className="text-base sm:text-lg font-sans text-text-secondary max-w-2xl mx-auto leading-relaxed">
              Algorithmic downside protection & disciplined exit engine for Indian equities.
              Mathematical precision without human emotion or generic AI summaries.
            </p>

            {/* Command Search Bar */}
            <div className="pt-6 pb-2 flex justify-center w-full">
              <SearchCommand autoFocus />
            </div>
          </div>
        </GridBackground>

        {/* Section 4.2: 3 Proof Sections */}
        <section id="proof" className="max-w-5xl mx-auto px-4 sm:px-8 py-20 border-t border-border-subtle font-mono">
          <div className="mb-12">
            <span className="text-xs uppercase text-text-tertiary block mb-1">
              // ARCHITECTURAL PROOF
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-text-primary uppercase tracking-tight">
              Deterministic Invariants Over Retail Emotion
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Proof 01 */}
            <div className="border border-border-subtle bg-bg-secondary/40 p-6 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
                <span className="text-xs text-text-tertiary">PROOF // 01</span>
                <TrendingDown className="w-4 h-4 text-text-secondary" />
              </div>
              <h3 className="text-sm font-bold text-text-primary uppercase">
                Drawdown Reduction vs. Buy & Hold
              </h3>
              <p className="text-xs font-sans text-text-secondary leading-relaxed">
                Trailing Chandelier stops ratchet strictly upward with price peaks. When a breakdown occurs, capital is protected before a minor correction transforms into a multi-year drawdown.
              </p>
              <div className="text-[11px] text-text-tertiary pt-2 border-t border-border-subtle">
                AVG MAX DD REDUCTION: <span className="text-text-primary font-bold">-44.2%</span>
              </div>
            </div>

            {/* Proof 02 */}
            <div className="border border-border-subtle bg-bg-secondary/40 p-6 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
                <span className="text-xs text-text-tertiary">PROOF // 02</span>
                <GitMerge className="w-4 h-4 text-text-secondary" />
              </div>
              <h3 className="text-sm font-bold text-text-primary uppercase">
                2D Precedence Conflict Resolution
              </h3>
              <p className="text-xs font-sans text-text-secondary leading-relaxed">
                When strong fundamentals clash with waning momentum, Kairos executes deterministic precedence rules — preventing premature panic sales while enforcing fractional Kelly profit-locking.
              </p>
              <div className="text-[11px] text-text-tertiary pt-2 border-t border-border-subtle">
                ASYNCHRONOUS OVERRIDES: <span className="text-text-primary font-bold">6 HARD RULES</span>
              </div>
            </div>

            {/* Proof 03 */}
            <div className="border border-border-subtle bg-bg-secondary/40 p-6 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
                <span className="text-xs text-text-tertiary">PROOF // 03</span>
                <ShieldCheck className="w-4 h-4 text-text-secondary" />
              </div>
              <h3 className="text-sm font-bold text-text-primary uppercase">
                SHA-256 Reproducibility Signature
              </h3>
              <p className="text-xs font-sans text-text-secondary leading-relaxed">
                Every calculation is stamped with a cryptographic SHA-256 hash locked to raw market ticks and SEBI filing timestamps. 100% auditable and mathematically transparent.
              </p>
              <div className="text-[11px] text-text-tertiary pt-2 border-t border-border-subtle">
                AUDIT COMPLIANCE: <span className="text-text-primary font-bold">DETERMINISTIC</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-border-subtle bg-bg-secondary/40 px-4 sm:px-8 py-8 font-mono text-xs text-text-secondary">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="font-bold text-text-primary">KAIROS</span>
            <span className="text-text-tertiary">// QUANTITATIVE EXIT ENGINE</span>
          </div>
          <div className="text-[11px] text-text-tertiary">
            SEBI Sandbox Diagnostic Protocol • Pure Deterministic Math
          </div>
        </div>
      </footer>
    </div>
  );
}
