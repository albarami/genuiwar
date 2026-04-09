"use client";

import { useEffect, useState } from "react";
import { getEvidenceChunk } from "@/lib/api";
import type { EvidenceChunk } from "@/lib/types";

interface Props {
  chunkId: string;
}

export function EvidenceDrawer({ chunkId }: Props) {
  const [chunk, setChunk] = useState<EvidenceChunk | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getEvidenceChunk(chunkId)
      .then(setChunk)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [chunkId]);

  if (loading) return <div data-testid="evidence-loading" className="text-sm text-gray-500">Loading evidence...</div>;
  if (error) return <div data-testid="evidence-error" className="text-sm text-red-600">Error: {error}</div>;
  if (!chunk) return <div data-testid="evidence-empty" className="text-sm text-gray-400">No evidence found</div>;

  const anchor = chunk.citation_anchor;

  return (
    <div data-testid="evidence-content" className="space-y-3">
      <div className="rounded border border-gray-200 bg-gray-50 p-3 text-sm">{chunk.content}</div>
      <div className="text-xs text-gray-500 space-y-1">
        <div>Type: {chunk.content_type}</div>
        {anchor.page && <div>Page: {anchor.page}</div>}
        {anchor.section && <div>Section: {anchor.section}</div>}
        {anchor.sheet_name && <div>Sheet: {anchor.sheet_name}</div>}
        {anchor.row_range && <div>Rows: {anchor.row_range[0]}–{anchor.row_range[1]}</div>}
      </div>
    </div>
  );
}
