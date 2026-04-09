import type { RunEvent, RunStatus } from "@/lib/types";

interface Props {
  events: RunEvent[];
  status: RunStatus;
}

export function GovernanceFailurePanel({ events, status }: Props) {
  const violations = events.filter(
    (e) =>
      e.event_type === "adjudication.governance_violation" ||
      e.event_type === "answer.governance_violation"
  );

  return (
    <div className="rounded-lg border-2 border-red-300 bg-red-50 p-4" data-testid="governance-failure">
      <h4 className="mb-2 text-sm font-semibold text-red-700">
        {status === "failed" ? "Run Failed — Governance Violation" : "Run Failed"}
      </h4>
      {violations.length > 0 ? (
        <ul className="space-y-2">
          {violations.map((v) => {
            const msgs = Array.isArray(v.payload?.violations)
              ? (v.payload.violations as string[])
              : [];
            return (
              <li key={v.event_id} className="text-sm text-red-800">
                <span className="font-medium">{v.title}</span>
                {msgs.length > 0 && (
                  <ul className="mt-1 ml-4 list-disc text-xs text-red-600">
                    {msgs.map((msg, i) => (
                      <li key={i}>{msg}</li>
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      ) : (
        <p className="text-sm text-red-700">
          This answer was blocked by governance validation. No answer blocks were released.
        </p>
      )}
    </div>
  );
}
