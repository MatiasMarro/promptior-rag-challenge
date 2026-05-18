import SuggestionChips from './SuggestionChips'

interface Props {
  suggestions: string[]
  onSelect: (suggestion: string) => void
}

export default function EmptyState({ suggestions, onSelect }: Props) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-6 px-6 text-center">
      <img src="/logo.svg" alt="Promtior" className="h-16 w-auto opacity-90" />
      <h1 className="text-lg font-semibold text-brand-text-primary">
        Ask me about Promtior
      </h1>
      <SuggestionChips suggestions={suggestions} onSelect={onSelect} />
    </div>
  )
}
