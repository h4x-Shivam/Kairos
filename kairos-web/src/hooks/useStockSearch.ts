"use client";

import { useState, useEffect } from "react";
import { searchStocks } from "@/lib/api";
import { StockSearchResult } from "@/types/diagnostic";

export function useStockSearch(initialQuery = "") {
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState<StockSearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setIsLoading(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await searchStocks(query.trim());
        setResults(data);
      } catch (err) {
        setError("Failed to fetch stock search results.");
      } finally {
        setIsLoading(false);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [query]);

  return {
    query,
    setQuery,
    results,
    isLoading,
    error,
  };
}
