"""Shared enumerations for the GenUIWar schema layer."""

from enum import StrEnum


class RunCategory(StrEnum):
    DOCUMENT_PREPARATION = "document_preparation"
    BACKGROUND_ANALYSIS = "background_analysis"
    QUESTION_ANSWERING = "question_answering"
    TARGETED_FOLLOWUP = "targeted_followup"
    DEEP_RERUN = "deep_rerun"
    CLARIFICATION_REQUIRED = "clarification_required"


class RunMode(StrEnum):
    REUSE = "reuse"
    HYBRID = "hybrid"
    FRESH = "fresh"


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_FOR_CLARIFICATION = "waiting_for_clarification"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EventGroup(StrEnum):
    RUN_LIFECYCLE = "run_lifecycle"
    INGESTION = "ingestion"
    LINKING = "linking"
    RETRIEVAL = "retrieval"
    ANALYSIS = "analysis"
    CALCULATION = "calculation"
    CHALLENGE = "challenge"
    ADJUDICATION = "adjudication"
    CLARIFICATION = "clarification"
    ANSWER_RENDERING = "answer_rendering"


class ClaimType(StrEnum):
    DIRECT = "direct"
    DERIVED = "derived"
    MODEL_BASED = "model_based"


class SupportStatus(StrEnum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    UNSUPPORTED = "unsupported"
    NEEDS_CLARIFICATION = "needs_clarification"


class ConfidenceGrade(StrEnum):
    HIGH = "high"
    MODERATE = "moderate"
    EMERGING = "emerging"
    LOW = "low"
    UNRESOLVED = "unresolved"


class Materiality(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AdjudicationStatus(StrEnum):
    APPROVED = "approved"
    DOWNGRADED = "downgraded"
    REJECTED = "rejected"
    PENDING = "pending"


class ChallengeFlag(StrEnum):
    MISSING_EVIDENCE = "missing_evidence"
    MISSING_CALCULATION_TRACE = "missing_calculation_trace"
    DENOMINATOR_UNCLEAR = "denominator_unclear"
    SCOPE_OVERREACH = "scope_overreach"
    FALSE_PRECISION = "false_precision"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    WEAK_INTERPRETATION = "weak_interpretation"
    SCHEMA_MAPPING_UNCLEAR = "schema_mapping_unclear"
    TIME_WINDOW_UNCLEAR = "time_window_unclear"
    CLAIM_TOO_BROAD = "claim_too_broad"
    NEEDS_USER_CLARIFICATION = "needs_user_clarification"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class FileType(StrEnum):
    DOCX = "docx"
    PDF = "pdf"
    PPTX = "pptx"
    XLSX = "xlsx"
    CSV = "csv"
