"use client"

import type React from "react"

import { Plus, MessageCircle, Settings, Info, HelpCircle, Trash2, Calendar, History, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { ChatSession } from "@/lib/types"
import { cn } from "@/lib/utils"

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  sessions: ChatSession[]
  onNewChat: () => void
  onSelectSession: (id: string) => void
}

export function Sidebar({ isOpen, onClose, sessions, onNewChat, onSelectSession }: SidebarProps) {
  const todaySessions = sessions.filter((s) => new Date(s.date).toDateString() === new Date().toDateString())
  const yesterdaySessions = sessions.filter((s) => {
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    return new Date(s.date).toDateString() === yesterday.toDateString()
  })
  const olderSessions = sessions.filter((s) => {
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    return new Date(s.date) < yesterday
  })

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-50 w-72 transform border-r border-border/50 glass transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0",
        isOpen ? "translate-x-0" : "-translate-x-full",
      )}
    >
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center justify-between border-b border-border/50 px-4">
          <Button
            onClick={onNewChat}
            className="flex-1 gap-2 bg-gradient-to-r from-primary to-secondary text-primary-foreground hover:opacity-90"
          >
            <Plus className="h-4 w-4" strokeWidth={2} />
            New Chat
          </Button>
          <Button variant="ghost" size="icon" className="ml-2 lg:hidden" onClick={onClose} aria-label="Close sidebar">
            <X className="h-5 w-5" strokeWidth={2} />
          </Button>
        </div>

        {/* Chat History */}
        <ScrollArea className="flex-1 px-2 py-4">
          {todaySessions.length > 0 && (
            <SessionGroup
              icon={<Calendar className="h-4 w-4" strokeWidth={2} />}
              title="Today"
              sessions={todaySessions}
              onSelectSession={onSelectSession}
            />
          )}

          {yesterdaySessions.length > 0 && (
            <SessionGroup
              icon={<History className="h-4 w-4" strokeWidth={2} />}
              title="Yesterday"
              sessions={yesterdaySessions}
              onSelectSession={onSelectSession}
            />
          )}

          {olderSessions.length > 0 && (
            <SessionGroup
              icon={<History className="h-4 w-4" strokeWidth={2} />}
              title="Previous"
              sessions={olderSessions}
              onSelectSession={onSelectSession}
            />
          )}
        </ScrollArea>

        {/* Footer */}
        <div className="border-t border-border/50 p-2">
          <Button variant="ghost" className="w-full justify-start gap-2">
            <Settings className="h-4 w-4" strokeWidth={2} />
            Settings
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-2">
            <Info className="h-4 w-4" strokeWidth={2} />
            About
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-2">
            <HelpCircle className="h-4 w-4" strokeWidth={2} />
            Help
          </Button>
        </div>
      </div>
    </aside>
  )
}

function SessionGroup({
  icon,
  title,
  sessions,
  onSelectSession,
}: {
  icon: React.ReactNode
  title: string
  sessions: ChatSession[]
  onSelectSession: (id: string) => void
}) {
  return (
    <div className="mb-4">
      <div className="mb-2 flex items-center gap-2 px-2 text-xs font-medium text-muted-foreground">
        {icon}
        {title}
      </div>
      <div className="space-y-1">
        {sessions.map((session) => (
          <button
            key={session.id}
            onClick={() => onSelectSession(session.id)}
            className="group flex w-full items-center gap-2 rounded-lg px-2 py-2 text-left text-sm transition-colors hover:bg-muted/50"
          >
            <MessageCircle className="h-4 w-4 shrink-0 text-muted-foreground" strokeWidth={2} />
            <span className="flex-1 truncate">{session.title}</span>
            <Trash2
              className="h-4 w-4 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100 hover:text-destructive"
              strokeWidth={2}
            />
          </button>
        ))}
      </div>
    </div>
  )
}
