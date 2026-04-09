import type { RunEvent } from "@/lib/types";

const GROUP_ICONS: Record<string, string> = {
  run_lifecycle: "▶",
  retrieval: "🔍",
  analysis: "📝",
  calculation: "🔢",
  challenge: "⚡",
  adjudication: "⚖️",
  clarification: "❓",
  answer_rendering: "✅",
};

interface Props {
  event: RunEvent;
}

export function EventItem({ event }: Props) {
  const icon = GROUP_ICONS[event.event_group] ?? "•";
  return (
    <li className="flex items-start gap-2 text-xs text-gray-600">
      <span className="mt-0.5 shrink-0">{icon}</span>
      <div>
        <span className="font-medium text-gray-800">{event.title}</span>
        {event.summary && <span className="ml-1 text-gray-500">— {event.summary}</span>}
        {event.agent_name && (
          <span className="ml-1 text-gray-400">({event.agent_name})</span>
        )}
      </div>
    </li>
  );
}
