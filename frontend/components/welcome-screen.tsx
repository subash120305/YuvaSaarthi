"use client"

import { BookOpen, DollarSign, School, Building2, Award, GraduationCap } from "lucide-react"

const prompts = [
  {
    icon: BookOpen,
    title: "Exam Guidance",
    description: "JEE, NEET, GATE preparation tips",
    prompt: "Can you help me prepare for JEE Main examination?",
  },
  {
    icon: DollarSign,
    title: "Scholarships",
    description: "Find financial aid & funding",
    prompt: "What scholarships are available for engineering students in India?",
  },
  {
    icon: School,
    title: "Admissions",
    description: "Application process help",
    prompt: "How do I apply for college admissions in India?",
  },
  {
    icon: Building2,
    title: "Colleges",
    description: "Find the best institutions",
    prompt: "What are the top engineering colleges in India?",
  },
  {
    icon: Award,
    title: "Career Guidance",
    description: "Plan your future path",
    prompt: "Can you help me choose a career after 12th?",
  },
  {
    icon: GraduationCap,
    title: "Study Abroad",
    description: "International opportunities",
    prompt: "How can I apply for studying abroad after graduation?",
  },
]

interface WelcomeScreenProps {
  onSelectPrompt: (prompt: string) => void
}

export function WelcomeScreen({ onSelectPrompt }: WelcomeScreenProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      {/* Welcome Text */}
      <div className="mb-8 text-center">
        <h1 className="mb-2 text-3xl font-bold text-foreground md:text-4xl">
          Hello,{" "}
          <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Student</span>
        </h1>
        <p className="text-lg text-muted-foreground">How can I help you today?</p>
      </div>

      {/* Prompt Cards Grid */}
      <div className="grid w-full max-w-2xl gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {prompts.map((item) => (
          <button
            key={item.title}
            onClick={() => onSelectPrompt(item.prompt)}
            className="group flex flex-col items-start gap-2 rounded-xl border border-border/50 p-4 text-left transition-all duration-200 glass hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 text-primary transition-colors group-hover:from-primary/20 group-hover:to-secondary/20">
              <item.icon className="h-5 w-5" strokeWidth={2} />
            </div>
            <div>
              <h3 className="font-medium text-foreground">{item.title}</h3>
              <p className="text-sm text-muted-foreground">{item.description}</p>
            </div>
          </button>
        ))}
      </div>

      {/* Supported Languages */}
      <div className="mt-10 text-center">
        <p className="text-sm text-muted-foreground">
          Supporting <span className="font-medium text-primary">23 Indian languages</span> for inclusive education
        </p>
      </div>
    </div>
  )
}
