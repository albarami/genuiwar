"""LLM adapter layer — Azure OpenAI + Deterministic implementations."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TypeVar

import httpx
from pydantic import BaseModel

from packages.shared.config import get_settings

T = TypeVar("T", bound=BaseModel)


class LLMAdapter(ABC):
    """Abstract contract for LLM backends."""

    @abstractmethod
    def complete_text(self, system_prompt: str, user_content: str) -> str:
        """Return raw text completion."""

    @abstractmethod
    def complete_structured(
        self,
        system_prompt: str,
        user_content: str,
        response_model: type[T],
    ) -> T:
        """Return a schema-validated Pydantic model from the LLM response."""


class AzureOpenAIAdapter(LLMAdapter):
    """Azure OpenAI-backed adapter for production use."""

    def __init__(self) -> None:
        s = get_settings()
        self._endpoint = s.azure_openai_endpoint.rstrip("/")
        self._api_key = s.azure_openai_api_key
        self._deployment = s.azure_openai_chat_deployment
        self._api_version = s.azure_openai_api_version

    def _call(self, system_prompt: str, user_content: str) -> str:
        url = (
            f"{self._endpoint}/openai/deployments/{self._deployment}"
            f"/chat/completions?api-version={self._api_version}"
        )
        resp = httpx.post(
            url,
            headers={"api-key": self._api_key, "Content-Type": "application/json"},
            json={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                "temperature": 0.1,
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]  # type: ignore[no-any-return]

    def complete_text(self, system_prompt: str, user_content: str) -> str:
        return self._call(system_prompt, user_content)

    def complete_structured(
        self,
        system_prompt: str,
        user_content: str,
        response_model: type[T],
    ) -> T:
        enriched_prompt = (
            f"{system_prompt}\n\n"
            f"Respond ONLY with valid JSON matching this schema:\n"
            f"{response_model.model_json_schema()}"
        )
        raw = self._call(enriched_prompt, user_content)
        data = json.loads(raw)
        return response_model.model_validate(data)


class DeterministicAdapter(LLMAdapter):
    """Rule-based adapter for tests and local dev — no LLM calls."""

    def complete_text(self, system_prompt: str, user_content: str) -> str:
        return f"[deterministic response to: {user_content[:80]}]"

    def complete_structured(
        self,
        system_prompt: str,
        user_content: str,
        response_model: type[T],
    ) -> T:
        return response_model.model_validate(
            response_model.model_json_schema().get("examples", [{}])[0]
            if response_model.model_json_schema().get("examples")
            else {}
        )


def get_llm_adapter() -> LLMAdapter:
    """Factory: reads AGENT_MODE config to select adapter."""
    mode = get_settings().agent_mode
    if mode == "azure":
        return AzureOpenAIAdapter()
    return DeterministicAdapter()
