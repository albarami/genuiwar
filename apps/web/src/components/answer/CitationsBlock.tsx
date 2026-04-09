import type { BlockProps } from "./BlockRegistry";

export function CitationsBlock({ block }: BlockProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-gray-50 p-4" data-testid="block-citations">
      <h4 className="mb-1 text-xs font-semibold text-gray-500 uppercase">Citations</h4>
      <p className="text-sm text-gray-600">{block.content}</p>
    </div>
  );
}
