import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { CalcTraceDrawer } from "../src/components/drawers/CalcTraceDrawer";

const mockTrace = {
  calculation_id: "calc1",
  operation: "percentage_change",
  trace: [
    "old = 100.0, new = 120.0",
    "change = (new - old) / old * 100",
    "change = (120.0 - 100.0) / 100.0 * 100 = 20.0",
    "output unit: percent",
  ],
  output_unit: "percent",
};

vi.mock("../src/lib/api", () => ({
  getCalculationTrace: vi.fn(),
}));

import { getCalculationTrace } from "../src/lib/api";
const mockedGet = vi.mocked(getCalculationTrace);

describe("CalcTraceDrawer", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows loading state", () => {
    mockedGet.mockReturnValue(new Promise(() => {}));
    render(<CalcTraceDrawer calcId="calc1" />);
    expect(screen.getByTestId("calc-loading")).toBeInTheDocument();
  });

  it("shows error state", async () => {
    mockedGet.mockRejectedValue(new Error("Server error"));
    render(<CalcTraceDrawer calcId="calc1" />);
    await waitFor(() => {
      expect(screen.getByTestId("calc-error")).toBeInTheDocument();
    });
    expect(screen.getByTestId("calc-error")).toHaveTextContent("Server error");
  });

  it("shows content with operation and trace lines", async () => {
    mockedGet.mockResolvedValue(mockTrace);
    render(<CalcTraceDrawer calcId="calc1" />);
    await waitFor(() => {
      expect(screen.getByTestId("calc-content")).toBeInTheDocument();
    });
    expect(screen.getByText("percentage_change")).toBeInTheDocument();
    expect(screen.getByText("old = 100.0, new = 120.0")).toBeInTheDocument();
    expect(screen.getByText("output unit: percent")).toBeInTheDocument();
    expect(screen.getByText("Unit: percent")).toBeInTheDocument();
  });
});
