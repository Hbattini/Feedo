type EmptyStateProps = {
  title: string;
  description?: string;
};

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      {description ? <p className="muted">{description}</p> : null}
    </section>
  );
}
