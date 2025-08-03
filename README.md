# LLM SEO Evaluation Agent

A comprehensive system for querying multiple Large Language Models (LLMs) with SEO-related prompts and performing systematic auditing of their responses. The system enables cross-model comparison, trend analysis, and quality assessment of AI-generated SEO advice.

## 🎯 Project Overview

This tool allows SEO professionals, digital marketers, and content strategists to:

- **Compare AI Responses**: Submit SEO questions to multiple LLM providers (OpenAI, Claude, Perplexity, Gemini) simultaneously
- **Analyze Similarities**: Get detailed similarity analysis between different AI responses
- **Quality Assessment**: Evaluate originality, factuality, and readability of AI-generated SEO advice
- **Trend Analysis**: Track patterns and changes in AI responses over time
- **Export Results**: Download comprehensive reports and share findings

## 🏗️ Architecture

### Technology Stack
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **Backend**: FastAPI + Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Queue System**: Redis + Celery for async task processing
- **LLM Providers**: OpenAI GPT-4, Anthropic Claude, Perplexity, Google Gemini

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI       │    │   PostgreSQL    │
│   - Query Input  │◄──►│   Backend       │◄──►│   Database      │
│   - Results View │    │   - API Routes  │    │   - Responses   │
│   - Analytics    │    │   - Evaluation  │    │   - Metrics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis Queue   │
                       │   - Async Tasks │
                       │   - Rate Limiting│
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   LLM Providers │
                       │   - OpenAI      │
                       │   - Claude      │
                       │   - Perplexity  │
                       └─────────────────┘
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd llm-seo-evaluator
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/seo_llm_audit

# Redis
REDIS_URL=redis://localhost:6379

# LLM API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
GOOGLE_API_KEY=your_google_api_key

# Security
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```

## 📖 Documentation

- [Architecture Document](./docs/architecture.md) - Detailed system architecture and design decisions
- [Workflow Guide](./docs/workflow.md) - Complete end-to-end workflow implementation guide
- [API Documentation](http://localhost:8000/docs) - Interactive API documentation (when backend is running)

## 🔧 Development

### Project Structure
```
llm-seo-evaluator/
├── src/                    # Frontend React application
│   ├── components/        # React components
│   ├── services/          # API services and utilities
│   ├── hooks/             # Custom React hooks
│   ├── types/             # TypeScript type definitions
│   └── pages/             # Page components
├── backend/               # FastAPI backend (to be implemented)
├── docs/                  # Project documentation
│   ├── architecture.md    # System architecture
│   └── workflow.md        # Workflow implementation guide
└── README.md              # This file
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## 🎯 Features

### Current Features
- ✅ Modern React frontend with TypeScript
- ✅ Responsive UI with Tailwind CSS and shadcn/ui
- ✅ Component-based architecture
- ✅ Type-safe development environment

### Planned Features
- 🔄 Backend API with FastAPI
- 🔄 LLM provider integrations
- 🔄 Real-time query processing
- 🔄 Response similarity analysis
- 🔄 Quality metrics calculation
- 🔄 Export and sharing functionality
- 🔄 User authentication and history
- 🔄 Advanced analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](./docs/)
2. Search existing [issues](../../issues)
3. Create a new issue with detailed information

## 🗺️ Roadmap

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] Set up FastAPI backend structure
- [ ] Implement PostgreSQL database models
- [ ] Configure Redis for task queuing
- [ ] Create basic API endpoints

### Phase 2: LLM Integration (Week 3-4)
- [ ] Implement OpenAI provider
- [ ] Implement Claude provider
- [ ] Add response storage and retrieval
- [ ] Create query orchestration system

### Phase 3: Evaluation Engine (Week 5-6)
- [ ] Implement similarity analysis
- [ ] Add quality metrics calculation
- [ ] Create response comparison interface
- [ ] Build analytics dashboard

### Phase 4: Enhancement (Week 7-8)
- [ ] Add WebSocket real-time updates
- [ ] Implement export functionality
- [ ] Add user authentication
- [ ] Performance optimization

---

**Built with ❤️ for the SEO community**
