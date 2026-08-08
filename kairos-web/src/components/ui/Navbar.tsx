"use client";

import React from "react";
import Link from "next/link";
import { HorizonMode } from "@/types/diagnostic";
import { FancyToggle } from "@/components/ui/FancyToggle";

interface NavbarProps {
  horizonMode?: HorizonMode;
  onToggleHorizon?: (mode: HorizonMode) => void;
  scansRemaining?: number;
  maxScans?: number;
}

export function Navbar({ horizonMode, onToggleHorizon }: NavbarProps) {
  return (
    <header className="sticky top-0 z-50 w-full bg-transparent px-6 sm:px-12 py-6 flex items-center justify-between select-none">
      {/* Left Wordmark: svxm */}
      <div className="flex-1 flex justify-start">
        <Link href="/" className="inline-block hover:opacity-90 transition-opacity">
          <span className="font-display text-3xl sm:text-4xl md:text-[46px] tracking-wide text-text-primary lowercase leading-none block">
            svxm
          </span>
        </Link>
      </div>

      {/* Center: Fancy Horizon Mode Toggle */}
      <div className="flex-shrink-0 flex items-center justify-center">
        <FancyToggle mode={horizonMode} onChange={onToggleHorizon} />
      </div>

      {/* Right Wordmark: dev */}
      <div className="flex-1 flex justify-end">
        <span className="font-display text-3xl sm:text-4xl md:text-[46px] tracking-wide text-text-primary lowercase leading-none block">
          dev
        </span>
      </div>
    </header>
  );
}
