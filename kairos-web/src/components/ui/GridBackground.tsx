import React from "react";

interface GridBackgroundProps {
  children: React.ReactNode;
  className?: string;
}

export function GridBackground({ children, className = "" }: GridBackgroundProps) {
  return (
    <div className={`relative min-h-screen w-full bg-bg-primary overflow-hidden ${className}`}>
      {/* Dimmed 4-6% opacity structural grid */}
      <div 
        className="absolute inset-0 dark-grid-bg pointer-events-none opacity-60" 
      />
      
      {/* Radial vignette mask fading edges to pitch black */}
      <div 
        className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,transparent_0%,rgba(10,10,10,0.85)_70%,#0A0A0A_100%)]" 
      />

      {/* Foreground Content */}
      <div className="relative z-10 w-full">
        {children}
      </div>
    </div>
  );
}
