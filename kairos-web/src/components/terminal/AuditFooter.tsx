"use client";

import React, { useState } from "react";
import { Copy, Check, ShieldCheck } from "lucide-react";
import { Modal } from "@/components/ui/Modal";
import { truncateHash } from "@/lib/formatters";
import { DiagnosticOutput } from "@/types/diagnostic";

interface AuditFooterProps {
  diagnostic: DiagnosticOutput;
}

export function AuditFooter({ diagnostic }: AuditFooterProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(diagnostic.audit_hash);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <>
      <footer className="w-full border-t border-border-subtle bg-bg-secondary/40 px-4 sm:px-8 py-6 font-mono text-xs text-text-secondary">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* SEBI Compliance Statement */}
          <div className="max-w-xl text-[11px] leading-relaxed text-text-secondary">
            <span className="text-text-primary font-bold mr-1">// REGULATORY NOTICE:</span>
            Kairos is a deterministic mathematical diagnostic sandbox. Not SEBI registered investment advice. Historical algorithms do not guarantee future returns.
          </div>

          {/* Cryptographic SHA-256 Verification Action */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 border border-border-subtle bg-bg-primary px-3 py-1.5 text-[11px]">
              <ShieldCheck className="w-3.5 h-3.5 text-text-secondary" />
              <span className="text-text-tertiary">HASH:</span>
              <span className="text-text-primary font-bold">
                {truncateHash(diagnostic.audit_hash, 8, 8)}
              </span>
            </div>

            <button
              type="button"
              onClick={handleCopy}
              className="p-1.5 border border-border-subtle bg-bg-secondary hover:border-border-active transition-colors text-text-secondary hover:text-text-primary"
              title="Copy SHA-256 Hash"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
            </button>

            <button
              type="button"
              onClick={() => setIsModalOpen(true)}
              className="px-2.5 py-1.5 border border-border-subtle bg-bg-secondary hover:border-border-active transition-colors text-[11px] text-text-primary font-bold"
            >
              INSPECT JSON
            </button>
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
