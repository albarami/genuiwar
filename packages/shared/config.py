"""Application configuration loaded from environment variables.

Follows the .env.example contract. Every variable in .env.example should have
a corresponding field here. Grouped by concern for readability.
"""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Full application settings matching the .env.example contract."""

    # ── Core ──
    app_env: str = "development"
    app_name: str = "genuiwar"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    web_host: str = "0.0.0.0"
    web_port: int = 3000
    log_level: str = "INFO"

    # ── Azure OpenAI ──
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_api_version: str = "2025-03-01-preview"
    azure_openai_chat_deployment: str = ""
    azure_openai_embedding_deployment: str = ""
    azure_openai_reasoning_deployment: str = ""
    azure_openai_responses_model_hint: str = "gpt-5.4"
    azure_openai_enable_reasoning: bool = True
    azure_openai_enable_streaming: bool = True
    azure_openai_timeout_seconds: int = 120

    # ── Database ──
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/genuiwar"
    database_echo: bool = False
    test_database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/genuiwar_test"

    # ── Redis ──
    redis_url: str = "redis://localhost:6379/0"
    queue_backend: str = "redis"
    cache_backend: str = "redis"

    # ── Storage ──
    local_storage_root: str = "./data"
    uploads_dir: str = "./data/uploads"
    parsed_dir: str = "./data/parsed"
    artifacts_dir: str = "./data/artifacts"
    eval_data_dir: str = "./data/evaluation"
    synthetic_data_dir: str = "./data/synthetic"

    # ── Retrieval ──
    retrieval_backend: str = "local"
    embedding_dimensions: int = 3072
    chunk_size: int = 1200
    chunk_overlap: int = 200
    top_k_default: int = 8
    top_k_max: int = 20

    # ── Azure Search (optional, for later adapter) ──
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""
    azure_search_index_name: str = ""
    azure_search_semantic_config: str = ""

    # ── Worker ──
    worker_enabled: bool = True
    worker_concurrency: int = 4
    worker_poll_interval_seconds: int = 2

    # ── Auth ──
    auth_mode: str = "local_dev"
    dev_admin_email: str = "admin@example.com"
    dev_admin_password: str = "change-me"

    # ── Feature flags ──
    enable_file_uploads: bool = True
    enable_run_reuse: bool = True
    enable_hybrid_runs: bool = True
    enable_fresh_deep_runs: bool = True
    enable_live_event_stream: bool = True
    enable_debate_trace: bool = True
    enable_evidence_drawer: bool = True
    enable_calculation_trace: bool = True
    enable_clarification_questions: bool = True
    enable_adjudication_gate: bool = True
    enable_synthetic_data: bool = True
    enable_evaluation_harness: bool = True

    # ── Governance ──
    no_free_facts: bool = True
    require_citations: bool = True
    require_calculation_trace_for_numbers: bool = True
    require_confidence_grades: bool = True
    allow_question_clarification: bool = True
    allow_low_confidence_finals: bool = False

    # ── Run limits ──
    max_run_seconds: int = 600
    max_agent_steps_per_run: int = 100
    max_debate_rounds: int = 3
    max_clarification_questions: int = 3
    run_reuse_similarity_threshold: float = 0.88

    # ── UI ──
    stream_transport: str = "sse"
    ui_mode: str = "generative"
    show_agent_events: bool = True
    show_debate_events: bool = True
    show_adjudication_events: bool = True

    # ── Logging ──
    enable_structured_logging: bool = True
    enable_audit_logging: bool = True
    enable_run_event_logging: bool = True
    sentry_dsn: str = ""

    # ── Synthetic / Test ──
    generate_synthetic_fixtures: bool = True
    synthetic_data_seed: int = 42

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


def get_settings() -> AppSettings:
    """Factory for application settings; call once at startup."""
    return AppSettings()
