/** TypeScript types mirroring backend Pydantic models. Manually maintained. */

export type RunStatus =
  | "queued"
  | "running"
  | "waiting_for_clarification"
  | "completed"
  | "failed"
  | "cancelled";

export type RunMode = "reuse" | "hybrid" | "fresh";

export type EventGroup =
  | "run_lifecycle"
  | "ingestion"
  | "linking"
  | "retrieval"
  | "analysis"
  | "calculation"
  | "challenge"
  | "adjudication"
  | "clarification"
  | "answer_rendering";

export type AdjudicationStatus = "approved" | "downgraded" | "rejected" | "pending";

export type AnswerBlockType =
  | "direct_answer"
  | "evidence"
  | "confidence"
  | "debate_summary"
  | "calculation"
  | "citations";

export interface Run {
  run_id: string;
  conversation_id: string;
  trigger_message_id: string | null;
  parent_run_id: string | null;
  run_category: string;
  run_mode: RunMode;
  status: RunStatus;
  scope: string | null;
  question: string | null;
  decision_reason: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface RunEvent {
  event_id: string;
  run_id: string;
  event_index: number;
  event_type: string;
  event_group: EventGroup;
  agent_name: string | null;
  status: string;
  title: string;
  summary: string | null;
  payload: Record<string, unknown>;
  created_at: string;
  is_user_visible: boolean;
}

export interface CitationAnchor {
  file_id: string;
  page: number | null;
  section: string | null;
  row_range: [number, number] | null;
  sheet_name: string | null;
}

export interface EvidenceChunk {
  chunk_id: string;
  file_id: string;
  content: string;
  content_type: string;
  citation_anchor: CitationAnchor;
  metadata: Record<string, string>;
  created_at: string;
}

export interface EvidenceBundle {
  bundle_id: string;
  query: string;
  chunks: EvidenceChunk[];
  file_ids: string[];
  total_candidates: number;
  created_at: string;
}

export interface ClaimLedgerEntry {
  claim_id: string;
  run_id: string;
  parent_claim_id: string | null;
  claim_text: string;
  claim_type: string;
  claim_scope: string | null;
  support_status: string;
  confidence_grade: string;
  materiality: string;
  evidence_refs: string[];
  calculation_result_ids: string[];
  assumptions: string[];
  challenge_flags: string[];
  adjudication_status: AdjudicationStatus;
  adjudication_reason: string | null;
  created_by_agent: string | null;
  created_at: string;
}

export interface AnswerBlock {
  block_type: AnswerBlockType;
  content: string;
  claim_ids: string[];
}

export interface FinalAnswerPayload {
  answer_id: string;
  run_id: string;
  blocks: AnswerBlock[];
  approved_claim_ids: string[];
  rejected_claim_ids: string[];
  confidence_summary: string;
  created_at: string;
}

export interface ClarificationRequest {
  clarification_id: string;
  run_id: string;
  question: string;
  reason: string;
  options: string[];
  response: string | null;
  responded_at: string | null;
  created_at: string;
}

export interface RunResult {
  run: Run;
  events: RunEvent[];
  claims: ClaimLedgerEntry[];
  answer_payload: FinalAnswerPayload | null;
  clarification_request: ClarificationRequest | null;
}

export interface FileDocument {
  file_id: string;
  original_filename: string;
  file_type: string;
  file_size_bytes: number;
  storage_path: string;
  content_hash: string | null;
  page_count: number | null;
  sheet_names: string[] | null;
  detected_schema: Record<string, unknown> | null;
  uploaded_at: string;
}

export interface FileUploadResponse {
  file_document: FileDocument;
  chunk_count: number;
  parse_warnings: string[];
  metadata: Record<string, unknown>;
}

export interface TraceResponse {
  calculation_id: string;
  operation: string;
  trace: string[];
  output_unit: string | null;
}

export interface CalculationResult {
  calculation_id: string;
  run_id: string;
  operation: string;
  inputs: Record<string, unknown>;
  result: unknown;
  trace: string[];
  input_units: Record<string, string>;
  output_unit: string | null;
  evidence_refs: string[];
  created_at: string;
}

/** UI state for the run lifecycle */
export type UIRunState = "empty" | "loading" | "answer" | "clarification" | "failed" | "error";
