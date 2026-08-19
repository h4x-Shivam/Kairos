"use client";

import React, { useState } from "react";
import { Copy, Check, ShieldCheck } from "lucide-react";
import { Modal } from "@/components/ui/Modal";
import { truncateHash, formatTimestamp } from "@/lib/formatters";
import { DiagnosticOutput } from "@/types/diagnostic";

interface AuditFooterProps {
  diagnostic: DiagnosticOutput;
}

export function AuditFooter({ diagnostic }: AuditFooterProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isTraceOpen, setIsTraceOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(diagnostic.audit_hash);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <>
      <footer className="w-full mt-12 mb-8 font-mono text-xs text-text-secondary border-t border-border-subtle pt-6">
        <div className="flex flex-col gap-6 max-w-5xl">
          
          {/* Provenance Trace Toggle */}
          <div>
            <button
              onClick={() => setIsTraceOpen(!isTraceOpen)}
              className="flex items-center gap-2 text-text-primary font-bold uppercase hover:opacity-80 transition-opacity"
            >
              {isTraceOpen ? "− HIDE CALCULATION TRACE" : "+ VIEW CALCULATION TRACE"}
            </button>
            
            {isTraceOpen && (
              <div className="mt-4 p-4 bg-bg-secondary border border-border-subtle space-y-4 text-xs font-mono">
                <div>
                  <span className="text-text-tertiary">RULE APPLIED:</span>{" "}
                  <span className="text-text-primary font-bold">{diagnostic.rule_applied}</span>
                </div>
                <div>
                  <span className="text-text-tertiary">EVALUATED AT:</span>{" "}
                  <span className="text-text-primary">{formatTimestamp(diagnostic.evaluated_at_epoch)}</span>
                </div>
                <div>
                  <span className="text-text-tertiary">PRECEDENCE WEIGHTS:</span>
                  <div className="mt-1 grid grid-cols-2 sm:grid-cols-4 gap-2">
                    <div className="p-2 border border-border-subtle bg-bg-primary">
                      FUND: {(diagnostic.weights.w_fund * 100).toFixed(0)}%
                    </div>
                    <div className="p-2 border border-border-subtle bg-bg-primary">
                      TECH: {(diagnostic.weights.w_tech * 100).toFixed(0)}%
                    </div>
                    <div className="p-2 border border-border-subtle bg-bg-primary">
                      QUANT: {(diagnostic.weights.w_quant * 100).toFixed(0)}%
                    </div>
                    <div className="p-2 border border-border-subtle bg-bg-primary">
                      NEWS: {(diagnostic.weights.w_news * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
            {/* SEBI Compliance Statement */}
            <div className="max-w-xl text-[11px] leading-relaxed text-text-secondary">
              <span className="text-text-primary font-bold mr-1">REGULATORY NOTICE &middot;</span>
              Kairos is a deterministic mathematical diagnostic sandbox. Not SEBI registered investment advice. Historical algorithms do not guarantee future returns.
            </div>

            {/* Cryptographic SHA-256 Verification Action */}
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5 px-3 py-1.5 text-[11px] text-text-tertiary">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>HASH:</span>
                <span className="text-text-secondary">
                  {truncateHash(diagnostic.audit_hash, 8, 8)}
                </span>
              </div>

              <button
                type="button"
                onClick={handleCopy}
                className="p-1.5 text-text-tertiary hover:text-text-primary transition-colors"
                title="Copy SHA-256 Hash"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              </button>

              <button
                type="button"
                onClick={() => setIsModalOpen(true)}
                className="px-2.5 py-1.5 text-[11px] text-text-primary font-bold hover:bg-bg-secondary transition-colors"
              >
                INSPECT JSON
              </button>
            </div>
          </div>
        </div>
      </footer>

      {/* JSON & Hash Inspector Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="CRYPTOGRAPHIC AUDIT & DETERMINISTIC STATE PROOF"
      >
        <div className="space-y-4 text-xs font-mono">
          <div>
            <span className="text-text-tertiary block mb-1 uppercase">
              SHA-256 REPRODUCIBILITY SIGNATURE:
            </span>
            <div className="p-3 bg-bg-secondary border border-border-subtle text-text-primary break-all">
              {diagnostic.audit_hash}
            </div>
          </div>

          <div>
            <span className="text-text-tertiary block mb-1 uppercase">
              IMMUTABLE DIAGNOSTIC JSON PAYLOAD:
            </span>
            <pre className="p-3 bg-bg-secondary border border-border-subtle text-text-secondary overflow-x-auto max-h-64 text-[11px] leading-relaxed">
              {JSON.stringify(diagnostic, null, 2)}
            </pre>
          </div>

          <div className="text-[11px] text-text-tertiary leading-relaxed pt-2">
            Every score, precedence weight, and verdict produced by Kairos is cryptographically locked to the exact market tick data and filing timestamp.
          </div>
        </div>
      </Modal>
    </>
  );
}
