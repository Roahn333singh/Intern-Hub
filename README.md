# InternHub AI - AI-Powered Internship Matching System

An intelligent internship matching platform that uses Google's Gemini API to analyze candidate profiles and provide comprehensive insights including match summaries, skill gap analysis, recommendations, resume generation, and ATS confidence scores.

## Overview

InternHub AI is a FastAPI-based application that leverages advanced prompt engineering and AI reasoning to help students and job seekers understand their fit for internship positions. The system takes structured user input (skills and interests) along with internship descriptions, then generates detailed analysis through well-designed prompts focused on logical reasoning.

## Features

1. **Internship Match Summary** (`POST /api/match-summary`)
   - Comprehensive compatibility analysis with step-by-step reasoning
   - Match score (0-100) with detailed justification
   - Strengths and weaknesses breakdown
   - Chain-of-thought analysis

2. **Skill Gap Explanation** (`POST /api/skill-gap`)
   - Detailed missing skills analysis
   - Prioritized learning recommendations (CRITICAL, IMPORTANT, NICE-TO-HAVE)
   - Learning paths with time estimates
   - Explanation of skill importance for the role

3. **Recommendations** (`POST /api/recommendation`)
   - Actionable steps to increase match degree
   - Prioritized by impact on match score
   - Short-term and long-term strategies
   - Specific, implementable suggestions linked to job requirements

4. **Resume Generation** (`POST /api/resume`)
   - ATS-optimized resume based on job description
   - Structured sections (Header, Summary, Skills, Experience, Education)
   - Keyword optimization
   - ATS-friendly formatting suggestions

5. **ATS Confidence Score** (`POST /api/confidence`)
   - Confidence percentage with detailed reasoning
   - Keyword matching analysis
   - Skill alignment assessment
   - Specific improvement suggestions

## Tech Stack

- **Framework**: FastAPI (Python web framework)
- **AI/ML**: Google Gemini API (gemini-pro)
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic (data validation)
- **Environment**: python-dotenv

## Project Structure

```
Intern-Hub/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # Pydantic models for request/response
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py   # Gemini API integration with advanced prompt engineering
│   └── routes/
│       ├── __init__.py
│       └── api.py              # API endpoints
├── templates/
│   └── index.html              # Optional simple web UI
├── static/
│   └── style.css               # Basic styling
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Intern-Hub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Web UI: http://localhost:8000/

## API Documentation

### Endpoints

All endpoints accept a JSON request body with the following structure:

```json
{
  "user_profile": {
    "skills": ["Python", "JavaScript", "Machine Learning"],
    "interests": ["Web Development", "Data Science"],
    "experience": "Optional: Work experience description",
    "education": "Optional: Education background"
  },
  "internship": {
    "title": "Software Engineering Intern",
    "description": "Full job description text",
    "requirements": ["Python", "React", "Git"],
    "company": "Optional: Company name"
  }
}
```

#### 1. Match Summary

**Endpoint**: `POST /api/match-summary`

**Response**:
```json
{
  "match_score": 75.5,
  "analysis": "Detailed analysis with reasoning...",
  "strengths": ["Strong Python skills", "Relevant experience"],
  "weaknesses": ["Missing React experience"],
  "reasoning": "Step-by-step reasoning for the match score"
}
```

#### 2. Skill Gap Analysis

**Endpoint**: `POST /api/skill-gap`

**Response**:
```json
{
  "missing_skills": ["React", "Docker"],
  "explanation": "Detailed explanation of skill gaps...",
  "learning_path": [
    {
      "skill": "React",
      "priority": "CRITICAL",
      "why_it_matters": "Required for frontend development",
      "learning_resources": ["React official docs", "Online course"],
      "estimated_time": "4-6 weeks",
      "practical_steps": ["Build a project", "Practice daily"]
    }
  ],
  "prioritized_gaps": [...]
}
```

#### 3. Recommendations

**Endpoint**: `POST /api/recommendation`

**Response**:
```json
{
  "recommendations": ["Learn React", "Build a portfolio project"],
  "actionable_steps": [
    {
      "step": "Complete React tutorial",
      "priority": "HIGH",
      "timeframe": "2 weeks",
      "linked_to_requirement": "React frontend development",
      "expected_impact": "Increases match by 15%"
    }
  ],
  "short_term": ["Quick wins..."],
  "long_term": ["Strategic moves..."],
  "impact_analysis": "Analysis of expected improvements"
}
```

#### 4. Resume Generation

**Endpoint**: `POST /api/resume`

**Response**:
```json
{
  "generated_resume": "Complete resume text...",
  "sections": {
    "header": "Name and contact",
    "summary": "Professional summary",
    "skills": "Skills section",
    "experience": "Experience section",
    "education": "Education section"
  },
  "optimized_content": "ATS-optimized version",
  "keywords_used": ["Python", "React", "Git"],
  "formatting_suggestions": "Formatting recommendations"
}
```

#### 5. ATS Confidence Score

**Endpoint**: `POST /api/confidence`

**Response**:
```json
{
  "ats_score": 82.5,
  "confidence_percentage": 82.5,
  "analysis": "Detailed ATS analysis...",
  "keyword_matching": {
    "matched_keywords": ["Python", "React"],
    "missing_keywords": ["Docker"],
    "match_percentage": 75.0,
    "critical_missing": ["Docker"]
  },
  "improvement_suggestions": ["Add Docker to skills"],
  "reasoning": "Step-by-step reasoning for confidence score"
}
```

## Prompt Design Approach

The core differentiator of this application is sophisticated prompt engineering. Each prompt is designed with:

1. **Reasoning Chains**: Prompts ask Gemini to think step-by-step, showing the analysis process
2. **Structured Analysis**: Requests organized, categorized responses with clear sections
3. **Justification**: Always asks for reasoning behind scores/ratings
4. **Context Awareness**: Prompts reference both user profile and job requirements simultaneously
5. **Actionable Output**: Focuses on practical, implementable recommendations
6. **Example-Driven**: Includes examples in prompts to guide output format

### Example Prompt Structure

Each prompt follows this pattern:
- **Context Setting**: Define the role (expert counselor, career coach, etc.)
- **Input Presentation**: Clearly format user profile and job details
- **Task Definition**: Explicitly state what analysis is needed
- **Step-by-Step Instructions**: Break down the analysis into logical steps
- **Output Format**: Specify JSON structure with required fields
- **Quality Guidelines**: Emphasize specificity, actionability, and reasoning

## Assumptions

- Gemini API key is provided via environment variable
- User inputs (skills, interests) are provided in English
- Internship descriptions are in English
- API responses are in JSON format
- Focus on prompt quality over complex system design
- No authentication required (as per assignment requirements)
- Simple error handling for API failures

## Important Notes

- **Processing Time**: AI processing may take 10-30 seconds depending on the complexity of the analysis. Please be patient while the AI processes your request. The system uses advanced prompt engineering which requires more processing time to ensure high-quality, detailed responses.

## Deployment

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GEMINI_API_KEY=your_key`



## Core Working Concepts

1. **Prompt Engineering**: The application uses carefully crafted prompts that guide Gemini to provide structured, reasoned responses
2. **Chain-of-Thought Reasoning**: Prompts explicitly ask for step-by-step analysis, improving response quality
3. **Structured Output**: All responses follow consistent JSON schemas defined by Pydantic models
4. **Error Handling**: Graceful fallbacks ensure the API always returns valid responses even if Gemini API fails
5. **Modular Design**: Service layer separates AI logic from API routes, making the code maintainable

## Future Enhancements

- Support for multiple resume formats
- Batch processing for multiple internships
- Caching for frequently requested analyses
- User authentication and profile storage
- Historical match tracking

## Author Information

- **Name**: [Rohan singh]
- **Enrollment**: [E22CSEU0095]
- **Batch**: [4]
- **University**: [Bennett University]
- **Role**: AI-focused role candidate

---

**Note**: This application focuses on prompt design and reasoning quality. The implementation prioritizes clear, maintainable code and sophisticated AI interactions over complex system architecture.
