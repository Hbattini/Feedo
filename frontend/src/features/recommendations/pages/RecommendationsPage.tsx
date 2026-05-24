import { useParams } from "react-router-dom";

import { EmptyState } from "../../../components/feedback/EmptyState";

export function RecommendationsPage() {
  const { catPublicId } = useParams();
  return (
    <div className="stack">
      <h1>Recommendations</h1>
      <EmptyState
        title={catPublicId ? "No recommendations generated" : "Choose a cat"}
        description="Recommendations are deterministic and all feedback must be tied to a specific cat."
      />
    </div>
  );
}
