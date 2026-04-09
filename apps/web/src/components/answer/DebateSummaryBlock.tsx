import type { BlockProps } from "./BlockRegistry";

export function DebateSummaryBlock({ block, onOpenDrawer }: BlockProps) {
  return (
    <div className="rounded-lg border border-purple-200 bg-purple-50 p-4" data-testid="block-debate_summary">
      <h4 className="mb-1 text-xs font-semibold text-purple-600 uppercase">Debate Summary</h4>
      <p className="text-sm text-gray-700">{block.content}</p>
      <button
        onClick={() => onOpenDrawer("debate")}
        className="mt-2 text-xs text-purple-600 hover:underline"
      >
        View full debate
      </button>
    </div>
  );
}
