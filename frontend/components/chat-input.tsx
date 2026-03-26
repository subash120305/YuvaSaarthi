"use client"

import { useState, useRef, useEffect, type KeyboardEvent } from "react"
import { Paperclip, Mic, ArrowUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
  history?: string[]
}

export function ChatInput({ onSend, disabled, history = [] }: ChatInputProps) {
  const [message, setMessage] = useState("")
  const [isRecording, setIsRecording] = useState(false)
  const [historyIndex, setHistoryIndex] = useState(-1)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [message])

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim())
      setMessage("")
      setHistoryIndex(-1)
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
      return
    }

    // Up Arrow - Navigate History Backwards
    if (e.key === "ArrowUp") {
      if (!history.length) return

      // Only navigate if cursor is at start or stored index is active
      if (textareaRef.current && textareaRef.current.selectionStart === 0) {
        e.preventDefault()
        const lastIdx = history.length - 1
        let newIdx = historyIndex

        if (historyIndex === -1) {
          newIdx = lastIdx
        } else {
          newIdx = Math.max(0, historyIndex - 1)
        }

        setHistoryIndex(newIdx)
        setMessage(history[newIdx])
      }
    }

    // Down Arrow - Navigate History Forwards
    if (e.key === "ArrowDown") {
      if (historyIndex === -1) return

      e.preventDefault()
      const lastIdx = history.length - 1

      if (historyIndex === lastIdx) {
        setHistoryIndex(-1)
        setMessage("")
      } else {
        const newIdx = Math.min(lastIdx, historyIndex + 1)
        setHistoryIndex(newIdx)
        setMessage(history[newIdx])
      }
    }
  }

  const toggleRecording = () => {
    setIsRecording((prev) => !prev)
    // Voice recording logic would go here
  }

  const hasMessage = message.trim().length > 0

  return (
    <div className="border-t border-border/50 p-4 glass">
      <div className="mx-auto max-w-3xl">
        <div className="flex items-end gap-2 rounded-2xl border border-border/50 bg-card/50 p-2 transition-colors focus-within:border-primary/50">
          {/* Attach Button (Disabled temporarily) */}
          {/* <Button variant="ghost" size="icon" className="h-9 w-9 shrink-0 rounded-full" aria-label="Attach file">
            <Paperclip className="h-5 w-5" strokeWidth={2} />
          </Button> */}

          {/* Text Input */}
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything about education..."
            disabled={disabled}
            rows={1}
            className="max-h-[200px] min-h-[40px] flex-1 resize-none bg-transparent py-2 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
          />

          {/* Voice Button (Disabled temporarily) */}
          {/* <Button
            variant="ghost"
            size="icon"
            className={cn(
              "h-9 w-9 shrink-0 rounded-full transition-colors",
              isRecording && "bg-destructive/10 text-destructive animate-pulse",
            )}
            onClick={toggleRecording}
            aria-label={isRecording ? "Stop recording" : "Start voice input"}
          >
            <Mic className="h-5 w-5" strokeWidth={2} />
          </Button> */}

          {/* Send Button */}
          <Button
            size="icon"
            className={cn(
              "h-9 w-9 shrink-0 rounded-full transition-all",
              hasMessage && !disabled
                ? "bg-gradient-to-br from-primary to-secondary text-primary-foreground shadow-lg shadow-primary/25"
                : "bg-muted text-muted-foreground",
            )}
            onClick={handleSend}
            disabled={!hasMessage || disabled}
            aria-label="Send message"
          >
            <ArrowUp className="h-5 w-5" strokeWidth={2} />
          </Button>
        </div>

        {/* Helper Text */}
        <p className="mt-2 text-center text-xs text-muted-foreground">
          YuvaSaarthi can make mistakes. Verify important information.
        </p>
      </div>
    </div>
  )
}
