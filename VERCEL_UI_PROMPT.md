# YuvaSaarthi - Premium Chatbot UI Generation Prompt  
**NO EMOJIS EDITION - Professional 2D Line Icons Only**

---

## CRITICAL DESIGN RULES

### **ICON REQUIREMENTS:**
**ABSOLUTELY NO EMOJIS ANYWHERE IN THE INTERFACE**
- Use ONLY 2D line icons from **Lucide Icons** (https://lucide.dev)
- Alternative: Heroicons (https://heroicons.com)
- All icons must be stroke-based, minimal, professional
- Icon stroke-width: 2px (1.5px for smaller icons)
- Icon size: 20-24px for buttons, 18px for inline, 32px for avatars
- Icon library: `lucide-react` package

---

## Project Overview
Create a **world-class, glassmorphic, minimal chatbot interface** for YuvaSaarthi - India's National Education Assistant supporting 23 languages.

---

## Design Requirements

### **Overall Aesthetic:**
- **Style:** Minimal, clean, glassmorphic, professional
- **Inspiration:** ChatGPT, Claude.ai, Google Gemini, Perplexity.ai
- **Color Scheme:**
  - Primary: #6366f1 (indigo)  
  - Secondary: #8b5cf6 (purple)
  - Accent: #06b6d4 (cyan)
  - Background Light: #f8fafc → #f1f5f9 gradient
  - Background Dark: #0f172a → #1e293b gradient
- **Typography:**
  - Font: Inter or SF Pro Display
  - Heading: 32-48px
  - Body: 14-16px
- **Theme:** Light + Dark mode support

---

## Layout Structure

### **1. Top Navigation Bar**
```
┌──────────────────────────────────────────────────────────┐
│ [GraduationCap] YuvaSaarthi    [Globe] [Sun/Moon] [Menu] │
└──────────────────────────────────────────────────────────┘
```

**Elements:**
- **Logo:** GraduationCap icon + "YuvaSaarthi" text (gradient)
- **Language Selector:** Globe icon + dropdown
  - NO flag emojis
  - Just text: "हिंदी", "English", "தமிழ்", etc.
  - Search icon inside dropdown
- **Theme Toggle:** Sun icon (light) / Moon icon (dark)
- **Menu:** Menu icon (hamburger)
- **Height:** 64px, glassmorphic

**Icons:**
- `graduation-cap` (logo)
- `globe` (language)
- `sun` / `moon` (theme)
- `menu` (navigation)

---

### **2. Main Chat Area**

```
┌────────────────────────────────────────────────┐
│          "Hello, Username"                     │
│      "How can I help you today?"               │
│                                                │
│     [Suggested Prompt Cards Grid]              │
│                                                │
│  ┌──────────────────────────────────┐         │
│  │ [Bot] Message content            │         │
│  │ [ThumbsUp][ThumbsDown][Copy]     │         │
│  │ [Share][RefreshCw]               │         │
│  └──────────────────────────────────┘         │
│                                                │
│              ┌──────────────────────┐          │
│              │ User message [User]  │          │
│              │ [Clock] 2:34 PM      │          │
│              └──────────────────────┘          │
└────────────────────────────────────────────────┘
```

**Bot Messages (LEFT, 60% width):**
- Avatar: `message-square` icon in gradient circle (32px)
- Glass card with blur effect
- Message content with markdown
- Action icons below message:
  - `thumbs-up` (Like)
  - `thumbs-down` (Dislike)
  - `copy` (Copy)
  - `share-2` (Share)
  - `refresh-cw` (Regenerate)
- Typing indicator: 3 animated dots (CSS or `loader-2` icon)

**User Messages (RIGHT, 50% width):**
- Avatar: `user` or `user-circle-2` icon in gradient (32px)
- Gradient background bubble (indigo → purple)
- Timestamp with `clock` icon
- Edit with `edit-3` icon

**All Message Icons:**
- message-square, user, user-circle-2
- thumbs-up, thumbs-down, copy, share-2, refresh-cw
- clock, edit-3

---

### **3. Input Area (Bottom)**

```
┌──────────────────────────────────────────────────────┐
│ [Paperclip] [Enter message...] [Mic] [ArrowUp]      │
└──────────────────────────────────────────────────────┘
```

**Elements:**
- **Attach:** `paperclip` icon
- **Text Input:** Multiline, auto-expand
- **Voice:** `mic` icon (pulse when active)
- **Send:** `arrow-up` icon in gradient circle
  - Disabled (gray) when empty
  - Active (gradient glow) when text present

**Icons:**
- `paperclip` (attach)
- `mic` (voice)
- `arrow-up` (send)

---

### **4. Sidebar (Collapsible)**

```
┌─────────────────────┐
│ [Plus] New Chat     │
│ ─────────────────── │
│ [Calendar] Today    │
│   [MessageCircle]..│
│ [History] Yesterday │
│   [MessageCircle]..│
│ ─────────────────── │
│ [Settings] Settings │
│ [Info] About        │
│ [HelpCircle] Help   │
└─────────────────────┘
```

**Icons:**
- `plus` (new chat)
- `calendar` (date groups)
- `message-circle` (chat items)
- `history` (past chats)
- `settings` (settings)
- `info` (about)
- `help-circle` (help)
- `trash-2` (delete on hover)

---

### **5. Suggested Prompt Cards (Welcome)**

```
┌──────────────────┐  ┌──────────────────┐
│ [BookOpen]       │  │ [DollarSign]     │
│ Exam Guidance    │  │ Scholarships     │
│ JEE, NEET info   │  │ Find funding     │
└──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐
│ [School]         │  │ [Building2]      │
│ Admissions       │  │ Colleges         │
│ Process help     │  │ Best options     │
└──────────────────┘  └──────────────────┘
```

**Icons for Cards:**
- `book-open` (exams/textbooks)
- `dollar-sign` or `banknote` (scholarships)
- `school` (admissions)
- `building-2` (colleges)
- `graduation-cap` (education)
- `award` (achievements)

---

### **6. Language Dropdown**

**NO flag emojis!**

```
┌─────────────────────────────┐
│ [Search] Search...          │
├─────────────────────────────┤
│ Popular Languages           │
│ हिंदी (Hindi)               │
│ English                     │
│ தமிழ் (Tamil)               │
│ తెలుగు (Telugu)             │
├─────────────────────────────┤
│ All Languages (23)          │
│ বাংলা (Bengali)             │
│ ગુજરાતી (Gujarati)          │
│ ... (expand for more)       │
└─────────────────────────────┘
```

**Icons:**
- `search` (search bar)
- `check` (selected language)
- `chevron-down` (expand dropdown)

---

### **7. Video Recommendations**

```
[Video] Recommended Videos:
┌────────────────────┐ ┌────────────────────┐
│ [Play] Thumbnail   │ │ [Play] Thumbnail   │
│ Video Title        │ │ Video Title        │
│ [User] Channel     │ │ [User] Channel     │
│ [Clock] 12:30      │ │ [Clock] 8:45       │
└────────────────────┘ └────────────────────┘
```

**Icons:**
- `video` (section header)
- `play` (play button overlay)
- `user` (channel icon)
- `clock` (duration)
- `external-link` (open in new tab)

---

## Complete Icon Reference

### **Navigation & Layout:**
- graduation-cap, globe, sun, moon, menu
- sidebar, panel-left, panel-right-close

### **Messages & Chat:**
- message-square, user, user-circle-2
- message-circle, messages
- send, arrow-up, corner-up-left

### **Actions:**
- thumbs-up, thumbs-down
- copy, share-2, refresh-cw
- edit-3, trash-2, download
- bookmark, heart, flag

### **Input & Media:**
- paperclip, mic, image, file
- video, play, pause
- volume-2, volume-x

### **UI Elements:**
- search, filter, settings
- info, help-circle, alert-circle
- check, x, chevron-down, chevron-up
- plus, minus, maximize, minimize

### **Education Specific:**
- book-open, library, notebook
- school, graduation-cap, award
- calculator, flask, atom
- building-2, map-pin, globe-2

### **Time & Status:**
- clock, calendar, history
- loader-2 (loading/typing)
- check-circle (success)
- alert-triangle (warning)

---

## Glassmorphism CSS

```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
}

.glass-card-dark {
  background: rgba(17, 25, 40, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.06);
}
```

---

## Animations

- **Message Appear:** Fade + slide from bottom (0.3s)
- **Icon Hover:** Scale(1.1) + color transition (0.2s)
- **Loading:** Rotating loader-2 icon
- **Theme:** Color transition (0.4s)
- **Typing Indicator:** 3 dots pulse animation

---

## Technical Stack

### **Required:**
- Next.js 14 + TypeScript
- Tailwind CSS 3.4+
- **lucide-react** (MUST USE THIS for all icons)
- Framer Motion (animations)
- Radix UI (accessible components)

### **Install Icons:**
```bash
npm install lucide-react
```

### **Usage Example:**
```tsx
import { GraduationCap, Globe, ThumbsUp, Copy } from 'lucide-react';

<GraduationCap className="w-6 h-6" strokeWidth={2} />
<Globe className="w-5 h-5" stroke Width={1.5} />
```

---

## Responsive Design

**Mobile (< 768px):**
- Hide sidebar (show on menu tap)
- Full-width messages
- Icon-only action buttons
- Floating send button

**Tablet (768px - 1024px):**
- Sidebar toggleable
- 80% message width
- All icons visible

**Desktop (> 1024px):**
- Sidebar always visible
- Max-width 1200px centered
- Spacious layout

---

## Accessibility

- All icons have aria-labels
- Keyboard navigation (Tab, Enter, Esc)
- Screen reader friendly
- High contrast mode support
- Focus indicators on all interactive elements

---

## Final Generation Prompt

**COPY THIS TO v0.dev or AI CODE GENERATOR:**

> Create a premium glassmorphic chatbot interface for YuvaSaarthi - National Education Assistant for India.
>
> **CRITICAL: NO EMOJIS - Use lucide-react icons ONLY**
>
> **Layout:**
> - Top navbar: graduation-cap logo, globe (language), sun/moon (theme), menu
> - Chat: Bot messages LEFT (60%, glass cards), User messages RIGHT (gradient bubbles)
> - Bot message actions: thumbs-up, thumbs-down, copy, share-2, refresh-cw icons
> - Input: paperclip (attach), mic (voice), arrow-up (send) icons
> - Sidebar: plus (new chat), message-circle (history), settings icons
>
> **Design:**
> - Glassmorphism throughout (backdrop-blur, semi-transparent)
> - Colors: Indigo/purple gradients (#6366f1 to #8b5cf6), cyan accents (#06b6d4)
> - Dark + Light theme
> - All icons from lucide-react library (stroke-width: 2)
> - Smooth animations, typing indicator
>
> **Features:**
> - Welcome screen with 4-6 prompt cards (book-open, dollar-sign, school, building-2 icons)
> - 23-language selector (globe icon, NO flags, text only)
> - Message markdown + code syntax highlighting
> - Video cards with play icons
> - Responsive (mobile/tablet/desktop)
>
> **Stack:** Next.js 14, TypeScript, Tailwind CSS, lucide-react, Framer Motion
>
> Make it professional, minimal, world-class. ChatGPT meets Perplexity design.

---

**Icon Package:** lucide-react (https://lucide.dev)  
**All Icons:** 2D line style, stroke-based, NO emojis anywhere  
**Theme:** Professional, minimal, glassmorphic  

---

**Made for YuvaSaarthi - National Education Assistant for India**
