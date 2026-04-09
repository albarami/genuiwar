"use client";

import { useCallback, useRef, useState, type DragEvent } from "react";

interface Props {
  onUpload: (file: File) => void;
  uploading: boolean;
}

export function FileUploader({ onUpload, uploading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFile = useCallback(
    (file: File) => {
      if (!uploading) onUpload(file);
    },
    [onUpload, uploading]
  );

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={`flex cursor-pointer items-center justify-center rounded-lg border-2 border-dashed p-4 text-sm transition-colors ${
        dragOver
          ? "border-blue-400 bg-blue-50 text-blue-600"
          : "border-gray-300 text-gray-500 hover:border-blue-400 hover:text-blue-600"
      }`}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
      }}
      data-testid="file-uploader"
    >
      {uploading ? "Uploading..." : "Drop file or click to upload"}
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        onChange={handleChange}
        disabled={uploading}
      />
    </div>
  );
}
