"use client"

import { useState } from "react"
import { Globe, Search, Check, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"

const languages = {
  popular: [
    { code: "en", name: "English", native: "English" },
    { code: "hi", name: "Hindi", native: "हिंदी" },
    { code: "ta", name: "Tamil", native: "தமிழ்" },
    { code: "te", name: "Telugu", native: "తెలుగు" },
  ],
  all: [
    { code: "bn", name: "Bengali", native: "বাংলা" },
    { code: "gu", name: "Gujarati", native: "ગુજરાતી" },
    { code: "kn", name: "Kannada", native: "ಕನ್ನಡ" },
    { code: "ml", name: "Malayalam", native: "മലയാളം" },
    { code: "mr", name: "Marathi", native: "मराठी" },
    { code: "or", name: "Odia", native: "ଓଡ଼ିଆ" },
    { code: "pa", name: "Punjabi", native: "ਪੰਜਾਬੀ" },
    { code: "ur", name: "Urdu", native: "اردو" },
    { code: "as", name: "Assamese", native: "অসমীয়া" },
    { code: "bh", name: "Bhojpuri", native: "भोजपुरी" },
    { code: "ks", name: "Kashmiri", native: "कॉशुर" },
    { code: "kok", name: "Konkani", native: "कोंकणी" },
    { code: "mai", name: "Maithili", native: "मैथिली" },
    { code: "mni", name: "Manipuri", native: "মৈতৈলোন্" },
    { code: "ne", name: "Nepali", native: "नेपाली" },
    { code: "sa", name: "Sanskrit", native: "संस्कृतम्" },
    { code: "sd", name: "Sindhi", native: "سنڌي" },
    { code: "doi", name: "Dogri", native: "डोगरी" },
    { code: "sat", name: "Santali", native: "ᱥᱟᱱᱛᱟᱲᱤ" },
  ],
}

interface LanguageSelectorProps {
  currentLanguage: string
  onLanguageChange: (language: string) => void
}

export function LanguageSelector({ currentLanguage, onLanguageChange }: LanguageSelectorProps) {
  const [search, setSearch] = useState("")

  const allLanguages = [...languages.popular, ...languages.all]
  const filteredLanguages = allLanguages.filter(
    (lang) =>
      lang.name.toLowerCase().includes(search.toLowerCase()) ||
      lang.native.toLowerCase().includes(search.toLowerCase()),
  )

  // Find current language native name
  const currentLang = allLanguages.find(l => l.code === currentLanguage)
  const displayName = currentLang?.native || "English"

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="gap-2 rounded-full px-3">
          <Globe className="h-4 w-4" strokeWidth={2} />
          <span className="hidden sm:inline">{displayName}</span>
          <ChevronDown className="h-3 w-3 opacity-50" strokeWidth={2} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-64 bg-popover border border-border shadow-lg md:glass md:bg-transparent md:border-white/10">
        <div className="p-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={2} />
            <Input
              placeholder="Search languages..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8"
            />
          </div>
        </div>

        {!search && (
          <>
            <DropdownMenuLabel className="text-xs text-muted-foreground">Popular Languages</DropdownMenuLabel>
            {languages.popular.map((lang) => (
              <DropdownMenuItem
                key={lang.code}
                onClick={() => onLanguageChange(lang.code)}
                className="flex items-center justify-between"
              >
                <span>
                  {lang.native} <span className="text-muted-foreground">({lang.name})</span>
                </span>
                {currentLanguage === lang.code && <Check className="h-4 w-4 text-primary" strokeWidth={2} />}
              </DropdownMenuItem>
            ))}
            <DropdownMenuSeparator />
            <DropdownMenuLabel className="text-xs text-muted-foreground">All Languages (23)</DropdownMenuLabel>
          </>
        )}

        <div className="max-h-48 overflow-y-auto">
          {(search ? filteredLanguages : languages.all).map((lang) => (
            <DropdownMenuItem
              key={lang.code}
              onClick={() => onLanguageChange(lang.code)}
              className="flex items-center justify-between"
            >
              <span>
                {lang.native} <span className="text-muted-foreground">({lang.name})</span>
              </span>
              {currentLanguage === lang.code && <Check className="h-4 w-4 text-primary" strokeWidth={2} />}
            </DropdownMenuItem>
          ))}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
