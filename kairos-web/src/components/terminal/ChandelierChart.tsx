"use client";

import React, { useEffect, useRef, useState } from "react";
import { formatCurrency } from "@/lib/formatters";
import { createChart, ColorType, CrosshairMode, LineStyle, LineType, Time, CandlestickSeries, LineSeries } from "lightweight-charts";
import { ChartDataPoint } from "@/types/diagnostic";

interface ChandelierChartProps {
  symbol: string;
  currentPrice: number;
  stopPrice: number;
  targetPrice: number;
  chartData: ChartDataPoint[];
}

export function ChandelierChart({
  symbol,
  currentPrice,
  stopPrice,
  targetPrice,
  chartData,
}: ChandelierChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [timeframe, setTimeframe] = useState<"15m" | "1D" | "1W">("1D");

  useEffect(() => {
    if (!chartContainerRef.current) return;

    // 1. Create Chart
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#A3A3A3',
        fontFamily: 'JetBrains Mono, monospace',
      },
      grid: {
        vertLines: { visible: false },
        horzLines: { visible: false },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: {
          color: '#404040',
          width: 1,
          style: LineStyle.Dashed,
          labelBackgroundColor: '#1A1A1A',
        },
        horzLine: {
          color: '#404040',
          width: 1,
          style: LineStyle.Dashed,
          labelBackgroundColor: '#1A1A1A',
        },
      },
      rightPriceScale: {
        borderVisible: false,
      },
      timeScale: {
        borderVisible: false,
        timeVisible: true,
      },
    });

    // 2. Add Candlestick Series
    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#FFFFFF',
      downColor: '#111111',
      borderVisible: true,
      borderColor: '#737373',
      wickColor: '#737373',
      borderUpColor: '#FFFFFF',
      borderDownColor: '#737373',
      wickUpColor: '#FFFFFF',
      wickDownColor: '#737373',
    });

    // Sort and map the data for the chart
    const sortedData = [...chartData].sort((a, b) => a.time - b.time);
    const candleData = sortedData.map(d => ({
      time: d.time as Time,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }));
    
    if (candleData.length > 0) {
      candleSeries.setData(candleData);
    }

    // 3. Add Target Price Line (Horizontal)
    candleSeries.createPriceLine({
      price: targetPrice,
      color: '#9CA3AF',
      lineWidth: 1,
      lineStyle: LineStyle.Dashed,
      axisLabelVisible: true,
      title: 'TARGET',
    });

    // 4. Add Chandelier Stop Series (Step Line)
    const stopSeries = chart.addSeries(LineSeries, {
      color: '#D1D5DB',
      lineWidth: 2,
      lineType: LineType.WithSteps,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    });
    
    const stopData = sortedData.map(d => ({
      time: d.time as Time,
      value: d.stop,
    }));
    
    if (stopData.length > 0) {
      stopSeries.setData(stopData);
    }

    // Make chart fit container properly
    chart.timeScale().fitContent();

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [chartData, targetPrice]);

  return (
    <div className="w-full font-mono flex flex-col gap-6 py-4">
      {/* Chart Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-border-subtle">
        <div className="flex items-center gap-3">
          <span className="text-[10px] uppercase text-text-tertiary tracking-widest">
            Chandelier Volatility Ratchet
          </span>
          <span className="text-[10px] text-text-tertiary">
            {symbol} • {timeframe}
          </span>
        </div>

        {/* Timeframe Switcher */}
        <div className="flex items-center gap-1 border border-border-subtle bg-bg-primary p-0.5 text-[10px]">
          {(["15m", "1D", "1W"] as const).map((tf) => (
            <button
              key={tf}
              type="button"
              onClick={() => setTimeframe(tf)}
              className={`px-2 py-0.5 transition-colors ${
                timeframe === tf
                  ? "bg-grey-700 text-text-primary font-bold"
                  : "text-text-tertiary hover:text-text-secondary"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* TradingView Lightweight Charts Canvas Container */}
      <div className="relative w-full h-56 sm:h-64">
        <div ref={chartContainerRef} className="absolute inset-0" />

        {/* Floating Legend Badges */}
        <div className="absolute top-2 right-2 flex flex-col items-end gap-1 text-[10px] bg-bg-primary/90 border border-border-subtle p-2 pointer-events-none z-10">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-[#D1D5DB]" />
            <span className="text-text-secondary">CHANDELIER FLOOR: {formatCurrency(stopPrice)}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 border-t border-dashed border-[#9CA3AF]" />
            <span className="text-text-tertiary">TARGET: {formatCurrency(targetPrice)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
