"use client";

import { useEffect, useState } from "react";
import { getCalculationTrace } from "@/lib/api";
import type { TraceResponse } from "@/lib/types";

interface Props {
  calcId: string;
}

export function CalcTraceDrawer({ calcId }: Props) {
  const [trace, setTrace] = useState<TraceResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getCalculationTrace(calcId)
      .then(setTrace)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [calcId]);

  if (loading) return <div data-testid="calc-loading" className="text-sm text-gray-500">Loading trace...</div>;
  if (error) return <div data-testid="calc-error" className="text-sm text-red-600">Error: {error}</div>;
  if (!trace) return <div data-testid="calc-empty" className="text-sm text-gray-400">No trace found</div>;

  return (
    <div data-testid="calc-content" className="space-y-3">
      <div className="text-sm font-medium">{trace.operation}</div>
      {trace.output_unit && (
        <div className="text-xs text-gray-500">Unit: {trace.output_unit}</div>
      )}
      <ol className="space-y-1 text-sm">
        {trace.trace.map((step, i) => (
          <li key={i} className="rounded bg-gray-50 px-3 py-1.5 font-mono text-xs">{step}</li>
        ))}
      </ol>
    </div>
  );
}
