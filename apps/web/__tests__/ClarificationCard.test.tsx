import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ClarificationCard } from "../src/components/clarification/ClarificationCard";

describe("ClarificationCard", () => {
  it("renders question and options", () => {
    render(
      <ClarificationCard
        request={{
          clarification_id: "c1",
          run_id: "r1",
          question: "Which column is the primary identifier?",
          reason: "Ambiguous schema",
          options: ["Column A", "Column B"],
        }}
      />
    );
    expect(screen.getByTestId("clarification-card")).toBeInTheDocument();
    expect(screen.getByText("Which column is the primary identifier?")).toBeInTheDocument();
    expect(screen.getByText("Column A")).toBeInTheDocument();
    expect(screen.getByText("Column B")).toBeInTheDocument();
  });

  it("shows reason", () => {
    render(
      <ClarificationCard
        request={{
          clarification_id: "c1",
          run_id: "r1",
          question: "Q?",
          reason: "Denominator unclear",
          options: [],
        }}
      />
    );
    expect(screen.getByText(/Denominator unclear/)).toBeInTheDocument();
  });
});
