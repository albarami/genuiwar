import type { BlockProps } from "./BlockRegistry";

export function DirectAnswerBlock({ block }: BlockProps) {
  return (
    <div className="rounded-lg border border-blue-200 bg-blue-50 p-4" data-testid="block-direct_answer">
      <h4 className="mb-1 text-xs font-semibold text-blue-600 uppercase">Answer</h4>
      <p className="text-gray-900">{block.content}</p>
    </div>
  );
}
