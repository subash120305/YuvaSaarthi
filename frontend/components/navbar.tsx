"use client"

import { GraduationCap, Sun, Moon, Info, HelpCircle, Trash2, MoreVertical } from "lucide-react"
import { Button } from "@/components/ui/button"
import { LanguageSelector } from "./language-selector"
import { useTheme } from "next-themes"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { useState } from "react"

interface NavbarProps {
  currentLanguage: string
  onLanguageChange: (language: string) => void
  onClearChat: () => void
}

export function Navbar({ currentLanguage, onLanguageChange, onClearChat }: NavbarProps) {
  const { theme, setTheme } = useTheme()
  const [aboutOpen, setAboutOpen] = useState(false)
  const [helpOpen, setHelpOpen] = useState(false)

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 border-b border-border/50 glass backdrop-blur-xl">
      <div className="flex h-full items-center justify-between px-4 md:px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          {/* Custom Logo - Gradient Mask */}
          <div
            className="h-12 w-16 bg-gradient-to-br from-primary to-secondary"
            style={{
              maskImage: "url('/logo-icon.png')",
              maskSize: "contain",
              maskRepeat: "no-repeat",
              maskPosition: "center",
              WebkitMaskImage: "url('/logo-icon.png')",
              WebkitMaskSize: "contain",
              WebkitMaskRepeat: "no-repeat",
              WebkitMaskPosition: "center"
            }}
          />
          <div>
            <h1 className="text-lg font-semibold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              YuvaSaarthi
            </h1>
          </div>
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center gap-2">
          {/* New Chat Button */}
          <Button
            variant="outline"
            size="sm"
            onClick={onClearChat}
            className="hidden sm:flex gap-2"
            aria-label="Start new chat"
          >
            <Trash2 className="h-4 w-4" strokeWidth={2} />
            New Chat
          </Button>

          {/* Language Selector */}
          <LanguageSelector currentLanguage={currentLanguage} onLanguageChange={onLanguageChange} />

          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            aria-label="Toggle theme"
          >
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" strokeWidth={2} />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" strokeWidth={2} />
          </Button>

          {/* Settings Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" aria-label="Settings menu">
                <MoreVertical className="h-5 w-5" strokeWidth={2} />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56 bg-popover border border-border shadow-lg md:glass md:bg-transparent md:border-white/10">
              <DropdownMenuLabel>Options</DropdownMenuLabel>
              <DropdownMenuSeparator />

              <Dialog open={aboutOpen} onOpenChange={setAboutOpen}>
                <DialogTrigger asChild>
                  <DropdownMenuItem onSelect={(e) => e.preventDefault()}>
                    <Info className="mr-2 h-4 w-4" strokeWidth={2} />
                    About YuvaSaarthi
                  </DropdownMenuItem>
                </DialogTrigger>
                <DialogContent className="glass">
                  <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                      <GraduationCap className="h-5 w-5 text-primary" strokeWidth={2} />
                      About YuvaSaarthi
                    </DialogTitle>
                    <DialogDescription className="space-y-3 pt-4">
                      <p>
                        <strong>YuvaSaarthi</strong> is India's National Education Assistant, designed to help students
                        across the country with educational queries in their native language.
                      </p>
                      <p>
                        <strong>Features:</strong>
                      </p>
                      <ul className="list-disc list-inside space-y-1 text-sm">
                        <li>Support for all 23 official Indian languages</li>
                        <li>Competitive exam guidance (JEE, NEET, CUET, CLAT, etc.)</li>
                        <li>Scholarship information</li>
                        <li>College admission guidance</li>
                        <li>Study resources and tips</li>
                      </ul>
                      <p className="text-xs text-muted-foreground mt-4">
                        Version 2.0 • Made with ❤️ for Students of India 🇮🇳
                      </p>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>

              <Dialog open={helpOpen} onOpenChange={setHelpOpen}>
                <DialogTrigger asChild>
                  <DropdownMenuItem onSelect={(e) => e.preventDefault()}>
                    <HelpCircle className="mr-2 h-4 w-4" strokeWidth={2} />
                    Help & Support
                  </DropdownMenuItem>
                </DialogTrigger>
                <DialogContent className="glass">
                  <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                      <HelpCircle className="h-5 w-5 text-primary" strokeWidth={2} />
                      Help & Support
                    </DialogTitle>
                    <DialogDescription className="space-y-3 pt-4">
                      <p>
                        <strong>How to use YuvaSaarthi:</strong>
                      </p>
                      <ol className="list-decimal list-inside space-y-2 text-sm">
                        <li>Select your preferred language from the language selector</li>
                        <li>Type your question in the input box at the bottom</li>
                        <li>Click send or press Enter to get a response</li>
                        <li>Use the action buttons to copy, like, or share responses</li>
                      </ol>
                      <p className="mt-4">
                        <strong>Sample Questions:</strong>
                      </p>
                      <ul className="list-disc list-inside space-y-1 text-sm">
                        <li>What are the JEE exam dates for 2026?</li>
                        <li>How do I apply for scholarships?</li>
                        <li>Tell me about NEET eligibility</li>
                        <li>Which are the best engineering colleges?</li>
                      </ul>
                      <p className="text-xs text-muted-foreground mt-4">
                        Your chat history is saved locally in your browser.
                      </p>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>

              <DropdownMenuSeparator />

              <DropdownMenuItem onClick={onClearChat} className="text-destructive focus:text-destructive">
                <Trash2 className="mr-2 h-4 w-4" strokeWidth={2} />
                Clear Chat History
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
