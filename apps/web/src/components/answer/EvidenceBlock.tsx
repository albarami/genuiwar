import type { BlockProps } from "./BlockRegistry";

export function EvidenceBlock({ block, onOpenDrawer }: BlockProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4" data-testid="block-evidence">
      <h4 className="mb-1 text-xs font-semibold text-gray-500 uppercase">Evidence</h4>
      <p className="text-sm text-gray-700">{block.content}</p>
      {block.claim_ids.length > 0 && (
        <button
          onClick={() => onOpenDrawer("evidence", block.claim_ids[0])}
          className="mt-2 text-xs text-blue-600 hover:underline"
        >
          View evidence details
        </button>
      )}
    </div>
  );
}
