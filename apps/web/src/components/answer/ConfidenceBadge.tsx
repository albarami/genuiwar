interface Props {
  grade: string;
}

const GRADE_COLORS: Record<string, string> = {
  high: "bg-green-100 text-green-700",
  moderate: "bg-blue-100 text-blue-700",
  emerging: "bg-amber-100 text-amber-700",
  low: "bg-orange-100 text-orange-700",
  unresolved: "bg-gray-100 text-gray-500",
};

export function ConfidenceBadge({ grade }: Props) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${GRADE_COLORS[grade] ?? GRADE_COLORS.unresolved}`}>
      {grade}
    </span>
  );
}
