import type { RunEvent } from "@/lib/types";
import { EventItem } from "./EventItem";

interface Props {
  events: RunEvent[];
}

export function EventStream({ events }: Props) {
  const visible = events.filter((e) => e.is_user_visible);

  if (visible.length === 0) return null;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-3" data-testid="event-stream">
      <h3 className="mb-2 text-xs font-semibold text-gray-500 uppercase">Run Timeline</h3>
      <ul className="space-y-1">
        {visible.map((e) => (
          <EventItem key={e.event_id} event={e} />
        ))}
      </ul>
    </div>
  );
}
