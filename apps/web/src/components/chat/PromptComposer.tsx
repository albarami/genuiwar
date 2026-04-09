"use client";

import { useState, type KeyboardEvent } from "react";

interface Props {
  onSubmit: (question: string) => void;
  disabled?: boolean;
}

export function PromptComposer({ onSubmit, disabled }: Props) {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSubmit(trimmed);
    setText("");
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about your data..."
        disabled={disabled}
        className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none disabled:opacity-50"
        data-testid="prompt-input"
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !text.trim()}
        className="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        data-testid="submit-button"
      >
        Send
      </button>
    </div>
  );
}
