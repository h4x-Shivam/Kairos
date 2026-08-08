"use client";

import { useState, useEffect } from "react";
import { HorizonMode } from "@/types/diagnostic";

export function useHorizonMode(initialMode: HorizonMode = "COMPOUNDER") {
  const [horizonMode, setHorizonMode] = useState<HorizonMode>(initialMode);

  useEffect(() => {
    try {
      const saved = localStorage.getItem("kairos_horizon_mode") as HorizonMode | null;
      if (saved === "COMPOUNDER" || saved === "SWING") {
        setHorizonMode(saved);
      }
    } catch {
      // Ignore localStorage errors in SSR/sandboxed mode
    }
  }, []);

  const toggleHorizonMode = (newMode?: HorizonMode) => {
    const next = newMode || (horizonMode === "COMPOUNDER" ? "SWING" : "COMPOUNDER");
    setHorizonMode(next);
    try {
      localStorage.setItem("kairos_horizon_mode", next);
    } catch {
      // Ignore
    }
  };

  return {
    horizonMode,
    setHorizonMode,
    toggleHorizonMode,
  };
}
