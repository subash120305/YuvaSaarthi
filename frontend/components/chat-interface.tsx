"use client"

import { useState, useEffect } from "react"
import dynamic from "next/dynamic"

// Dynamically import Navbar to avoid hydration mismatch with Radix UI IDs
const Navbar = dynamic(() => import("./navbar").then((mod) => mod.Navbar), {
  ssr: false,
  loading: () => <div className="h-16 border-b border-border/50 glass" />, // Skeleton placeholder
})
import { ChatArea } from "./chat-area"
import { ChatInput } from "./chat-input"
import type { Message } from "@/lib/types"

// LocalStorage key
const STORAGE_KEY = "yuvasaarthi_chat_history"

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isTyping, setIsTyping] = useState(false)
  const [currentLanguage, setCurrentLanguage] = useState("en")

  // Load messages from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        setMessages(parsed)
      } catch (e) {
        console.error("Failed to load chat history:", e)
      }
    }
  }, [])

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages))
    }
  }, [messages])

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: "user",
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setIsTyping(true)

    try {
      // Call backend API
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: content,
          language: currentLanguage,
          conversation_id: "user_" + Date.now(),
          include_videos: true,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get response")
      }

      const data = await response.json()

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: "assistant",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error("Error:", error)
      // Fallback response
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running on http://localhost:8000",
        role: "assistant",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleClearChat = () => {
    setMessages([])
    localStorage.removeItem(STORAGE_KEY)
  }

  const handleSelectPrompt = (prompt: string) => {
    handleSendMessage(prompt)
  }

  return (
    <div className="flex h-[100dvh] overflow-hidden bg-gradient-to-br from-muted/50 via-background to-muted/30 pt-16">
      {/* Main Content - No Sidebar */}
      <div className="flex flex-1 flex-col">
        <Navbar
          currentLanguage={currentLanguage}
          onLanguageChange={setCurrentLanguage}
          onClearChat={handleClearChat}
        />

        <ChatArea
          messages={messages}
          isTyping={isTyping}
          onSelectPrompt={handleSelectPrompt}
        />

        <ChatInput
          onSend={handleSendMessage}
          disabled={isTyping}
          history={messages.filter(m => m.role === "user").map(m => m.content)}
        />
      </div>
    </div>
  )
}
