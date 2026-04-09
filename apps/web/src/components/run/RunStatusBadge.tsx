import type { RunMode, RunStatus } from "@/lib/types";

interface Props {
  status: RunStatus;
  mode: RunMode;
}

const STATUS_COLORS: Record<RunStatus, string> = {
  queued: "bg-gray-200 text-gray-700",
  running: "bg-blue-100 text-blue-700",
  waiting_for_clarification: "bg-amber-100 text-amber-700",
  completed: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
  cancelled: "bg-gray-200 text-gray-500",
};

export function RunStatusBadge({ status, mode }: Props) {
  return (
    <div className="flex gap-2 text-xs" data-testid="run-status-badge">
      <span className={`rounded-full px-2 py-0.5 font-medium ${STATUS_COLORS[status]}`}>
        {status}
      </span>
      <span className="rounded-full bg-gray-100 px-2 py-0.5 text-gray-600">
        {mode} run
      </span>
    </div>
  );
}
