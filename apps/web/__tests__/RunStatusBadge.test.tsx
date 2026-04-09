import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { RunStatusBadge } from "../src/components/run/RunStatusBadge";

describe("RunStatusBadge", () => {
  it("renders completed status", () => {
    render(<RunStatusBadge status="completed" mode="fresh" />);
    expect(screen.getByTestId("run-status-badge")).toHaveTextContent("completed");
    expect(screen.getByTestId("run-status-badge")).toHaveTextContent("fresh run");
  });

  it("renders failed status", () => {
    render(<RunStatusBadge status="failed" mode="hybrid" />);
    expect(screen.getByTestId("run-status-badge")).toHaveTextContent("failed");
  });

  it("renders clarification status", () => {
    render(<RunStatusBadge status="waiting_for_clarification" mode="fresh" />);
    expect(screen.getByTestId("run-status-badge")).toHaveTextContent("waiting_for_clarification");
  });
});
