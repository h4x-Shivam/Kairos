"use client";

import React from "react";
import Link from "next/link";
import { HorizonMode } from "@/types/diagnostic";

interface NavbarProps {
  horizonMode?: HorizonMode;
  onToggleHorizon?: (mode: HorizonMode) => void;
  scansRemaining?: number;
  maxScans?: number;
}

export function Navbar({
  horizonMode = "COMPOUNDER",
  onToggleHorizon,
  scansRemaining = 2,
  maxScans = 3,
}: NavbarProps) {
  return (
    <header className="sticky top-0 z-50 w-full bg-bg-primary/95 backdrop-blur border-b border-border-subtle px-4 sm:px-8 py-3.5 flex items-center justify-between">
      {/* Brand Wordmark */}
      <Link href="/" className="flex items-center gap-2 group">
        <span className="font-mono text-lg font-black tracking-tighter text-text-primary group-hover:text-grey-300 transition-colors">
          KAIROS
        </span>
        <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 border border-border-subtle text-text-secondary bg-bg-secondary">
          v1.0
        </span>
      </Link>

      {/* Center Navigation Links */}
      <nav className="hidden md:flex items-center gap-6 text-xs font-mono text-text-secondary">
        <Link href="/#proof" className="hover:text-text-primary transition-colors">
          // METHODOLOGY
        </Link>
        <Link href="/#audit" className="hover:text-text-primary transition-colors">
          // PROVENANCE
        </Link>
        <Link href="/#pricing" className="hover:text-text-primary transition-colors">
          // PRO ACCESS
        </Link>
      </nav>

      {/* Right Actions */}
      <div className="flex items-center gap-4 sm:gap-6">
        {/* Horizon Mode Toggle */}
        <div className="flex items-center gap-1.5 border border-border-subtle bg-bg-secondary p-1 text-[11px] font-mono">
          <button
            type="button"
            onClick={() => onToggleHorizon?.("SWING")}
            className={`px-2 py-0.5 transition-all ${
              horizonMode === "SWING"
                ? "bg-grey-700 text-text-primary font-semibold"
                : "text-text-tertiary hover:text-text-secondary"
            }`}
          >
            SWING
          </button>
          <button
            type="button"
            onClick={() => onToggleHorizon?.("COMPOUNDER")}
            className={`px-2 py-0.5 transition-all flex items-center gap-1 ${
              horizonMode === "COMPOUNDER"
                ? "bg-grey-700 text-text-primary font-semibold"
                : "text-text-tertiary hover:text-text-secondary"
            }`}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-signal-good inline-block" />
            COMPOUNDER
          </button>
        </div>

        {/* Free-tier Scan Quota Indicator */}
        <div className="flex items-center gap-1 text-[11px] font-mono text-text-secondary border border-border-subtle px-2.5 py-1 bg-bg-secondary">
          <span>⚡</span>
          <span>{scansRemaining}/{maxScans} SCANS</span>
        </div>
      </div>
    </header>
  );
}
