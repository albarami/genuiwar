import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { GovernanceFailurePanel } from "../src/components/clarification/GovernanceFailurePanel";
import type { RunEvent } from "../src/lib/types";

const violationEvent: RunEvent = {
  event_id: "ev1",
  run_id: "r1",
  event_index: 0,
  event_type: "adjudication.governance_violation",
  event_group: "adjudication",
  agent_name: null,
  status: "emitted",
  title: "Pre-compose governance violations detected",
  summary: null,
  payload: { violations: ["Claim c1 has status rejected"] },
  created_at: "2026-01-01T00:00:00Z",
  is_user_visible: true,
};

describe("GovernanceFailurePanel", () => {
  it("renders violation details", () => {
    render(<GovernanceFailurePanel events={[violationEvent]} status="failed" />);
    expect(screen.getByTestId("governance-failure")).toBeInTheDocument();
    expect(screen.getByText("Claim c1 has status rejected")).toBeInTheDocument();
  });

  it("renders generic message when no violation events", () => {
    render(<GovernanceFailurePanel events={[]} status="failed" />);
    expect(screen.getByText(/blocked by governance/)).toBeInTheDocument();
  });
});
