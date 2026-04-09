import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DrawerShell } from "../src/components/drawers/DrawerShell";

describe("DrawerShell", () => {
  it("renders when open", () => {
    render(
      <DrawerShell open={true} onClose={vi.fn()} title="Evidence">
        <p>Content</p>
      </DrawerShell>
    );
    expect(screen.getByTestId("drawer-shell")).toBeInTheDocument();
    expect(screen.getByText("Content")).toBeInTheDocument();
  });

  it("does not render when closed", () => {
    const { container } = render(
      <DrawerShell open={false} onClose={vi.fn()} title="Evidence">
        <p>Content</p>
      </DrawerShell>
    );
    expect(container.firstChild).toBeNull();
  });

  it("calls onClose when close button clicked", () => {
    const onClose = vi.fn();
    render(
      <DrawerShell open={true} onClose={onClose} title="Evidence">
        <p>Content</p>
      </DrawerShell>
    );
    fireEvent.click(screen.getByTestId("drawer-close"));
    expect(onClose).toHaveBeenCalledOnce();
  });

  it("calls onClose on Escape key", () => {
    const onClose = vi.fn();
    render(
      <DrawerShell open={true} onClose={onClose} title="Evidence">
        <p>Content</p>
      </DrawerShell>
    );
    fireEvent.keyDown(screen.getByTestId("drawer-shell"), { key: "Escape" });
    expect(onClose).toHaveBeenCalledOnce();
  });
});
