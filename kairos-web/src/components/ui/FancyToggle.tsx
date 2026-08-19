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
      className={`relative inline-grid grid-cols-2 p-1 bg-bg-secondary border border-border-subtle rounded-md select-none ${className}`}
      role="radiogroup"
      aria-label="Horizon Mode Selector"
    >
      {/* Sliding active capsule */}
      <div
        className={`absolute top-1 bottom-1 left-1 w-[calc(50%-4px)] bg-bg-primary rounded border border-border-subtle shadow-sm transition-transform duration-300 ease-out pointer-events-none ${
          activeMode === "SWING" ? "translate-x-0" : "translate-x-full"
        }`}
      />

      {/* SWING Option */}
      <button
        type="button"
        role="radio"
        aria-checked={activeMode === "SWING"}
        onClick={() => handleSelect("SWING")}
        className={`relative z-10 flex items-center justify-center gap-2 px-4 sm:px-6 py-1.5 rounded text-xs font-mono tracking-wider uppercase transition-colors duration-200 cursor-pointer ${
          activeMode === "SWING"
            ? "text-text-primary font-bold"
            : "text-text-tertiary hover:text-text-secondary font-medium"
        }`}
      >
        <span>SWING</span>
        <span
          className={`text-[10px] hidden sm:inline transition-opacity duration-200 ${
            activeMode === "SWING" ? "text-text-secondary" : "text-text-tertiary"
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
        className={`relative z-10 flex items-center justify-center gap-2 px-4 sm:px-6 py-1.5 rounded text-xs font-mono tracking-wider uppercase transition-colors duration-200 cursor-pointer ${
          activeMode === "COMPOUNDER"
            ? "text-text-primary font-bold"
            : "text-text-tertiary hover:text-text-secondary font-medium"
        }`}
      >
        <span>COMPOUNDER</span>
        <span
          className={`text-[10px] hidden sm:inline transition-opacity duration-200 ${
            activeMode === "COMPOUNDER" ? "text-text-secondary" : "text-text-tertiary"
          }`}
        >
          3-12M
        </span>
      </button>
    </div>
  );
}
