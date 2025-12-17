"use client"

import { useState } from "react"
import { MessageSquare, User, ThumbsUp, ThumbsDown, Copy, Share2, RefreshCw, Check, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import type { Message } from "@/lib/types"

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const [copied, setCopied] = useState(false)
  const [liked, setLiked] = useState<boolean | null>(null)

  const isUser = message.role === "user"

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const formatTime = (timestamp: Date | string) => {
    try {
      // Convert to Date if it's a string
      const date = timestamp instanceof Date ? timestamp : new Date(timestamp)

      // Check if valid date
      if (isNaN(date.getTime())) {
        return "Just now"
      }

      return new Intl.DateTimeFormat("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      }).format(date)
    } catch (error) {
      return "Just now"
    }
  }

  return (
    <div className={cn("flex gap-3", isUser ? "flex-row-reverse" : "flex-row")}>
      {/* Avatar */}
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
          isUser ? "bg-gradient-to-br from-primary to-secondary" : "bg-gradient-to-br from-accent to-primary",
        )}
      >
        {isUser ? (
          <User className="h-4 w-4 text-primary-foreground" strokeWidth={2} />
        ) : (
          <MessageSquare className="h-4 w-4 text-primary-foreground" strokeWidth={2} />
        )}
      </div>

      {/* Message Content */}
      <div className={cn("max-w-[80%] space-y-2 md:max-w-[70%]", isUser ? "items-end" : "items-start")}>
        <div
          className={cn(
            "rounded-2xl px-4 py-3",
            isUser
              ? "bg-gradient-to-br from-primary to-secondary text-primary-foreground"
              : "border border-border/50 glass",
          )}
        >
          <div className="whitespace-pre-wrap text-sm leading-relaxed">
            {message.content.split("\n").map((line, i) => (
              <p key={i} className={cn(line.startsWith("**") && "font-semibold", i > 0 && "mt-2")}>
                {line.replace(/\*\*/g, "")}
              </p>
            ))}
          </div>
        </div>

        {/* Actions & Timestamp */}
        <div
          className={cn(
            "flex items-center gap-2 text-xs text-muted-foreground",
            isUser ? "flex-row-reverse" : "flex-row",
          )}
        >
          <div className="flex items-center gap-1">
            <Clock className="h-3 w-3" strokeWidth={2} />
            {formatTime(message.timestamp)}
          </div>

          {!isUser && (
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                className={cn("h-7 w-7", liked === true && "text-primary")}
                onClick={() => setLiked(liked === true ? null : true)}
                aria-label="Like message"
              >
                <ThumbsUp className="h-3.5 w-3.5" strokeWidth={2} />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className={cn("h-7 w-7", liked === false && "text-destructive")}
                onClick={() => setLiked(liked === false ? null : false)}
                aria-label="Dislike message"
              >
                <ThumbsDown className="h-3.5 w-3.5" strokeWidth={2} />
              </Button>
              <Button variant="ghost" size="icon" className="h-7 w-7" onClick={handleCopy} aria-label="Copy message">
                {copied ? (
                  <Check className="h-3.5 w-3.5 text-primary" strokeWidth={2} />
                ) : (
                  <Copy className="h-3.5 w-3.5" strokeWidth={2} />
                )}
              </Button>
              <Button variant="ghost" size="icon" className="h-7 w-7" aria-label="Share message">
                <Share2 className="h-3.5 w-3.5" strokeWidth={2} />
              </Button>
              <Button variant="ghost" size="icon" className="h-7 w-7" aria-label="Regenerate response">
                <RefreshCw className="h-3.5 w-3.5" strokeWidth={2} />
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
