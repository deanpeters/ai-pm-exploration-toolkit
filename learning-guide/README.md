# AI PM Learning Guide 🎓

**Interactive HTML5 learning platform for product managers to master AI tools and techniques**

## Overview

The AI PM Learning Guide is a Progressive Web App (PWA) that transforms product managers from AI-curious to AI-confident through structured, hands-on learning experiences.

### Key Features

- **🎯 PM-Centric Organization** - Learning paths based on real product management use cases
- **📱 Progressive Web App** - Works offline, installable on any device
- **📊 Progress Tracking** - Local storage tracks your learning journey  
- **🔍 Smart Search** - Find content by topic, tool, or use case
- **⚡ Interactive Elements** - Copy-paste code blocks, live demos, progress indicators
- **🎨 Modern Design** - Professional, confidence-building interface

## Learning Structure

### Primary Organization: PM Use Cases + Progressive Difficulty

**5 Main Learning Tracks:**
1. **✍️ AI Collaboration** - "I need to write better product briefs"
2. **🔍 Research & Analysis** - "I need competitive intelligence fast"  
3. **🎨 Visual Building** - "I need to demo concepts without engineering"
4. **🧪 Experimentation** - "I need to validate assumptions with data"
5. **🎬 Storytelling** - "I need to convince stakeholders"

### Progressive Learning Path
Each track follows the same evidence-based structure:
- **🎓 Learn** (15 min) - Basic concepts and first success
- **⚡ Practice** (30 min) - Guided hands-on exercises  
- **🚀 Apply** (60 min) - Real-world project scenarios
- **🎯 Master** (ongoing) - Advanced techniques and combinations

### Cross-Reference Navigation
- **By Tool** - "Show me everything about Aider"
- **By Learning Topic** - "Show me all AI prompting techniques"
- **By Time Available** - "I have 15 minutes" vs "I have 2 hours"
- **By Skill Level** - Beginner, Intermediate, Advanced

## File Structure

```
learning-guide/
├── index.html              # Main homepage with track selection
├── manifest.json           # PWA configuration
├── css/
│   ├── styles.css          # Main stylesheet with design system
│   └── track.css           # Track-specific styling
├── js/
│   ├── learning-guide.js   # Homepage functionality and search
│   └── track.js            # Track progression and progress tracking
├── tracks/
│   ├── collaboration.html  # AI Collaboration track (completed)
│   ├── research.html       # Research & Analysis track
│   ├── visual.html         # Visual Building track
│   ├── experimentation.html # Data & Experimentation track
│   └── storytelling.html   # Storytelling & Presentation track
└── assets/
    ├── favicon.svg         # App icon
    └── (screenshots, icons for PWA)
```

## Technology Stack

- **HTML5** - Semantic, accessible markup
- **CSS3** - Modern responsive design with CSS Grid/Flexbox
- **Vanilla JavaScript** - Fast, lightweight interactions
- **Local Storage** - Progress tracking without accounts
- **Progressive Web App** - Offline capability and app-like experience

## Design System

### Colors
- **Primary**: #2563eb (Blue) - Trust, professionalism
- **Secondary**: #10b981 (Green) - Success, progress
- **Accent**: #f59e0b (Amber) - Attention, warnings
- **Grays**: Full spectrum for text and backgrounds

### Typography
- **Sans-serif**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Monospace**: 'SF Mono', Monaco, 'Cascadia Code' (for code blocks)

### Key Components
- **Track Cards** - Hover effects, progress indicators
- **Module Cards** - Expandable content, lock/unlock states
- **Code Blocks** - Copy-paste functionality, syntax highlighting
- **Progress Bars** - Visual feedback for completion
- **Interactive Elements** - Buttons, search, modal dialogs

## Usage

### Local Development
```bash
# Serve locally (Python)
cd learning-guide
python -m http.server 8000

# Or with Node.js
npx serve .

# Open http://localhost:8000
```

### Integration with Toolkit
The learning guide is designed to work alongside the main AI PM Toolkit:

1. **Commands Integration** - References actual toolkit commands
2. **Hands-on Practice** - Exercises use real toolkit tools  
3. **Progressive Enhancement** - Builds skills for using the full toolkit
4. **Seamless Transition** - From learning to real product management work

## Content Integration

### Existing Playbook Transformation
The learning guide transforms existing playbooks into interactive modules:

- **AIDER_PLAYBOOK.md** → **AI Collaboration Track**
- **WORKFLOW_PLAYBOOK.md** → **Visual Building Track**  
- **MARKET_RESEARCH_PLAYBOOK.md** → **Research & Analysis Track**

### Learning Science Features
- **Spaced Repetition** - Reminders to review concepts
- **Progressive Disclosure** - Information revealed as needed
- **Immediate Feedback** - Real-time progress and validation
- **Social Learning** - Community examples and sharing

## Progressive Web App Features

### Offline Capability
- **Service Worker** - Cache resources for offline use
- **Local Storage** - Progress tracking without internet
- **App-like Experience** - Installable on home screen

### Performance Optimizations
- **Lazy Loading** - Content loaded as needed
- **Optimized Images** - WebP format with fallbacks
- **Minimal JavaScript** - Fast initial load times
- **CSS Grid/Flexbox** - Efficient layouts without frameworks

## Accessibility

- **Semantic HTML** - Screen reader friendly
- **Keyboard Navigation** - Full functionality without mouse
- **Color Contrast** - WCAG AA compliance
- **Focus Management** - Clear visual indicators
- **Alt Text** - Descriptive text for all images

## Browser Support

- **Modern Browsers** - Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **Mobile Responsive** - iOS Safari, Chrome Mobile, Samsung Internet
- **Progressive Enhancement** - Graceful degradation for older browsers

## Future Enhancements

### Planned Features
- **Video Integration** - Embedded walkthroughs and demos
- **Community Features** - Share progress and examples
- **Advanced Analytics** - Learning pattern insights
- **Personalization** - Adaptive content based on progress
- **Integration APIs** - Connect with external PM tools

### Expansion Opportunities
- **Team Learning** - Multi-user progress tracking
- **Certification** - Completion badges and certificates
- **Advanced Tracks** - Specialized PM domains
- **Mobile App** - Native iOS/Android versions

## Maintenance

### Content Updates
- **Modular Structure** - Easy to add new tracks and modules
- **JSON Configuration** - Content separated from presentation
- **Version Control** - Track changes and rollback capability

### Performance Monitoring
- **Core Web Vitals** - Loading, interactivity, visual stability
- **User Analytics** - Completion rates and engagement
- **Error Tracking** - JavaScript errors and failed requests

---

**The AI PM Learning Guide bridges the gap between AI-curious and AI-confident product managers through structured, hands-on learning experiences that build real-world skills.**