"use client";

import { useState, useCallback } from "react";
import { createRun } from "@/lib/api";
import type { RunResult, UIRunState } from "@/lib/types";

export function useRun() {
  const [state, setState] = useState<UIRunState>("empty");
  const [result, setResult] = useState<RunResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submitQuestion = useCallback(
    async (question: string, fileIds: string[]) => {
      setState("loading");
      setError(null);
      setResult(null);

      try {
        const res = await createRun(question, fileIds);
        setResult(res);

        if (res.run.status === "waiting_for_clarification") {
          setState("clarification");
        } else if (res.run.status === "failed") {
          setState("failed");
        } else {
          setState("answer");
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
        setState("error");
      }
    },
    []
  );

  return { state, result, error, submitQuestion };
}
