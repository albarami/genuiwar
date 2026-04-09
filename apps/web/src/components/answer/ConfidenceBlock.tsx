import type { BlockProps } from "./BlockRegistry";

export function ConfidenceBlock({ block }: BlockProps) {
  return (
    <div className="rounded-lg border border-amber-200 bg-amber-50 p-4" data-testid="block-confidence">
      <h4 className="mb-1 text-xs font-semibold text-amber-600 uppercase">Confidence</h4>
      <p className="text-sm text-gray-700">{block.content}</p>
    </div>
  );
}
