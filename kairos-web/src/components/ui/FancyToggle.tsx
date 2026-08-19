"use client";

import React, { useState } from "react";
import { HorizonMode } from "@/types/diagnostic";

interface FancyToggleProps {
  mode?: HorizonMode;
  onChange?: (mode: HorizonMode) => void;
  className?: string;
}

export function FancyToggle({
  mode: controlledMode,
  onChange,
  className = "",
}: FancyToggleProps) {
  const [internalMode, setInternalMode] = useState<HorizonMode>("SWING");
  const activeMode = controlledMode ?? internalMode;

  const handleSelect = (newMode: HorizonMode) => {
    setInternalMode(newMode);
    onChange?.(newMode);
  };

  return (
    <div
      className={`relative inline-grid grid-cols-2 p-1 bg-[#0d0d0d] border border-white/15 rounded-full shadow-[0_4px_20px_rgba(0,0,0,0.7),inset_0_1px_1px_rgba(255,255,255,0.06)] select-none ${className}`}
      role="radiogroup"
      aria-label="Horizon Mode Selector"
    >
      {/* Mathematically precise sliding white capsule */}
      <div
        className={`absolute top-1 bottom-1 left-1 w-[calc(50%-4px)] bg-white rounded-full shadow-[0_2px_10px_rgba(255,255,255,0.25)] transition-transform duration-300 ease-out pointer-events-none ${
          activeMode === "SWING" ? "translate-x-0" : "translate-x-full"
        }`}
      />

      {/* SWING Option */}
      <button
        type="button"
        role="radio"
        aria-checked={activeMode === "SWING"}
        onClick={() => handleSelect("SWING")}
        className={`relative z-10 flex items-center justify-center gap-2 px-4 sm:px-6 py-1.5 rounded-full text-xs font-mono font-bold tracking-wider uppercase transition-colors duration-200 cursor-pointer ${
          activeMode === "SWING"
            ? "text-black"
            : "text-white/40 hover:text-white/80"
        }`}
      >
        <span
          className={`w-1.5 h-1.5 rounded-full transition-colors duration-200 flex-shrink-0 ${
            activeMode === "SWING"
              ? "bg-emerald-600 shadow-[0_0_6px_rgba(5,150,105,0.8)]"
              : "bg-white/20"
          }`}
        />
        <span>SWING</span>
        <span
          className={`text-[10px] hidden sm:inline transition-opacity duration-200 ${
            activeMode === "SWING" ? "text-black/60 font-medium" : "text-white/30"
          }`}
        >
          2-8W
        </span>
      </button>

      {/* COMPOUNDER Option */}
      <button
        type="button"
        role="radio"
        aria-checked={activeMode === "COMPOUNDER"}
        onClick={() => handleSelect("COMPOUNDER")}
        className={`relative z-10 flex items-center justify-center gap-2 px-4 sm:px-6 py-1.5 rounded-full text-xs font-mono font-bold tracking-wider uppercase transition-colors duration-200 cursor-pointer ${
          activeMode === "COMPOUNDER"
            ? "text-black"
            : "text-white/40 hover:text-white/80"
        }`}
      >
        <span
          className={`w-1.5 h-1.5 rounded-full transition-colors duration-200 flex-shrink-0 ${
            activeMode === "COMPOUNDER"
              ? "bg-emerald-600 shadow-[0_0_6px_rgba(5,150,105,0.8)]"
              : "bg-white/20"
          }`}
        />
        <span>COMPOUNDER</span>
        <span
          className={`text-[10px] hidden sm:inline transition-opacity duration-200 ${
            activeMode === "COMPOUNDER" ? "text-black/60 font-medium" : "text-white/30"
          }`}
        >
          3-12M
        </span>
      </button>
    </div>
  );
}
