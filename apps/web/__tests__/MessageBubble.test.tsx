import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { MessageBubble } from "../src/components/chat/MessageBubble";

describe("MessageBubble", () => {
  it("renders user message", () => {
    render(<MessageBubble role="user" content="Hello" />);
    expect(screen.getByTestId("message-user")).toHaveTextContent("Hello");
  });

  it("renders assistant message", () => {
    render(<MessageBubble role="assistant" content="Analysis complete" />);
    expect(screen.getByTestId("message-assistant")).toHaveTextContent("Analysis complete");
  });
});
