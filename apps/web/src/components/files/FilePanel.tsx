"use client";

import type { FileUploadResponse } from "@/lib/types";
import { FileListItem } from "./FileListItem";

interface Props {
  files: FileUploadResponse[];
  uploading: boolean;
  onUpload: (file: File) => void;
}

export function FilePanel({ files, uploading, onUpload }: Props) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onUpload(file);
  };

  return (
    <div className="flex h-full flex-col p-4" data-testid="file-panel">
      <h2 className="mb-4 text-sm font-semibold text-gray-500 uppercase">Files</h2>

      <label className="mb-4 flex cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-4 text-sm text-gray-500 hover:border-blue-400 hover:text-blue-600">
        {uploading ? "Uploading..." : "Upload file"}
        <input type="file" className="hidden" onChange={handleChange} disabled={uploading} />
      </label>

      {files.length === 0 ? (
        <p className="text-sm text-gray-400" data-testid="file-panel-empty">No files uploaded</p>
      ) : (
        <ul className="space-y-2">
          {files.map((f) => (
            <FileListItem key={f.file_document.file_id} file={f} />
          ))}
        </ul>
      )}
    </div>
  );
}
