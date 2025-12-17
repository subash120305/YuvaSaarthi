"use client"

import { useRef, useEffect, useState } from "react"
import { ArrowDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { WelcomeScreen } from "./welcome-screen"
import { ChatMessage } from "./chat-message"
import { TypingIndicator } from "./typing-indicator"
import type { Message } from "@/lib/types"

interface ChatAreaProps {
  messages: Message[]
  isTyping: boolean
  onSelectPrompt: (prompt: string) => void
}

export function ChatArea({ messages, isTyping, onSelectPrompt }: ChatAreaProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const [showScrollButton, setShowScrollButton] = useState(false)
  const [isUserScrolling, setIsUserScrolling] = useState(false)
  const prevMessageCount = useRef(messages.length)

  // Auto-scroll to bottom only when NEW messages are added
  useEffect(() => {
    // Only auto-scroll if messages were added and user isn't manually scrolling
    if (messages.length > prevMessageCount.current && !isUserScrolling) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }
    prevMessageCount.current = messages.length
  }, [messages.length, isUserScrolling])

  // Detect scroll position to show/hide button
  const handleScroll = () => {
    if (!scrollContainerRef.current) return

    const element = scrollContainerRef.current
    const isNearBottom = element.scrollHeight - element.scrollTop - element.clientHeight < 100

    // User is scrolling if they're not near the bottom
    setIsUserScrolling(!isNearBottom)
    setShowScrollButton(!isNearBottom && messages.length > 0)
  }

  const scrollToBottom = () => {
    setIsUserScrolling(false) // Re-enable auto-scroll
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const showWelcome = messages.length === 0

  return (
    <div className="relative flex-1 overflow-hidden">
      <div
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="h-full overflow-y-auto scrollbar-thin scrollbar-thumb-border scrollbar-track-transparent"
      >
        <div className="mx-auto max-w-3xl px-4 py-6">
          {showWelcome ? (
            <WelcomeScreen onSelectPrompt={onSelectPrompt} />
          ) : (
            <div className="space-y-6">
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isTyping && <TypingIndicator />}
              {/* Invisible element to scroll to */}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Floating Scroll to Bottom Button */}
      {showScrollButton && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10">
          <Button
            onClick={scrollToBottom}
            size="icon"
            className="h-10 w-10 rounded-full shadow-lg bg-gradient-to-br from-primary to-secondary hover:opacity-90"
            aria-label="Scroll to bottom"
          >
            <ArrowDown className="h-5 w-5" strokeWidth={2} />
          </Button>
        </div>
      )}
    </div>
  )
}
