import type { FileUploadResponse } from "@/lib/types";

interface Props {
  file: FileUploadResponse;
}

export function FileListItem({ file }: Props) {
  const doc = file.file_document;
  return (
    <li className="rounded border border-gray-200 p-2 text-sm">
      <div className="font-medium truncate">{doc.original_filename}</div>
      <div className="text-xs text-gray-500">
        {doc.file_type.toUpperCase()} &middot; {file.chunk_count} chunks
        {file.parse_warnings.length > 0 && (
          <span className="ml-1 text-amber-600">({file.parse_warnings.length} warnings)</span>
        )}
      </div>
    </li>
  );
}
