"use client";

import type { RunResult, UIRunState } from "@/lib/types";
import { PromptComposer } from "./PromptComposer";
import { MessageBubble } from "./MessageBubble";
import { RunStatusBadge } from "@/components/run/RunStatusBadge";
import { EventStream } from "@/components/run/EventStream";
import { AnswerRenderer } from "@/components/answer/AnswerRenderer";
import { ClarificationCard } from "@/components/clarification/ClarificationCard";
import { GovernanceFailurePanel } from "@/components/clarification/GovernanceFailurePanel";

interface Props {
  state: UIRunState;
  result: RunResult | null;
  error: string | null;
  fileIds: string[];
  onSubmit: (question: string, fileIds: string[]) => void;
  onOpenDrawer: (type: "evidence" | "debate" | "calc", id?: string) => void;
}

export function ChatThread({ state, result, error, fileIds, onSubmit, onOpenDrawer }: Props) {
  return (
    <div className="flex flex-1 flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {result?.run.question && (
          <MessageBubble role="user" content={result.run.question} />
        )}

        {state === "loading" && (
          <div className="flex items-center gap-2 text-gray-500">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />
            Running analysis...
          </div>
        )}

        {state === "answer" && result?.answer_payload && (
          <>
            <RunStatusBadge status={result.run.status} mode={result.run.run_mode} />
            <EventStream events={result.events} />
            <AnswerRenderer payload={result.answer_payload} onOpenDrawer={onOpenDrawer} />
          </>
        )}

        {state === "clarification" && result?.clarification_request && (
          <ClarificationCard request={result.clarification_request} />
        )}

        {state === "failed" && result && (
          <GovernanceFailurePanel events={result.events} status={result.run.status} />
        )}

        {state === "error" && error && (
          <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-red-800">{error}</div>
        )}
      </div>

      <div className="border-t border-gray-200 bg-white p-4">
        <PromptComposer onSubmit={(q) => onSubmit(q, fileIds)} disabled={state === "loading"} />
      </div>
    </div>
  );
}
