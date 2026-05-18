export default function LoadingDots() {
  return (
    <div className="flex justify-start">
      <div className="rounded-2xl bg-brand-bg-surface px-4 py-3">
        <div className="flex gap-1.5">
          <span className="h-2 w-2 animate-bounce rounded-full bg-brand-text-secondary [animation-delay:-0.3s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-brand-text-secondary [animation-delay:-0.15s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-brand-text-secondary" />
        </div>
      </div>
    </div>
  )
}
