# Assumptions and Design Decisions

This document outlines the assumptions and design decisions made in the InternHub AI application.

## Core Assumptions

### 1. **Input Format**
- **Assumption**: Users provide structured input (skills and interests as lists, not PDF resumes)
- **Reasoning**: Structured data is easier to process and analyze programmatically
- **Impact**: No PDF parsing required, simpler implementation

### 2. **Language**
- **Assumption**: All inputs (skills, interests, job descriptions) are in English
- **Reasoning**: Focus on English-speaking markets, simplifies NLP processing
- **Impact**: No multi-language support needed

### 3. **API Key Management**
- **Assumption**: Gemini API key is provided via environment variable (`.env` file)
- **Reasoning**: Standard security practice, keeps keys out of code
- **Impact**: Users must set up `.env` file before using


## ATS Confidence Score Calculation

The ATS (Applicant Tracking System) confidence score is calculated based on the following weighted factors:

### **Keyword Match (40% weight)**
- **What it measures**: How many keywords from the job description appear in the candidate's profile
- **Components**:
  - Keywords from the job description (skills, technologies, tools, qualifications)
  - Which keywords appear in the candidate's profile
  - Keyword match percentage
  - Missing critical keywords
- **Reasoning**: ATS systems heavily rely on keyword matching to filter candidates
- **Impact**: Highest weight because keywords are the primary ATS filtering mechanism

### **Skill Alignment (30% weight)**
- **What it measures**: How well the candidate's skills match the required skills
- **Components**:
  - Candidate skills vs required skills comparison
  - Skill level match (entry-level, intermediate, advanced)
  - Skill gaps that could cause ATS rejection
  - Transferable skills recognition
- **Reasoning**: Skills are the core requirement for most positions
- **Impact**: Second highest weight as skills directly indicate job fit

### **Profile Completeness (20% weight)**
- **What it measures**: How well-structured and complete the profile is
- **Components**:
  - How well-structured the profile is
  - Standard section headings presence
  - Keyword placement and density
  - Formatting compatibility with ATS systems
- **Reasoning**: Well-structured profiles parse better in ATS systems
- **Impact**: Moderate weight - structure affects ATS parsing success

### **Overall Fit (10% weight)**
- **What it measures**: General alignment with the role beyond just keywords and skills
- **Components**:
  - General alignment with the role
  - Contextual fit assessment
- **Reasoning**: Provides holistic view beyond technical matching
- **Impact**: Lowest weight - supplementary factor

### **Total Score Calculation**
```
ATS Score = (Keyword Match × 0.40) + 
            (Skill Alignment × 0.30) + 
            (Profile Completeness × 0.20) + 
            (Overall Fit × 0.10)
```

**Example**: If a candidate scores:
- Keyword Match: 80%
- Skill Alignment: 70%
- Profile Completeness: 90%
- Overall Fit: 75%

**Final ATS Score** = (80 × 0.40) + (70 × 0.30) + (90 × 0.20) + (75 × 0.10) = **77.5/100**

## Design Decisions

### 1. **Separate Endpoints for Each Feature**
- **Decision**: Each analysis type (match, skill gap, recommendations, resume, ATS) is a separate endpoint
- **Reasoning**: 
  - Allows users to get specific insights without running all analyses
  - Better API design (single responsibility)
  - Easier to test and maintain
- **Trade-off**: Multiple API calls needed for complete analysis

### 2. **Automatic Recommendation Integration in Resume**
- **Decision**: Resume generation automatically fetches and uses recommendations
- **Reasoning**: 
  - Ensures resume uses best practices
  - Reduces user steps
  - Guarantees consistency
- **Trade-off**: Resume generation takes longer (two AI calls)

### 3. **Text-Based Recommendations (Not Action Steps)**
- **Decision**: Recommendations focus on text/phrasing improvements, not learning resources
- **Reasoning**: 
  - Assignment requirement
  - More actionable for immediate resume improvement
  - Focuses on what user can change now
- **Trade-off**: Doesn't provide long-term skill development paths

### 4. **Standard Resume Format**
- **Decision**: Generated resumes follow strict standard formatting
- **Reasoning**: 
  - ATS systems require standard formats
  - Professional appearance
  - Industry best practices
- **Trade-off**: Less creative flexibility

### 5. **No Learning Resources in Skill Gap**
- **Decision**: Skill gap analysis only identifies gaps, doesn't provide learning paths
- **Reasoning**: 
  - Assignment requirement
  - Keeps focus on immediate matching
  - Simpler output
- **Trade-off**: Users must find learning resources elsewhere

### 6. **Model Selection**
- **Decision**: Default to `gemini-2.5-flash` with fallback to `gemini-pro`
- **Reasoning**: 
  - Latest model for best performance
  - Fallback ensures reliability
  - User can override via environment variable
- **Trade-off**: May have quota limits on newer models

### 7. **JSON Response Format**
- **Decision**: All endpoints return structured JSON
- **Reasoning**: 
  - Easy to parse programmatically
  - Consistent API design
  - Works well with frontend frameworks
- **Trade-off**: Less human-readable than plain text

### 8. **Prompt Engineering Focus**
- **Decision**: Heavy emphasis on sophisticated prompt design
- **Reasoning**: 
  - Assignment requirement (major focus on prompt design)
  - Better AI outputs through better instructions
  - Demonstrates understanding of AI capabilities
- **Trade-off**: More complex prompts, but better results

## Limitations

1. **No PDF Upload**: Only structured text input accepted
2. **English Only**: No multi-language support
3. **No Authentication**: Public API (not production-ready)
4. **API Rate Limits**: Subject to Gemini API quota limits
5. **Single Model**: Uses one AI model (no ensemble)
6. **No Caching**: Each request calls AI API (no result caching)
7. **No History**: Doesn't store previous analyses

## Future Enhancements (Not Implemented)

- PDF resume parsing
- Multi-language support
- User authentication and profiles
- Result caching
- Analysis history
- Batch processing
- Multiple model comparison
- Learning resource recommendations

---

**Note**: These assumptions and design decisions were made to balance functionality, simplicity, and assignment requirements. The application focuses on core AI-powered matching features with emphasis on prompt engineering quality.

