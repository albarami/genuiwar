import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { AnswerRenderer } from "../src/components/answer/AnswerRenderer";
import type { FinalAnswerPayload } from "../src/lib/types";

const mockPayload: FinalAnswerPayload = {
  answer_id: "a1",
  run_id: "r1",
  blocks: [
    { block_type: "direct_answer", content: "Headcount is 1200", claim_ids: ["c1"] },
    { block_type: "confidence", content: "High confidence", claim_ids: ["c1"] },
    { block_type: "evidence", content: "Based on Q1 report", claim_ids: ["c1"] },
  ],
  approved_claim_ids: ["c1"],
  rejected_claim_ids: [],
  confidence_summary: "1 claim used",
  created_at: "2026-01-01T00:00:00Z",
};

describe("AnswerRenderer", () => {
  it("renders all block types", () => {
    render(<AnswerRenderer payload={mockPayload} onOpenDrawer={vi.fn()} />);
    expect(screen.getByTestId("block-direct_answer")).toBeInTheDocument();
    expect(screen.getByTestId("block-confidence")).toBeInTheDocument();
    expect(screen.getByTestId("block-evidence")).toBeInTheDocument();
  });

  it("shows confidence summary", () => {
    render(<AnswerRenderer payload={mockPayload} onOpenDrawer={vi.fn()} />);
    expect(screen.getByText("1 claim used")).toBeInTheDocument();
  });
});
