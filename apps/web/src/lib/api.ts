/** Typed API client for GenUIWar backend. */

import type {
  CalculationResult,
  ClaimLedgerEntry,
  EvidenceBundle,
  EvidenceChunk,
  FileUploadResponse,
  RunEvent,
  RunResult,
  TraceResponse,
} from "./types";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${await res.text()}`);
  }
  return res.json() as Promise<T>;
}

// ── Health ──

export async function healthCheck(): Promise<{ status: string; service: string }> {
  return fetchJSON<{ status: string; service: string }>(`${BASE_URL}/health`);
}

// ── Files ──

export async function uploadFile(file: File): Promise<FileUploadResponse> {
  const form = new FormData();
  form.append("file", file);
  return fetchJSON<FileUploadResponse>(`${BASE_URL}/files/upload`, {
    method: "POST",
    body: form,
  });
}

export async function getFileMetadata(
  fileId: string
): Promise<FileUploadResponse> {
  return fetchJSON<FileUploadResponse>(`${BASE_URL}/files/${fileId}`);
}

// ── Runs ──

export async function createRun(
  question: string,
  fileIds: string[]
): Promise<RunResult> {
  return fetchJSON<RunResult>(`${BASE_URL}/runs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, file_ids: fileIds }),
  });
}

export async function getRun(runId: string): Promise<RunResult> {
  return fetchJSON<RunResult>(`${BASE_URL}/runs/${runId}`);
}

export async function getRunEvents(runId: string): Promise<RunEvent[]> {
  return fetchJSON<RunEvent[]>(`${BASE_URL}/runs/${runId}/events`);
}

export async function getRunClaims(
  runId: string
): Promise<ClaimLedgerEntry[]> {
  return fetchJSON<ClaimLedgerEntry[]>(`${BASE_URL}/runs/${runId}/claims`);
}

// ── Evidence ──

export async function getEvidenceChunk(
  chunkId: string
): Promise<EvidenceChunk> {
  return fetchJSON<EvidenceChunk>(`${BASE_URL}/evidence/chunk/${chunkId}`);
}

export async function getChunksForFile(
  fileId: string
): Promise<EvidenceChunk[]> {
  return fetchJSON<EvidenceChunk[]>(`${BASE_URL}/evidence/chunks/${fileId}`);
}

export interface RetrieveResponse {
  bundle: EvidenceBundle;
  chunk_count: number;
}

export async function retrieveEvidence(
  query: string,
  topK?: number
): Promise<RetrieveResponse> {
  return fetchJSON<RetrieveResponse>(`${BASE_URL}/evidence/retrieve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k: topK }),
  });
}

export async function getBundle(bundleId: string): Promise<EvidenceBundle> {
  return fetchJSON<EvidenceBundle>(`${BASE_URL}/evidence/bundle/${bundleId}`);
}

// ── Calculations ──

export async function executeCalculation(
  operation: string,
  inputs: Record<string, unknown>,
  options?: {
    inputUnits?: Record<string, string>;
    outputUnit?: string;
    evidenceRefs?: string[];
  }
): Promise<CalculationResult> {
  return fetchJSON<CalculationResult>(`${BASE_URL}/calculations/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      operation,
      inputs,
      input_units: options?.inputUnits ?? {},
      output_unit: options?.outputUnit ?? null,
      evidence_refs: options?.evidenceRefs ?? [],
    }),
  });
}

export async function getCalculation(
  calcId: string
): Promise<CalculationResult> {
  return fetchJSON<CalculationResult>(`${BASE_URL}/calculations/${calcId}`);
}

export async function getCalculationTrace(
  calcId: string
): Promise<TraceResponse> {
  return fetchJSON<TraceResponse>(`${BASE_URL}/calculations/${calcId}/trace`);
}
