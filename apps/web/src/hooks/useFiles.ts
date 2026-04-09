"use client";

import { useState, useCallback } from "react";
import { uploadFile } from "@/lib/api";
import type { FileUploadResponse } from "@/lib/types";

export function useFiles() {
  const [files, setFiles] = useState<FileUploadResponse[]>([]);
  const [uploading, setUploading] = useState(false);

  const upload = useCallback(async (file: File) => {
    setUploading(true);
    try {
      const res = await uploadFile(file);
      setFiles((prev) => [...prev, res]);
      return res;
    } finally {
      setUploading(false);
    }
  }, []);

  const fileIds = files.map((f) => f.file_document.file_id);

  return { files, fileIds, uploading, upload };
}
