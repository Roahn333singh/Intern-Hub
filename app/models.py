"""
Pydantic models for request and response validation.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile with skills and interests."""
    skills: List[str] = Field(..., description="User's technical and soft skills")
    interests: List[str] = Field(..., description="User's interests and career preferences")
    experience: Optional[str] = Field(None, description="User's work experience (optional)")
    education: Optional[str] = Field(None, description="User's education background (optional)")


class InternshipDescription(BaseModel):
    """Internship/job description."""
    title: str = Field(..., description="Job title")
    description: str = Field(..., description="Full job description")
    requirements: List[str] = Field(..., description="Required skills/qualifications")
    company: Optional[str] = Field(None, description="Company name (optional)")


class MatchRequest(BaseModel):
    """Request model for match summary endpoint."""
    user_profile: UserProfile
    internship: InternshipDescription
    api_key: Optional[str] = Field(None, description="Optional Gemini API key (if not set via environment)")


class MatchSummaryResponse(BaseModel):
    """Response model for match summary."""
    match_score: float = Field(..., description="Match percentage (0-100)")
    analysis: str = Field(..., description="Detailed match analysis with reasoning")
    strengths: List[str] = Field(..., description="User's strengths for this position")
    weaknesses: List[str] = Field(..., description="Areas where user falls short")
    reasoning: str = Field(..., description="Step-by-step reasoning for the match score")


class SkillGapResponse(BaseModel):
    """Response model for skill gap analysis."""
    missing_skills: List[str] = Field(..., description="Skills that are missing")
    explanation: str = Field(..., description="Detailed explanation of skill gaps")
    prioritized_gaps: List[dict] = Field(..., description="Gaps prioritized by importance with reasoning")


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    recommended_text: str = Field(..., description="Recommended text/phrasing to use in resume/profile to increase match")
    improvements: List[str] = Field(..., description="Specific text improvements and better ways to phrase skills/experience")
    explanation: str = Field(..., description="Explanation of why these text changes will improve match")


class ResumeResponse(BaseModel):
    """Response model for resume generation."""
    generated_resume: str = Field(..., description="Complete generated resume text")
    sections: dict = Field(..., description="Structured resume sections")
    optimized_content: str = Field(..., description="ATS-optimized content")
    keywords_used: List[str] = Field(..., description="Keywords from JD that were incorporated")
    formatting_suggestions: str = Field(..., description="ATS-friendly formatting recommendations")
    improvements_made: str = Field(..., description="Explanation of improvements made using recommended text")
    ats_improvement: str = Field(..., description="Expected ATS score improvement explanation")


class ConfidenceResponse(BaseModel):
    """Response model for ATS confidence score."""
    ats_score: float = Field(..., description="ATS compatibility score (0-100)")
    confidence_percentage: float = Field(..., description="Confidence percentage")
    analysis: str = Field(..., description="Detailed ATS analysis")
    keyword_matching: dict = Field(..., description="Keyword matching breakdown")
    improvement_suggestions: List[str] = Field(..., description="Specific suggestions to improve ATS score")
    reasoning: str = Field(..., description="Reasoning behind the confidence score")

