/** Typed API client for GenUIWar backend. */

import type {
  CalculationResult,
  EvidenceChunk,
  FileUploadResponse,
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

export async function uploadFile(file: File): Promise<FileUploadResponse> {
  const form = new FormData();
  form.append("file", file);
  return fetchJSON<FileUploadResponse>(`${BASE_URL}/files/upload`, {
    method: "POST",
    body: form,
  });
}

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

export async function getEvidenceChunk(
  chunkId: string
): Promise<EvidenceChunk> {
  return fetchJSON<EvidenceChunk>(`${BASE_URL}/evidence/chunk/${chunkId}`);
}

export async function getCalculationTrace(
  calcId: string
): Promise<TraceResponse> {
  return fetchJSON<TraceResponse>(`${BASE_URL}/calculations/${calcId}/trace`);
}

export async function getCalculation(
  calcId: string
): Promise<CalculationResult> {
  return fetchJSON<CalculationResult>(`${BASE_URL}/calculations/${calcId}`);
}
