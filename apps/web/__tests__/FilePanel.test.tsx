import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { FilePanel } from "../src/components/files/FilePanel";
import type { FileUploadResponse } from "../src/lib/types";

const mockFile: FileUploadResponse = {
  file_document: {
    file_id: "f1",
    original_filename: "report.xlsx",
    file_type: "xlsx",
    file_size_bytes: 1024,
    storage_path: "/tmp/report.xlsx",
    content_hash: null,
    page_count: null,
    sheet_names: ["Sheet1"],
  },
  chunk_count: 5,
  parse_warnings: [],
  metadata: {},
};

describe("FilePanel", () => {
  it("shows empty state", () => {
    render(<FilePanel files={[]} uploading={false} onUpload={vi.fn()} />);
    expect(screen.getByTestId("file-panel-empty")).toHaveTextContent("No files uploaded");
  });

  it("shows files", () => {
    render(<FilePanel files={[mockFile]} uploading={false} onUpload={vi.fn()} />);
    expect(screen.getByText("report.xlsx")).toBeInTheDocument();
    expect(screen.getByText(/5 chunks/)).toBeInTheDocument();
  });

  it("shows uploading state", () => {
    render(<FilePanel files={[]} uploading={true} onUpload={vi.fn()} />);
    expect(screen.getByText("Uploading...")).toBeInTheDocument();
  });
});
