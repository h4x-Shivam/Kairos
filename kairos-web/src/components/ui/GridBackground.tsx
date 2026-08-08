"use client";

import React from "react";
import { Particles } from "./Particles";

interface GridBackgroundProps {
  children: React.ReactNode;
  className?: string;
  enableParticles?: boolean;
}

export function GridBackground({
  children,
  className = "",
  enableParticles = true,
}: GridBackgroundProps) {
  return (
    <div className={`relative min-h-[640px] w-full bg-bg-primary overflow-hidden ${className}`}>
      {/* Interactive WebGL Particles - Crisp & Bright */}
      {enableParticles && (
        <div className="absolute inset-0 pointer-events-none">
          <Particles
            particleColors={["#ffffff", "#ffffff", "#f0f0f0"]}
            particleCount={240}
            particleSpread={11}
            speed={0.15}
            particleBaseSize={100}
            moveParticlesOnHover={true}
            particleHoverFactor={0.5}
            alphaParticles={true}
            disableRotation={false}
          />
        </div>
      )}

      {/* Foreground Content */}
      <div className="relative z-10 w-full flex flex-col items-center justify-center">
        {children}
      </div>
    </div>
  );
}
