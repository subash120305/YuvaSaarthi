"use client"

import { MessageSquare } from "lucide-react"

export function TypingIndicator() {
  return (
    <div className="flex gap-3">
      {/* Avatar */}
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-accent to-primary">
        <MessageSquare className="h-4 w-4 text-primary-foreground" strokeWidth={2} />
      </div>

      {/* Typing Dots */}
      <div className="rounded-2xl border border-border/50 px-4 py-3 glass">
        <div className="flex items-center gap-1">
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.3s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.15s]" />
          <span className="h-2 w-2 animate-bounce rounded-full bg-primary" />
        </div>
      </div>
    </div>
  )
}
