import { useLayoutEffect, useRef, useState } from 'react'

interface Props {
  onSubmit: (text: string) => void
  isLoading: boolean
}

const MAX_ROWS = 4
const LINE_HEIGHT = 24
const VERTICAL_PADDING = 20

export default function ChatInput({ onSubmit, isLoading }: Props) {
  const [value, setValue] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize entre 1 y 4 líneas.
  useLayoutEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    const maxHeight = LINE_HEIGHT * MAX_ROWS + VERTICAL_PADDING
    el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`
  }, [value])

  const canSend = value.trim().length > 0 && !isLoading

  function submit() {
    if (!canSend) return
    onSubmit(value.trim())
    setValue('')
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    // Enter envía, Shift+Enter inserta salto de línea.
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className="sticky bottom-0 border-t border-brand-border bg-brand-bg-base/90 px-4 py-3 backdrop-blur sm:px-6">
      <div className="flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder="Type your question…"
          className="max-h-40 flex-1 resize-none rounded-2xl border border-brand-border bg-brand-bg-surface px-4 py-2.5 text-brand-text-primary placeholder:text-brand-text-secondary focus:outline-none focus:ring-1 focus:ring-brand-accent"
        />
        <button
          type="button"
          onClick={submit}
          disabled={!canSend}
          aria-label="Send"
          className="shrink-0 rounded-2xl bg-brand-accent px-4 py-2.5 font-semibold text-brand-bg-base transition-colors hover:bg-brand-accent-hover disabled:cursor-not-allowed disabled:opacity-40"
        >
          ↑
        </button>
      </div>
    </div>
  )
}
