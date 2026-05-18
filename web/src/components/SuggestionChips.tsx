interface Props {
  suggestions: string[]
  onSelect: (suggestion: string) => void
}

export default function SuggestionChips({ suggestions, onSelect }: Props) {
  return (
    <div className="flex flex-wrap justify-center gap-2">
      {suggestions.map((s) => (
        <button
          key={s}
          type="button"
          onClick={() => onSelect(s)}
          className="rounded-full border border-brand-border bg-brand-bg-surface px-4 py-2 text-sm text-brand-text-secondary transition-colors hover:border-brand-accent hover:text-brand-text-primary"
        >
          {s}
        </button>
      ))}
    </div>
  )
}
