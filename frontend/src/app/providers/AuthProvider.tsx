import { createContext, useContext, useMemo, useState } from "react";
import type { PropsWithChildren } from "react";

import { fetchSession } from "../../features/auth/api/allauth-client";

type AuthStatus = "loading" | "authenticated" | "unauthenticated";

type Viewer = {
  publicId: string;
  email: string;
};

type AuthContextValue = {
  status: AuthStatus;
  viewer: Viewer | null;
  refreshSession: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: PropsWithChildren) {
  const [status, setStatus] = useState<AuthStatus>("unauthenticated");
  const [viewer, setViewer] = useState<Viewer | null>(null);

  async function refreshSession() {
    setStatus("loading");
    const session = await fetchSession();
    setViewer(session.viewer);
    setStatus(session.viewer ? "authenticated" : "unauthenticated");
  }

  const value = useMemo<AuthContextValue>(
    () => ({ status, viewer, refreshSession }),
    [status, viewer]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider.");
  }
  return context;
}
