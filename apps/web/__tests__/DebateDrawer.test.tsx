import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { DebateDrawer } from "../src/components/drawers/DebateDrawer";
import type { ClaimLedgerEntry } from "../src/lib/types";

const mockClaim: ClaimLedgerEntry = {
  claim_id: "c1",
  run_id: "r1",
  claim_text: "Headcount increased by 5%",
  claim_type: "derived",
  support_status: "supported",
  confidence_grade: "moderate",
  materiality: "high",
  evidence_refs: ["e1"],
  calculation_result_ids: [],
  challenge_flags: ["weak_interpretation"],
  adjudication_status: "downgraded",
  adjudication_reason: "Downgraded due to weak interpretation",
  created_by_agent: "primary_analyst",
};

describe("DebateDrawer", () => {
  it("renders claim with adjudication status", () => {
    render(<DebateDrawer claims={[mockClaim]} />);
    expect(screen.getByTestId("debate-content")).toBeInTheDocument();
    expect(screen.getByText("downgraded")).toBeInTheDocument();
    expect(screen.getByText("Headcount increased by 5%")).toBeInTheDocument();
  });

  it("renders challenge flags", () => {
    render(<DebateDrawer claims={[mockClaim]} />);
    expect(screen.getByText("weak_interpretation")).toBeInTheDocument();
  });

  it("shows empty state", () => {
    render(<DebateDrawer claims={[]} />);
    expect(screen.getByTestId("debate-empty")).toBeInTheDocument();
  });
});
