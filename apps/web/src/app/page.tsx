"use client";

import { useState } from "react";
import { ChatThread } from "@/components/chat/ChatThread";
import { FilePanel } from "@/components/files/FilePanel";
import { DrawerShell } from "@/components/drawers/DrawerShell";
import { EvidenceDrawer } from "@/components/drawers/EvidenceDrawer";
import { DebateDrawer } from "@/components/drawers/DebateDrawer";
import { CalcTraceDrawer } from "@/components/drawers/CalcTraceDrawer";
import { useRun } from "@/hooks/useRun";
import { useFiles } from "@/hooks/useFiles";

type DrawerType = "evidence" | "debate" | "calc" | null;

export default function HomePage() {
  const run = useRun();
  const fileState = useFiles();
  const [drawer, setDrawer] = useState<DrawerType>(null);
  const [drawerId, setDrawerId] = useState<string | null>(null);

  const openDrawer = (type: DrawerType, id?: string) => {
    setDrawer(type);
    setDrawerId(id ?? null);
  };

  return (
    <div className="flex h-screen">
      <aside className="hidden w-72 border-r border-gray-200 bg-white md:block">
        <FilePanel files={fileState.files} uploading={fileState.uploading} onUpload={fileState.upload} />
      </aside>

      <main className="flex flex-1 flex-col">
        <ChatThread
          state={run.state}
          result={run.result}
          error={run.error}
          fileIds={fileState.fileIds}
          onSubmit={run.submitQuestion}
          onOpenDrawer={openDrawer}
        />
      </main>

      <DrawerShell open={drawer !== null} onClose={() => setDrawer(null)} title={drawer ?? ""}>
        {drawer === "evidence" && drawerId && <EvidenceDrawer chunkId={drawerId} />}
        {drawer === "debate" && run.result && <DebateDrawer claims={run.result.claims} />}
        {drawer === "calc" && drawerId && <CalcTraceDrawer calcId={drawerId} />}
      </DrawerShell>
    </div>
  );
}
