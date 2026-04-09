"use client";

import { useEffect, useRef, type KeyboardEvent } from "react";

interface Props {
  open: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function DrawerShell({ open, onClose, title, children }: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open) ref.current?.focus();
  }, [open]);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") onClose();
  };

  if (!open) return null;

  return (
    <div
      ref={ref}
      tabIndex={-1}
      onKeyDown={handleKeyDown}
      className="fixed inset-y-0 right-0 z-50 flex w-96 flex-col border-l border-gray-200 bg-white shadow-xl focus:outline-none"
      role="dialog"
      aria-label={title}
      data-testid="drawer-shell"
    >
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
        <h3 className="text-sm font-semibold capitalize">{title}</h3>
        <button
          onClick={onClose}
          className="rounded p-1 text-gray-400 hover:text-gray-600"
          aria-label="Close drawer"
          data-testid="drawer-close"
        >
          ✕
        </button>
      </div>
      <div className="flex-1 overflow-y-auto p-4">{children}</div>
    </div>
  );
}
