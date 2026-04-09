import type { ClaimLedgerEntry } from "@/lib/types";
import { ConfidenceBadge } from "@/components/answer/ConfidenceBadge";

interface Props {
  claims: ClaimLedgerEntry[];
}

export function DebateDrawer({ claims }: Props) {
  if (claims.length === 0) {
    return <div data-testid="debate-empty" className="text-sm text-gray-400">No claims to display</div>;
  }

  return (
    <div className="space-y-3" data-testid="debate-content">
      {claims.map((claim) => (
        <div key={claim.claim_id} className="rounded border border-gray-200 p-3 text-sm">
          <div className="mb-1 flex items-center gap-2">
            <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${
              claim.adjudication_status === "approved" ? "bg-green-100 text-green-700" :
              claim.adjudication_status === "downgraded" ? "bg-amber-100 text-amber-700" :
              claim.adjudication_status === "rejected" ? "bg-red-100 text-red-700" :
              "bg-gray-100 text-gray-500"
            }`}>
              {claim.adjudication_status}
            </span>
            <ConfidenceBadge grade={claim.confidence_grade} />
          </div>
          <p className="text-gray-800">{claim.claim_text}</p>
          {claim.adjudication_reason && (
            <p className="mt-1 text-xs text-gray-500">Reason: {claim.adjudication_reason}</p>
          )}
          {claim.challenge_flags.length > 0 && (
            <div className="mt-1 flex flex-wrap gap-1">
              {claim.challenge_flags.map((flag) => (
                <span key={flag} className="rounded bg-red-50 px-1.5 py-0.5 text-xs text-red-600">{flag}</span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
