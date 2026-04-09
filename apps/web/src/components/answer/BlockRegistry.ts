import type { ComponentType } from "react";
import type { AnswerBlock, AnswerBlockType } from "@/lib/types";
import { DirectAnswerBlock } from "./DirectAnswerBlock";
import { EvidenceBlock } from "./EvidenceBlock";
import { ConfidenceBlock } from "./ConfidenceBlock";
import { DebateSummaryBlock } from "./DebateSummaryBlock";
import { CalculationBlock } from "./CalculationBlock";
import { CitationsBlock } from "./CitationsBlock";

export interface BlockProps {
  block: AnswerBlock;
  onOpenDrawer: (type: "evidence" | "debate" | "calc", id?: string) => void;
}

const REGISTRY: Record<AnswerBlockType, ComponentType<BlockProps>> = {
  direct_answer: DirectAnswerBlock,
  evidence: EvidenceBlock,
  confidence: ConfidenceBlock,
  debate_summary: DebateSummaryBlock,
  calculation: CalculationBlock,
  citations: CitationsBlock,
};

export function getBlockComponent(type: AnswerBlockType): ComponentType<BlockProps> {
  return REGISTRY[type] ?? DirectAnswerBlock;
}
