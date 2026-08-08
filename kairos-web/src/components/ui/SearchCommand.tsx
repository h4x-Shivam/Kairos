"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Search, Loader2 } from "lucide-react";
import { searchStocks } from "@/lib/api";
import { StockSearchResult } from "@/types/diagnostic";

interface SearchCommandProps {
  onSelectStock?: (stock: StockSearchResult) => void;
  className?: string;
  autoFocus?: boolean;
}

const POPULAR_TICKERS = ["TATAMOTORS", "RELIANCE", "INFY", "HDFCBANK", "SUZLON"];

export function SearchCommand({
  onSelectStock,
  className = "",
  autoFocus = false,
}: SearchCommandProps) {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<StockSearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  // Debounced search query
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setIsLoading(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      const res = await searchStocks(query.trim());
      setResults(res);
      setIsLoading(false);
      setIsOpen(true);
      setSelectedIndex(0);
    }, 180);

    return () => clearTimeout(timer);
  }, [query]);

  // Click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (stock: StockSearchResult) => {
    setIsOpen(false);
    setQuery(stock.symbol);
    if (onSelectStock) {
      onSelectStock(stock);
    } else {
      router.push(`/diagnostic/${encodeURIComponent(stock.symbol)}`);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % (results.length || 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + results.length) % (results.length || 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (results.length > 0 && selectedIndex < results.length) {
        handleSelect(results[selectedIndex]);
      } else if (query.trim()) {
        const symbol = query.trim().toUpperCase();
        handleSelect({
          symbol,
          company_name: symbol,
          exchange: "NSE",
          market_cap_bucket: "LARGE_CAP",
          sector: "EQUITY",
        });
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  return (
    <div ref={containerRef} className={`relative w-full max-w-2xl ${className}`}>
      {/* Search Input Box */}
      <div className="flex items-center w-full bg-bg-secondary border border-border-subtle focus-within:border-border-active transition-all px-4 py-3.5">
        <span className="font-mono text-text-tertiary mr-3 text-sm select-none">$</span>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.trim() && setIsOpen(true)}
          onKeyDown={handleKeyDown}
          autoFocus={autoFocus}
          placeholder="Search NSE/BSE ticker (e.g. TATAMOTORS, RELIANCE, INFY)..."
          className="w-full bg-transparent font-mono text-sm text-text-primary placeholder:text-text-tertiary focus:outline-none"
        />
        {isLoading ? (
          <Loader2 className="w-4 h-4 text-text-secondary animate-spin" />
        ) : (
          <div className="flex items-center gap-1">
            <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono border border-border-subtle bg-bg-tertiary text-text-tertiary">
              ENTER
            </kbd>
          </div>
        )}
      </div>

      {/* Autocomplete Dropdown */}
      {isOpen && results.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-bg-secondary border border-border-subtle divide-y divide-border-subtle z-50 shadow-2xl max-h-72 overflow-y-auto">
          {results.map((item, idx) => (
            <button
              key={`${item.symbol}-${idx}`}
              type="button"
              onClick={() => handleSelect(item)}
              onMouseEnter={() => setSelectedIndex(idx)}
              className={`w-full text-left px-4 py-3 flex items-center justify-between transition-colors ${
                selectedIndex === idx ? "bg-bg-tertiary" : "hover:bg-bg-tertiary"
              }`}
            >
              <div className="flex items-baseline gap-3">
                <span className="font-mono font-bold text-text-primary text-sm">
                  {item.symbol}
                </span>
                <span className="text-xs text-text-secondary truncate max-w-xs sm:max-w-md">
                  {item.company_name}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono px-1.5 py-0.5 border border-border-subtle text-text-tertiary bg-bg-primary">
                  {item.market_cap_bucket}
                </span>
                <span className="text-[10px] font-mono text-text-tertiary">
                  {item.exchange}
                </span>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Quick Select Watchlist Pills */}
      <div className="mt-3 flex items-center gap-2 flex-wrap text-xs font-mono text-text-tertiary">
        <span className="text-[11px] text-text-tertiary uppercase">// WATCHLIST:</span>
        {POPULAR_TICKERS.map((ticker) => (
          <button
            key={ticker}
            type="button"
            onClick={() =>
              handleSelect({
                symbol: ticker,
                company_name: ticker,
                exchange: "NSE",
                market_cap_bucket: "LARGE_CAP",
                sector: "EQUITY",
              })
            }
            className="px-2 py-0.5 border border-border-subtle bg-bg-secondary text-text-secondary hover:text-text-primary hover:border-border-active transition-colors text-[11px]"
          >
            {ticker}
          </button>
        ))}
      </div>
    </div>
  );
}
