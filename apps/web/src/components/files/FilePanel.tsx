"use client";

import type { FileUploadResponse } from "@/lib/types";
import { FileListItem } from "./FileListItem";
import { FileUploader } from "./FileUploader";

interface Props {
  files: FileUploadResponse[];
  uploading: boolean;
  onUpload: (file: File) => void;
}

export function FilePanel({ files, uploading, onUpload }: Props) {
  return (
    <div className="flex h-full flex-col p-4" data-testid="file-panel">
      <h2 className="mb-4 text-sm font-semibold text-gray-500 uppercase">Files</h2>

      <div className="mb-4">
        <FileUploader onUpload={onUpload} uploading={uploading} />
      </div>

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
