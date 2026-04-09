import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { EvidenceDrawer } from "../src/components/drawers/EvidenceDrawer";

const mockChunk = {
  chunk_id: "ch1",
  file_id: "f1",
  content: "Total headcount: 1200",
  content_type: "text",
  citation_anchor: {
    file_id: "f1",
    page: 3,
    section: "Summary",
    row_range: null,
    sheet_name: null,
  },
  metadata: {},
  created_at: "2026-01-01T00:00:00Z",
};

vi.mock("../src/lib/api", () => ({
  getEvidenceChunk: vi.fn(),
}));

import { getEvidenceChunk } from "../src/lib/api";
const mockedGet = vi.mocked(getEvidenceChunk);

describe("EvidenceDrawer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows loading state", () => {
    mockedGet.mockReturnValue(new Promise(() => {}));
    render(<EvidenceDrawer chunkId="ch1" />);
    expect(screen.getByTestId("evidence-loading")).toBeInTheDocument();
  });

  it("shows error state", async () => {
    mockedGet.mockRejectedValue(new Error("Network failure"));
    render(<EvidenceDrawer chunkId="ch1" />);
    await waitFor(() => {
      expect(screen.getByTestId("evidence-error")).toBeInTheDocument();
    });
    expect(screen.getByTestId("evidence-error")).toHaveTextContent("Network failure");
  });

  it("shows content state", async () => {
    mockedGet.mockResolvedValue(mockChunk);
    render(<EvidenceDrawer chunkId="ch1" />);
    await waitFor(() => {
      expect(screen.getByTestId("evidence-content")).toBeInTheDocument();
    });
    expect(screen.getByText("Total headcount: 1200")).toBeInTheDocument();
    expect(screen.getByText("Page: 3")).toBeInTheDocument();
    expect(screen.getByText("Section: Summary")).toBeInTheDocument();
  });
});
