import { EmptyState } from "../../../components/feedback/EmptyState";

export function FoodsPage() {
  return (
    <div className="stack">
      <h1>Food catalog</h1>
      <EmptyState
        title="Catalog pending"
        description="Food records come from deterministic ingestion, validation, enrichment, and QA."
      />
    </div>
  );
}
