export default function HomePage() {
  return (
    <main
      style={{
        display: "flex",
        minHeight: "100vh",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1 style={{ fontSize: "1.875rem", fontWeight: 700 }}>GenUIWar</h1>
        <p style={{ marginTop: "0.5rem", color: "#666" }}>
          Ministry-grade analytical conversation system
        </p>
        <p style={{ marginTop: "1rem", fontSize: "0.875rem", color: "#999" }}>
          Phase 0 — Foundation shell
        </p>
      </div>
    </main>
  );
}
