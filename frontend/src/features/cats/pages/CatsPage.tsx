import { EmptyState } from "../../../components/feedback/EmptyState";

export function CatsPage() {
  return (
    <div className="stack">
      <h1>Cats</h1>
      <EmptyState
        title="No cats yet"
        description="Create individual profiles so every recommendation and feedback event has explicit cat context."
      />
    </div>
  );
}
