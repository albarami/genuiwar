import type { BlockProps } from "./BlockRegistry";

export function CalculationBlock({ block, onOpenDrawer }: BlockProps) {
  return (
    <div className="rounded-lg border border-green-200 bg-green-50 p-4" data-testid="block-calculation">
      <h4 className="mb-1 text-xs font-semibold text-green-600 uppercase">Calculation</h4>
      <p className="text-sm text-gray-700">{block.content}</p>
      {block.claim_ids.length > 0 && (
        <button
          onClick={() => onOpenDrawer("calc", block.claim_ids[0])}
          className="mt-2 text-xs text-green-600 hover:underline"
        >
          View calculation trace
        </button>
      )}
    </div>
  );
}
