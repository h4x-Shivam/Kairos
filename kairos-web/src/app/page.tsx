"use client";

import React from "react";
import { Navbar } from "@/components/ui/Navbar";
import { Particles } from "@/components/ui/Particles";
import { SearchCommand } from "@/components/ui/SearchCommand";
import { useHorizonMode } from "@/hooks/useHorizonMode";
import { ShieldCheck, TrendingDown, GitMerge } from "lucide-react";

export default function HomePage() {
  const { horizonMode, toggleHorizonMode } = useHorizonMode();

  return (
    <div className="relative min-h-screen bg-bg-primary text-text-primary flex flex-col font-sans overflow-x-hidden selection:bg-grey-700">
      {/* Full-Page Unified Interactive Particles Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <Particles
          particleColors={["#ffffff", "#ffffff", "#f0f0f0"]}
          particleCount={260}
          particleSpread={12}
          speed={0.15}
          particleBaseSize={100}
          moveParticlesOnHover={true}
          particleHoverFactor={0.4}
          alphaParticles={true}
          disableRotation={false}
        />
      </div>

      {/* Foreground Interactive Elements */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* 1st Slide: Full-Screen Viewport (100vh) */}
        <section className="min-h-screen w-full flex flex-col justify-between">
          <Navbar horizonMode={horizonMode} onToggleHorizon={toggleHorizonMode} />

          {/* Centered Hero Content */}
          <div className="flex-1 flex flex-col items-center justify-center px-4 sm:px-8 text-center my-auto">
            <div className="max-w-4xl mx-auto space-y-6 w-full flex flex-col items-center">
              {/* Display Headline: KAIROX */}
              <h1 className="text-6xl sm:text-7xl md:text-8xl lg:text-9xl font-display font-black tracking-tight text-text-primary uppercase leading-none select-none">
                KAIROX
              </h1>

              {/* Subtitle */}
              <p className="text-sm sm:text-base md:text-lg font-mono text-text-secondary max-w-xl">
                want to know, when to sell your holding?
              </p>

              {/* Command Search Bar */}
              <div className="w-full flex justify-center pt-3">
                <SearchCommand autoFocus />
              </div>
            </div>
          </div>

          {/* Subtle Scroll Hint */}
          <div className="pb-8 text-center select-none">
            <span className="text-[10px] font-mono uppercase text-text-tertiary tracking-widest">
              ↓ SCROLL FOR METHODOLOGY
            </span>
          </div>
        </section>

        <main className="flex-1 flex flex-col">
          {/* Section 4.2: 3 Proof Sections */}
          <section id="proof" className="max-w-5xl mx-auto px-4 sm:px-8 py-28 font-mono w-full">
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
              <div className="border border-border-subtle bg-bg-secondary/40 backdrop-blur-[2px] p-6 space-y-4">
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
              <div className="border border-border-subtle bg-bg-secondary/40 backdrop-blur-[2px] p-6 space-y-4">
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
              <div className="border border-border-subtle bg-bg-secondary/40 backdrop-blur-[2px] p-6 space-y-4">
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
        <footer className="w-full bg-transparent px-4 sm:px-8 py-8 font-mono text-xs text-text-secondary">
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
    </div>
  );
}
