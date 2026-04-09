import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { EventStream } from "../src/components/run/EventStream";
import type { RunEvent } from "../src/lib/types";

const mockEvents: RunEvent[] = [
  {
    event_id: "e1",
    run_id: "r1",
    event_index: 0,
    event_type: "run.started",
    event_group: "run_lifecycle",
    agent_name: null,
    status: "emitted",
    title: "Run started",
    summary: null,
    payload: {},
    created_at: "2026-01-01T00:00:00Z",
    is_user_visible: true,
  },
  {
    event_id: "e2",
    run_id: "r1",
    event_index: 1,
    event_type: "answer.completed",
    event_group: "answer_rendering",
    agent_name: "composer",
    status: "emitted",
    title: "Answer assembled",
    summary: null,
    payload: {},
    created_at: "2026-01-01T00:00:01Z",
    is_user_visible: true,
  },
];

describe("EventStream", () => {
  it("renders visible events", () => {
    render(<EventStream events={mockEvents} />);
    expect(screen.getByTestId("event-stream")).toBeInTheDocument();
    expect(screen.getByText("Run started")).toBeInTheDocument();
    expect(screen.getByText("Answer assembled")).toBeInTheDocument();
  });

  it("renders nothing for empty events", () => {
    const { container } = render(<EventStream events={[]} />);
    expect(container.firstChild).toBeNull();
  });
});
