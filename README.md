# AI-Powered Content & Research System

A Python-based AI automation solution using CrewAI for content creation and customer support. The system leverages intelligent agent workflows to generate blog posts and handle customer inquiries.

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
# Add your OpenAI API key to .env
```

## ✨ Key Features

### 🖋️ Content Research & Generation

- **AI Research Team**
  - Planner: Develops content strategies and outlines
  - Writer: Creates detailed blog posts based on outlines
  - Editor: Reviews and refines content for quality

- **Output Capabilities**
  - Markdown-formatted blog posts
  - SEO-optimized content
  - Structured sections with proper headers

### 🛎️ Customer Support System

- **Support Team**
  - Senior Support Representative: Handles customer inquiries
  - Quality Assurance Specialist: Reviews support responses
  
- **Support Features**
  - Website documentation integration
  - Detailed response generation
  - Quality assurance review process

### 🤝 Customer Outreach System

- **Sales Team**
  - Sales Representative: Identifies and profiles high-value leads
  - Lead Sales Representative: Crafts personalized communications
  - Quality Assurance Agent: Reviews and validates outreach communications

- **Outreach Features**
  - Lead profiling and analysis
  - Personalized email campaign generation
  - Sentiment analysis for communications
  - Quality assurance review process

## 💻 Usage Examples

### Generate Research Content
```bash
uv run res
```

### Handle Customer Support
```bash
uv run customer
```

## 🛠️ Technical Stack

- CrewAI Framework
- CrewAI Tools
- Python 3.10+
- UV Package Manager

## ⚙️ Configuration

### Prerequisites
- Python 3.10-3.12
- OpenAI API key
- UV package manager

### Project Structure
```
src/course/
├── research.py    # Content generation system
└── customer.py    # Customer support system
```

### Output Files
- `blog_post.md`: Generated content output
- `customer.md`: Support response output

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch
3. Submit a PR with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
