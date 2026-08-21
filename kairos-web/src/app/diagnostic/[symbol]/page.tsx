"use client";

import React, { use } from "react";
import { Navbar } from "@/components/ui/Navbar";
import { StagedLoader } from "@/components/terminal/StagedLoader";
import { IdentityStrip } from "@/components/terminal/IdentityStrip";
import { VerdictBox } from "@/components/terminal/VerdictBox";
import { StopLossDesk } from "@/components/terminal/StopLossDesk";
import { RiskRewardDesk } from "@/components/terminal/RiskRewardDesk";
import { ChandelierChart } from "@/components/terminal/ChandelierChart";
import { DiagnosticGrid } from "@/components/terminal/DiagnosticGrid";
import { TrimSimulator } from "@/components/terminal/TrimSimulator";
import { AuditFooter } from "@/components/terminal/AuditFooter";
import { useDiagnosticStream } from "@/hooks/useDiagnosticStream";
import { useHorizonMode } from "@/hooks/useHorizonMode";

interface DiagnosticPageProps {
  params: Promise<{ symbol: string }>;
}

export default function DiagnosticPage({ params }: DiagnosticPageProps) {
  const resolvedParams = use(params);
  const symbol = decodeURIComponent(resolvedParams.symbol).toUpperCase();
  const { horizonMode, toggleHorizonMode } = useHorizonMode();

  const {
    currentStage,
    progress,
    statusMessage,
    diagnosticData,
    isComplete,
  } = useDiagnosticStream(symbol, horizonMode);

  const latestBar = diagnosticData?.chart_data?.[diagnosticData.chart_data.length - 1];

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary flex flex-col font-sans">
      <Navbar horizonMode={horizonMode} onToggleHorizon={toggleHorizonMode} />

      {!isComplete || !diagnosticData ? (
        // Editorial Staged Loading Transition
        <main className="flex-1 flex items-center justify-center">
          <StagedLoader
            symbol={symbol}
            stage={currentStage}
            progress={progress}
            message={statusMessage}
          />
        </main>
      ) : (
        // 7-Zone Full Diagnostic Terminal Dashboard
        <main className="flex-1 flex flex-col w-full pb-16">
          {/* Zone 1: Identity Strip */}
          <IdentityStrip
            symbol={diagnosticData.symbol}
            companyName={diagnosticData.company_name}
            marketCapBucket={diagnosticData.market_cap_bucket}
            currentPrice={diagnosticData.stop_telemetry.current_price}
            dayHigh={latestBar?.high}
            dayLow={latestBar?.low}
            beta={diagnosticData.quant.beta}
          />

          <div className="max-w-7xl mx-auto w-full px-4 sm:px-8 py-6 space-y-6">
            {/* Zone 2: Verdict Box */}
            <div className="w-full">
              <VerdictBox
                action={diagnosticData.action}
                ruleApplied={diagnosticData.rule_applied}
                scores={diagnosticData.scores}
                weights={diagnosticData.weights}
                explanation={diagnosticData.explanation}
                plainSummary={diagnosticData.plain_language?.summary}
                evaluatedEpoch={diagnosticData.evaluated_at_epoch}
                horizonMode={horizonMode}
                onToggleHorizon={toggleHorizonMode}
              />
            </div>

            {/* De-emphasize subsequent zones if Tier-1 Hard Governance Override triggered */}
            <div
              className={`space-y-6 transition-opacity duration-300 ${
                diagnosticData.rule_applied === "TIER_1_HARD_GOVERNANCE_BYPASS"
                  ? "opacity-40 pointer-events-none"
                  : "opacity-100"
              }`}
            >
              {/* Zone 3: Stop-Loss Desk + Risk/Reward Desk Side-by-Side */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <StopLossDesk
                  telemetry={diagnosticData.stop_telemetry}
                  baseMultiplier={diagnosticData.weights.net_multiplier}
                />
                <RiskRewardDesk
                  telemetry={diagnosticData.risk_telemetry}
                  currentPrice={diagnosticData.stop_telemetry.current_price}
                />
              </div>

              {/* Zone 4: Chandelier Chart Canvas */}
              <ChandelierChart
                symbol={diagnosticData.symbol}
                currentPrice={diagnosticData.stop_telemetry.current_price}
                stopPrice={diagnosticData.stop_telemetry.chandelier_stop}
                targetPrice={diagnosticData.risk_telemetry.target_price}
                chartData={diagnosticData.chart_data}
              />

              {/* Zone 5: Execution Simulator ("What If I Trim Now?") */}
              <TrimSimulator
                currentPrice={diagnosticData.stop_telemetry.current_price}
              />

              {/* Zone 6: 4-Pillar Diagnostic Ledger Grid */}
              <DiagnosticGrid diagnostic={diagnosticData} />
            </div>
          </div>

          {/* Zone 7: Regulatory Audit Footer */}
          <AuditFooter diagnostic={diagnosticData} />
        </main>
      )}
    </div>
  );
}
