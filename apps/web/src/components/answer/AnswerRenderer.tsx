import type { FinalAnswerPayload } from "@/lib/types";
import { getBlockComponent } from "./BlockRegistry";

interface Props {
  payload: FinalAnswerPayload;
  onOpenDrawer: (type: "evidence" | "debate" | "calc", id?: string) => void;
}

export function AnswerRenderer({ payload, onOpenDrawer }: Props) {
  return (
    <div className="space-y-3" data-testid="answer-renderer">
      {payload.blocks.map((block, i) => {
        const Block = getBlockComponent(block.block_type);
        return <Block key={i} block={block} onOpenDrawer={onOpenDrawer} />;
      })}
      <div className="text-xs text-gray-500">
        {payload.confidence_summary}
      </div>
    </div>
  );
}
