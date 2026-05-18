import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { Role } from '../types'

interface Props {
  role: Role
  content: string
}

export default function MessageBubble({ role, content }: Props) {
  if (role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] whitespace-pre-wrap break-words rounded-2xl bg-brand-accent px-4 py-2.5 text-brand-bg-base">
          {content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="bot-markdown max-w-[90%] break-words rounded-2xl bg-brand-bg-surface px-4 py-2.5 text-brand-text-primary">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  )
}
