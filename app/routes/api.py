"""
API routes for InternHub AI endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.models import (
    MatchRequest,
    MatchSummaryResponse,
    SkillGapResponse,
    RecommendationResponse,
    ResumeResponse,
    ConfidenceResponse
)
from app.services.gemini_service import GeminiService

router = APIRouter()
_gemini_service = None


def get_gemini_service():
    """Lazy initialization of Gemini service."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service


@router.post("/match-summary", response_model=MatchSummaryResponse)
async def get_match_summary(request: MatchRequest):
    """
    Generate internship match summary with detailed reasoning.
    
    Analyzes the compatibility between a user profile and internship position,
    providing a match score, strengths, weaknesses, and detailed reasoning.
    """
    try:
        user_profile_dict = request.user_profile.dict()
        internship_dict = request.internship.dict()
        
        gemini_service = get_gemini_service()
        result = gemini_service.generate_match_summary(user_profile_dict, internship_dict)
        
        return MatchSummaryResponse(
            match_score=float(result.get("match_score", 0.0)),
            analysis=result.get("analysis", ""),
            strengths=result.get("strengths", []),
            weaknesses=result.get("weaknesses", []),
            reasoning=result.get("reasoning", result.get("analysis", ""))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating match summary: {str(e)}")


@router.post("/skill-gap", response_model=SkillGapResponse)
async def analyze_skill_gap(request: MatchRequest):
    """
    Analyze skill gaps between user profile and internship requirements.
    
    Identifies missing skills, prioritizes them, and provides learning recommendations.
    """
    try:
        user_profile_dict = request.user_profile.dict()
        internship_dict = request.internship.dict()
        
        gemini_service = get_gemini_service()
        result = gemini_service.analyze_skill_gaps(user_profile_dict, internship_dict)
        
        return SkillGapResponse(
            missing_skills=result.get("missing_skills", []),
            explanation=result.get("explanation", ""),
            prioritized_gaps=result.get("prioritized_gaps", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing skill gaps: {str(e)}")


@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendations(request: MatchRequest):
    """
    Generate recommended text/phrasing to increase match degree.
    
    Provides specific text and phrasing that should be used in resume/profile
    to improve match with the internship position.
    """
    try:
        user_profile_dict = request.user_profile.dict()
        internship_dict = request.internship.dict()
        
        gemini_service = get_gemini_service()
        result = gemini_service.generate_recommendations(user_profile_dict, internship_dict)
        
        return RecommendationResponse(
            recommended_text=result.get("recommended_text", ""),
            improvements=result.get("improvements", []),
            explanation=result.get("explanation", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@router.post("/resume", response_model=ResumeResponse)
async def generate_resume(request: MatchRequest):
    """
    Generate ATS-optimized resume based on job description.
    
    Creates a tailored resume using recommended text that matches the job requirements
    and is optimized for Applicant Tracking Systems. Shows ATS score improvements.
    """
    try:
        user_profile_dict = request.user_profile.dict()
        internship_dict = request.internship.dict()
        
        gemini_service = get_gemini_service()
        # Generate resume with recommended text (will auto-generate recommendations if needed)
        result = gemini_service.generate_resume(user_profile_dict, internship_dict)
        
        return ResumeResponse(
            generated_resume=result.get("generated_resume", ""),
            sections=result.get("sections", {}),
            optimized_content=result.get("optimized_content", result.get("generated_resume", "")),
            keywords_used=result.get("keywords_used", []),
            formatting_suggestions=result.get("formatting_suggestions", ""),
            improvements_made=result.get("improvements_made", ""),
            ats_improvement=result.get("ats_improvement", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")


@router.post("/confidence", response_model=ConfidenceResponse)
async def calculate_confidence(request: MatchRequest):
    """
    Calculate ATS confidence score.
    
    Analyzes how well the user profile matches the job posting for
    Applicant Tracking System compatibility.
    """
    try:
        user_profile_dict = request.user_profile.dict()
        internship_dict = request.internship.dict()
        
        gemini_service = get_gemini_service()
        result = gemini_service.calculate_ats_confidence(user_profile_dict, internship_dict)
        
        return ConfidenceResponse(
            ats_score=float(result.get("ats_score", 0.0)),
            confidence_percentage=float(result.get("confidence_percentage", result.get("ats_score", 0.0))),
            analysis=result.get("analysis", ""),
            keyword_matching=result.get("keyword_matching", {}),
            improvement_suggestions=result.get("improvement_suggestions", []),
            reasoning=result.get("reasoning", result.get("analysis", ""))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating confidence: {str(e)}")


@router.get("/available-models")
async def get_available_models():
    """
    Get list of available Gemini models for your API key.
    Useful for checking which models you can use.
    """
    try:
        import google.generativeai as genai
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            return {
                "error": "API key not found",
                "available_models": [],
                "working_models": []
            }
        
        genai.configure(api_key=api_key)
        models = genai.list_models()
        
        available_models = []
        for model in models:
            model_name = model.name.replace('models/', '')
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model_name)
        
        # Test common models
        test_models = ['gemini-2.5-flash', 'gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-2.0-flash-exp']
        working_models = []
        quota_exceeded = []
        not_found = []
        
        for model_name in test_models:
            if model_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content("test")
                    working_models.append(model_name)
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "quota" in error_msg.lower():
                        quota_exceeded.append(model_name)
                    elif "404" in error_msg or "not found" in error_msg.lower():
                        not_found.append(model_name)
        
        return {
            "total_available": len(available_models),
            "available_models": available_models[:20],  # Limit to first 20
            "working_models": working_models,
            "quota_exceeded": quota_exceeded,
            "not_found": not_found,
            "current_model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            "recommendation": working_models[0] if working_models else "gemini-pro"
        }
    except Exception as e:
        return {
            "error": str(e),
            "available_models": [],
            "working_models": []
        }

