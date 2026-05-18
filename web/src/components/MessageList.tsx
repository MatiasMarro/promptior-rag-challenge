import { useEffect, useRef } from 'react'
import type { ChatMessage } from '../types'
import MessageBubble from './MessageBubble'
import LoadingDots from './LoadingDots'

interface Props {
  messages: ChatMessage[]
  isLoading: boolean
}

export default function MessageList({ messages, isLoading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  // Auto-scroll al final con cada mensaje nuevo o cambio de loading.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="flex flex-col gap-4 px-4 py-4 sm:px-6 sm:py-6">
      {messages.map((m, i) => (
        <MessageBubble key={i} role={m.role} content={m.content} />
      ))}
      {isLoading && <LoadingDots />}
      <div ref={bottomRef} />
    </div>
  )
}
