import type { ClarificationRequest } from "@/lib/types";

interface Props {
  request: ClarificationRequest;
}

export function ClarificationCard({ request }: Props) {
  return (
    <div className="rounded-lg border-2 border-amber-300 bg-amber-50 p-4" data-testid="clarification-card">
      <h4 className="mb-2 text-sm font-semibold text-amber-700">Clarification Needed</h4>
      <p className="mb-3 text-sm text-gray-800">{request.question}</p>
      <p className="mb-3 text-xs text-gray-500">Reason: {request.reason}</p>
      {request.options.length > 0 && (
        <div className="space-y-2">
          {request.options.map((opt, i) => (
            <button
              key={i}
              className="block w-full rounded border border-amber-300 bg-white px-3 py-2 text-left text-sm hover:bg-amber-100"
            >
              {opt}
            </button>
          ))}
        </div>
      )}
      <p className="mt-3 text-xs text-gray-400 italic">
        Clarification resume is not yet implemented. This display is read-only.
      </p>
    </div>
  );
}
