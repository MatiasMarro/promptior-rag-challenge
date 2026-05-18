import { useState } from 'react'
import Header from './components/Header'
import MessageList from './components/MessageList'
import ChatInput from './components/ChatInput'
import EmptyState from './components/EmptyState'
import type { ChatMessage } from './types'

const SUGGESTIONS = [
  '¿Qué es Promtior?',
  '¿Qué servicios ofrece?',
  '¿Con qué partners trabaja?',
]

interface InvokeResponse {
  output: string
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [, setError] = useState<string | null>(null)

  async function handleSend(text: string) {
    setError(null)
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setIsLoading(true)

    try {
      // Cada request es independiente: NO se manda historial al backend
      // (el chain no tiene memoria conversacional). El historial vive solo
      // en la UI.
      const res = await fetch('/promtior/invoke', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text }),
      })

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }

      const data = (await res.json()) as InvokeResponse
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.output },
      ])
    } catch (e) {
      const message = e instanceof Error ? e.message : 'error desconocido'
      setError(message)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            '⚠️ No pude conectar con el servidor. Intentá de nuevo en un momento.',
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const isEmpty = messages.length === 0 && !isLoading

  return (
    <div className="mx-auto flex h-full max-w-3xl flex-col">
      <Header />
      <main className="flex flex-1 flex-col overflow-y-auto">
        {isEmpty ? (
          <EmptyState suggestions={SUGGESTIONS} onSelect={handleSend} />
        ) : (
          <MessageList messages={messages} isLoading={isLoading} />
        )}
      </main>
      <ChatInput onSubmit={handleSend} isLoading={isLoading} />
    </div>
  )
}
