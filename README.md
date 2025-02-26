# AI-Powered Multi-Agent Automation System

A Python-based AI automation solution using CrewAI for content creation, customer support, event planning, and financial analysis. The system leverages intelligent agent workflows to handle various business operations.

## 🚀 Quick Start

```bash
# Install UV package manager (if not present)
pip install uv

# Clone and setup
git clone https://github.com/yourrepo/course.git
cd course

# Install dependencies
uv run sync

# Configure environment
cp .env.example .env
# Add your API keys to .env
```

## ✨ Key Features

### 🖋️ Content Research & Generation

- **AI Research Team**
  - Planner: Develops content strategies and outlines
  - Writer: Creates detailed blog posts based on outlines
  - Editor: Reviews and refines content for quality

### 🛎️ Customer Support System

- **Support Team**
  - Senior Support Representative: Handles customer inquiries
  - Quality Assurance Specialist: Reviews support responses

### 🤝 Customer Outreach System

- **Sales Team**
  - Sales Representative: Identifies and profiles high-value leads
  - Lead Sales Representative: Crafts personalized communications

### 📅 Event Planning System

- **Event Team**
  - Venue Coordinator: Identifies and books appropriate venues
  - Logistics Manager: Handles catering and equipment
  - Marketing Communications Agent: Promotes events and engages participants

### 📊 Financial Analysis System

- **Trading Team**
  - Data Analyst: Monitors and analyzes market data
  - Trading Strategy Developer: Develops trading strategies
  - Trade Advisor: Suggests execution strategies
  - Risk Advisor: Evaluates trading risks

## 💻 Usage Examples

### Generate Research Content
```bash
uv run res
```

### Handle Customer Support
```bash
uv run customer
```

### Manage Customer Outreach
```bash
uv run outreach
```

### Plan Events
```bash
uv run event
```

### Run Financial Analysis
```bash
uv run multiAgent
```

## 🛠️ Technical Stack

- CrewAI Framework
- CrewAI Tools
- Python 3.10+
- UV Package Manager
- Serper API for web search
- Various specialized tools for each system

## ⚙️ Configuration

### Prerequisites
- Python 3.10-3.12
- Required API keys (Serper, etc.)
- UV package manager

### Project Structure
```
src/course/
├── research.py          # Content generation system
├── customer.py         # Customer support system
├── customer_outreach.py # Sales outreach system
├── event_planner.py    # Event planning system
└── multi_agent.py      # Financial analysis system
```

### Output Files
- `blog_post.md`: Generated content output
- `customer.md`: Support response output
- `customer_outreach.md`: Sales communications
- `marketing_report.md`: Event marketing reports
- `multi_agent_output.md`: Financial analysis reports
- `venue_details.json`: Event venue information

## 🔑 Key Features by System

### Content Research System
- SEO-optimized content generation
- Structured blog post creation
- Multi-stage review process

### Customer Support System
- Documentation integration
- Detailed response generation
- Quality assurance review

### Customer Outreach System
- Lead profiling and analysis
- Personalized email campaigns
- Sentiment analysis

### Event Planning System
- Venue selection and booking
- Logistics coordination
- Marketing campaign management
- Attendee engagement strategies

### Financial Analysis System
- Real-time market data analysis
- Trading strategy development
- Risk assessment
- Execution planning

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch
3. Submit a PR with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
