import { Link, Navigate, Outlet, RouterProvider, createBrowserRouter } from "react-router-dom";

import { useAuth } from "../app/providers/AuthProvider";
import { LoginPage } from "../features/auth/pages/LoginPage";
import { CatsPage } from "../features/cats/pages/CatsPage";
import { FoodsPage } from "../features/foods/pages/FoodsPage";
import { OnboardingPage } from "../features/onboarding/pages/OnboardingPage";
import { RecommendationsPage } from "../features/recommendations/pages/RecommendationsPage";

function AppShell() {
  return (
    <div className="app-shell">
      <header className="top-nav">
        <Link to="/app/cats">Feedo</Link>
        <nav className="top-nav__links" aria-label="Primary">
          <Link to="/app/cats">Cats</Link>
          <Link to="/app/recommendations">Recommendations</Link>
          <Link to="/app/foods">Foods</Link>
        </nav>
      </header>
      <main className="page">
        <Outlet />
      </main>
    </div>
  );
}

function ProtectedRoute() {
  const { status } = useAuth();
  if (status === "unauthenticated") {
    return <Navigate to="/auth/login" replace />;
  }
  return <Outlet />;
}

const router = createBrowserRouter([
  { path: "/", element: <Navigate to="/app/cats" replace /> },
  { path: "/auth/login", element: <LoginPage /> },
  { path: "/onboarding", element: <OnboardingPage /> },
  {
    path: "/app",
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppShell />,
        children: [
          { path: "cats", element: <CatsPage /> },
          { path: "foods", element: <FoodsPage /> },
          { path: "recommendations", element: <RecommendationsPage /> },
          { path: "recommendations/:catPublicId", element: <RecommendationsPage /> }
        ]
      }
    ]
  }
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
