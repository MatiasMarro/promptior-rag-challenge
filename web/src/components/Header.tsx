export default function Header() {
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center gap-3 border-b border-brand-border bg-brand-bg-base/80 px-4 backdrop-blur sm:px-6">
      <img src="/logo.svg" alt="Promtior" className="h-8 w-auto" />
      <span className="text-sm font-medium text-brand-text-secondary">
        RAG Assistant
      </span>
    </header>
  )
}
