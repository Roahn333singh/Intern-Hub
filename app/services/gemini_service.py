"""
Gemini API service with advanced prompt engineering.
Focus on reasoning, chain-of-thought, and structured analysis.
"""
import os
import json
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    """Service for interacting with Gemini API with sophisticated prompts."""
    
    def __init__(self, api_key: str = None):
        """Initialize Gemini client with API key.
        
        Args:
            api_key: Optional API key. If not provided, uses environment variable.
        """
        # Use provided API key, or try GEMINI_API_KEY, then fallback to GOOGLE_API_KEY
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set. "
                    "Please create a .env file in the project root with: GEMINI_API_KEY=your_api_key_here"
                )
        
        genai.configure(api_key=self.api_key)
        # Model can be configured via GEMINI_MODEL env var
        # Default: gemini-2.5-flash (latest flash model)
        # Alternative: gemini-pro (most stable, good free tier)
        # Note: gemini-2.0-flash-exp may have limited quota
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        try:
            self.model = genai.GenerativeModel(model_name)
            print(f"✓ Using model: {model_name}")
        except Exception as e:
            # Try fallback models in order of preference (gemini-pro has best free tier quota)
            fallback_models = ["gemini-pro", "gemini-1.5-pro"]
            print(f"Warning: Could not load model {model_name}, trying fallbacks... Error: {e}")
            model_loaded = False
            for fallback in fallback_models:
                try:
                    self.model = genai.GenerativeModel(fallback)
                    print(f"✓ Using fallback model: {fallback}")
                    model_loaded = True
                    break
                except Exception as e2:
                    continue
            
            if not model_loaded:
                raise ValueError(
                    f"Could not initialize any Gemini model. Tried {model_name} and fallbacks: {fallback_models}. "
                    f"Please check your API key and available models. You may need to enable the model in Google AI Studio."
                )
    
    def _extract_json_from_response(self, text: str) -> Dict[str, Any]:
        """Extract JSON from Gemini response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        original_text = text
        
        # Try to extract JSON from markdown code blocks
        if "```json" in text:
            # Find the JSON block
            start = text.find("```json")
            end = text.find("```", start + 7)
            if end != -1:
                text = text[start + 7:end].strip()
        elif "```" in text:
            # Try to find any code block
            parts = text.split("```")
            if len(parts) >= 3:
                # Take the content between first and second ```
                text = parts[1].strip()
                # Remove language identifier if present (e.g., "json" at the start)
                if text.startswith("json"):
                    text = text[4:].strip()
        
        # Try to find JSON object in the text
        if not text.strip().startswith("{"):
            # Look for JSON object pattern
            start_brace = text.find("{")
            if start_brace != -1:
                # Find matching closing brace
                brace_count = 0
                end_brace = start_brace
                for i in range(start_brace, len(text)):
                    if text[i] == "{":
                        brace_count += 1
                    elif text[i] == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            end_brace = i + 1
                            break
                if end_brace > start_brace:
                    text = text[start_brace:end_brace]
        
        # Clean up the text
        text = text.strip()
        
        # Try to parse JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract just the JSON part more aggressively
            # Look for the first { and last }
            start_idx = text.find("{")
            if start_idx != -1:
                # Find the last }
                last_idx = text.rfind("}")
                if last_idx > start_idx:
                    try:
                        json_text = text[start_idx:last_idx + 1]
                        return json.loads(json_text)
                    except json.JSONDecodeError:
                        pass
            
            # If all parsing fails, return the text as-is in a structured format
            return {"raw_response": original_text}
    
    def generate_match_summary(self, user_profile: Dict, internship: Dict) -> Dict[str, Any]:
        """
        Generate internship match summary with chain-of-thought reasoning.
        """
        prompt = f"""You are an expert career counselor analyzing the match between a candidate and an internship position.

CANDIDATE PROFILE:
Skills: {', '.join(user_profile.get('skills', []))}
Interests: {', '.join(user_profile.get('interests', []))}
Experience: {user_profile.get('experience', 'Not provided')}
Education: {user_profile.get('education', 'Not provided')}

INTERNSHIP DETAILS:
Title: {internship.get('title', 'N/A')}
Company: {internship.get('company', 'N/A')}
Description: {internship.get('description', '')}
Requirements: {', '.join(internship.get('requirements', []))}

TASK: Analyze the match between the candidate and this internship position.

Please provide your analysis using the following step-by-step reasoning approach:

STEP 1: Skill Overlap Analysis
- Identify which candidate skills match the job requirements
- Calculate the percentage of required skills that the candidate possesses
- Note any skills that are partially relevant

STEP 2: Interest Alignment
- Assess how well the candidate's interests align with the role
- Consider if the role would be engaging for this candidate

STEP 3: Experience Relevance
- Evaluate how the candidate's experience relates to the position
- Identify transferable skills and experiences

STEP 4: Match Score Calculation
- Calculate a match score from 0-100
- Provide clear justification for the score
- Consider: skill match (40%), interest alignment (20%), experience relevance (30%), overall fit (10%)

STEP 5: Strengths Identification
- List 3-5 key strengths the candidate brings to this role
- Be specific and reference actual skills/experiences

STEP 6: Weaknesses/Gaps
- Identify 2-4 areas where the candidate falls short
- Be constructive and specific

Please respond ONLY with valid JSON in the following format (do NOT wrap in markdown code blocks):
{{
    "match_score": <number 0-100>,
    "analysis": "<detailed analysis with step-by-step reasoning>",
    "strengths": ["<strength1>", "<strength2>", ...],
    "weaknesses": ["<weakness1>", "<weakness2>", ...],
    "reasoning": "<step-by-step reasoning for the match score>"
}}

IMPORTANT: Respond with ONLY the JSON object, no markdown formatting, no code blocks, no additional text before or after the JSON.

Focus on providing detailed, actionable reasoning. Be specific and reference the actual skills and requirements."""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json_from_response(response.text)
            
            # If extraction returned raw_response, try to parse it manually
            if "raw_response" in result and len(result) == 1:
                raw_text = result["raw_response"]
                # Try one more time with better extraction
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw_text, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group(0))
                    except:
                        pass
            
            # Ensure all required fields are present
            if "match_score" not in result or result.get("match_score") == 0:
                # Try to extract match_score from the response text if available
                if isinstance(result.get("raw_response"), str):
                    import re
                    score_match = re.search(r'"match_score"\s*:\s*(\d+(?:\.\d+)?)', result["raw_response"])
                    if score_match:
                        result["match_score"] = float(score_match.group(1))
                    else:
                        result["match_score"] = 0.0
                else:
                    result["match_score"] = float(result.get("match_score", 0.0))
            else:
                result["match_score"] = float(result["match_score"])
            
            if "analysis" not in result or not result["analysis"]:
                result["analysis"] = response.text if "raw_response" not in result else result.get("raw_response", response.text)
            
            if "strengths" not in result or not isinstance(result["strengths"], list):
                # Try to extract strengths array
                if isinstance(result.get("raw_response"), str):
                    import re
                    strengths_match = re.search(r'"strengths"\s*:\s*\[(.*?)\]', result["raw_response"], re.DOTALL)
                    if strengths_match:
                        # Try to parse the array
                        try:
                            strengths_str = "[" + strengths_match.group(1) + "]"
                            strengths = json.loads(strengths_str)
                            result["strengths"] = strengths if isinstance(strengths, list) else []
                        except:
                            result["strengths"] = []
                    else:
                        result["strengths"] = []
                else:
                    result["strengths"] = []
            
            if "weaknesses" not in result or not isinstance(result["weaknesses"], list):
                # Try to extract weaknesses array
                if isinstance(result.get("raw_response"), str):
                    import re
                    weaknesses_match = re.search(r'"weaknesses"\s*:\s*\[(.*?)\]', result["raw_response"], re.DOTALL)
                    if weaknesses_match:
                        try:
                            weaknesses_str = "[" + weaknesses_match.group(1) + "]"
                            weaknesses = json.loads(weaknesses_str)
                            result["weaknesses"] = weaknesses if isinstance(weaknesses, list) else []
                        except:
                            result["weaknesses"] = []
                    else:
                        result["weaknesses"] = []
                else:
                    result["weaknesses"] = []
            
            if "reasoning" not in result or not result["reasoning"]:
                result["reasoning"] = result.get("analysis", "")
            
            return result
        except Exception as e:
            error_msg = str(e)
            # Check for quota errors
            if "429" in error_msg or "quota" in error_msg.lower() or "Quota exceeded" in error_msg:
                return {
                    "match_score": 0.0,
                    "analysis": f"API Quota Exceeded: You've reached your free tier limit for this model. Please wait a few minutes and try again, or use a different model by setting GEMINI_MODEL=gemini-pro in your .env file. For more info: https://ai.google.dev/gemini-api/docs/rate-limits",
                    "strengths": [],
                    "weaknesses": [],
                    "reasoning": ""
                }
            return {
                "match_score": 0.0,
                "analysis": f"Error generating match summary: {error_msg}",
                "strengths": [],
                "weaknesses": [],
                "reasoning": ""
            }
    
    def analyze_skill_gaps(self, user_profile: Dict, internship: Dict) -> Dict[str, Any]:
        """
        Analyze skill gaps with prioritized recommendations.
        """
        prompt = f"""You are a career development expert analyzing skill gaps between a candidate and an internship position.

CANDIDATE PROFILE:
Skills: {', '.join(user_profile.get('skills', []))}
Interests: {', '.join(user_profile.get('interests', []))}
Experience: {user_profile.get('experience', 'Not provided')}

INTERNSHIP REQUIREMENTS:
Title: {internship.get('title', 'N/A')}
Required Skills: {', '.join(internship.get('requirements', []))}
Job Description: {internship.get('description', '')}

TASK: Identify skill gaps and provide prioritized learning recommendations.

Please follow this structured analysis:

STEP 1: Required Skills Inventory
- List all skills explicitly mentioned in the requirements
- Identify implicit skills needed based on the job description

STEP 2: Gap Identification
- Compare candidate skills against required skills
- Identify missing skills
- Note skills that are partially present but need improvement

STEP 3: Prioritization
- Categorize gaps as: CRITICAL (must-have), IMPORTANT (highly valuable), NICE-TO-HAVE (beneficial)
- Explain why each skill matters for this specific role
- Consider the role's core responsibilities

Please respond in the following JSON format:
{{
    "missing_skills": ["<skill1>", "<skill2>", ...],
    "explanation": "<detailed explanation of why these gaps matter and their impact>",
    "prioritized_gaps": [
        {{
            "skill": "<skill name>",
            "priority_level": "<CRITICAL|IMPORTANT|NICE-TO-HAVE>",
            "importance_reasoning": "<why this is important for this role>",
            "impact_if_missing": "<what happens if this skill is missing>"
        }}
    ]
}}

Be specific, actionable, and prioritize based on the actual job requirements."""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json_from_response(response.text)
            
            # Ensure required fields
            if "missing_skills" not in result:
                result["missing_skills"] = []
            if "explanation" not in result:
                result["explanation"] = response.text
            if "prioritized_gaps" not in result:
                result["prioritized_gaps"] = []
            
            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "Quota exceeded" in error_msg:
                error_msg = "API Quota Exceeded. Please wait a few minutes or use GEMINI_MODEL=gemini-pro in .env"
            return {
                "missing_skills": [],
                "explanation": f"Error analyzing skill gaps: {error_msg}",
                "prioritized_gaps": []
            }
    
    def generate_recommendations(self, user_profile: Dict, internship: Dict) -> Dict[str, Any]:
        """
        Generate recommended text/phrasing to increase match degree.
        Focus on what text the user should use in their resume/profile.
        """
        prompt = f"""You are a resume optimization expert helping a candidate improve their resume text to better match an internship position.

CANDIDATE PROFILE:
Skills: {', '.join(user_profile.get('skills', []))}
Interests: {', '.join(user_profile.get('interests', []))}
Experience: {user_profile.get('experience', 'Not provided')}
Education: {user_profile.get('education', 'Not provided')}

INTERNSHIP DETAILS:
Title: {internship.get('title', 'N/A')}
Requirements: {', '.join(internship.get('requirements', []))}
Description: {internship.get('description', '')}

TASK: Provide recommended text and phrasing that the candidate should use in their resume/profile to increase their match with this position.

Focus on:
1. How to better phrase existing skills to match job requirements
2. Better ways to describe experience that aligns with the job
3. Keywords and terminology from the job description to incorporate
4. How to present skills/experience in a way that ATS systems will recognize
5. Text improvements that will increase ATS score

Please respond in the following JSON format:
{{
    "recommended_text": "<comprehensive recommended text that should be used in resume/profile. Include improved phrasing for skills, experience descriptions, and summary. Make it ready to use in a resume>",
    "improvements": [
        "<specific improvement 1: e.g., 'Change \"know Python\" to \"Proficient in Python programming with experience in...\"'>",
        "<specific improvement 2: e.g., 'Add keyword \"agile methodology\" when describing team experience'>",
        "<specific improvement 3: e.g., 'Reframe experience to emphasize \"collaborative software development\" instead of just \"worked on projects\"'>"
    ],
    "explanation": "<detailed explanation of why these text changes will improve the match score and ATS compatibility. Explain how the recommended text better aligns with job requirements>"
}}

Be specific about the exact text to use. Provide ready-to-use phrases and descriptions that will improve ATS matching."""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json_from_response(response.text)
            
            # Ensure required fields
            if "recommended_text" not in result:
                result["recommended_text"] = response.text
            if "improvements" not in result:
                result["improvements"] = []
            if "explanation" not in result:
                result["explanation"] = response.text
            
            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "Quota exceeded" in error_msg:
                error_msg = "API Quota Exceeded. Please wait a few minutes or use GEMINI_MODEL=gemini-pro in .env"
            return {
                "recommended_text": "",
                "improvements": [],
                "explanation": f"Error generating recommendations: {error_msg}"
            }
    
    def generate_resume(self, user_profile: Dict, internship: Dict, recommended_text: str = None) -> Dict[str, Any]:
        """
        Generate ATS-optimized resume based on job description.
        Uses recommended text to improve the resume and show ATS score improvements.
        """
        # If recommended text not provided, generate it first
        if not recommended_text:
            recommendations = self.generate_recommendations(user_profile, internship)
            recommended_text = recommendations.get("recommended_text", "")
        
        prompt = f"""You are a professional resume writer specializing in ATS (Applicant Tracking System) optimization.

CANDIDATE INFORMATION:
Skills: {', '.join(user_profile.get('skills', []))}
Interests: {', '.join(user_profile.get('interests', []))}
Experience: {user_profile.get('experience', 'Not provided')}
Education: {user_profile.get('education', 'Not provided')}

TARGET POSITION:
Title: {internship.get('title', 'N/A')}
Company: {internship.get('company', 'N/A')}
Job Description: {internship.get('description', '')}
Required Skills: {', '.join(internship.get('requirements', []))}

RECOMMENDED TEXT TO USE:
{recommended_text if recommended_text else "Use optimized phrasing that matches job requirements"}

TASK: Create an ATS-optimized resume tailored to this specific position following STANDARD RESUME FORMAT. IMPORTANT: Use the recommended text provided above to improve the resume. Incorporate the recommended phrasing, keywords, and improvements.

STANDARD RESUME FORMAT REQUIREMENTS:
1. Section Order (MUST FOLLOW THIS ORDER):
   - Header (Name, Phone, Email, Location - one line each or separated by |)
   - Professional Summary (2-4 sentences, no bullet points)
   - Skills (categorized if needed: Technical Skills, Soft Skills, etc.)
   - Experience (if provided)
   - Education
   - Additional Sections (Projects, Certifications, etc. - only if relevant)

2. Standard Section Headings (USE EXACTLY):
   - "PROFESSIONAL SUMMARY" or "SUMMARY"
   - "SKILLS" or "TECHNICAL SKILLS"
   - "EXPERIENCE" or "WORK EXPERIENCE" or "PROFESSIONAL EXPERIENCE"
   - "EDUCATION"
   - "PROJECTS" (if applicable)
   - "CERTIFICATIONS" (if applicable)

3. Formatting Standards:
   - Use ALL CAPS for section headings
   - Use consistent date formats (e.g., "Jan 2024 - Present" or "2024")
   - Use bullet points (• or -) for experience descriptions
   - Use action verbs at the start of bullet points (Developed, Implemented, Created, etc.)
   - Keep consistent spacing between sections
   - Use clear hierarchy (Name largest, sections clearly separated)

4. Content Structure:
   - Header: Full name on first line, contact info below
   - Summary: 2-4 sentences, no bullets, highlights key qualifications
   - Skills: List format, can be comma-separated or bulleted, prioritize job-relevant skills
   - Experience: Company/Position | Dates format, then bullet points with achievements
   - Education: Degree, Institution, Year (or Expected Year)

5. ATS Optimization:
   - Use standard fonts (Arial, Calibri, Times New Roman)
   - Avoid graphics, tables, columns, or complex formatting
   - Use standard bullet points (• or -)
   - Include keywords naturally throughout
   - Use standard file formats (plain text representation)

Please follow these guidelines:

STEP 1: Keyword Optimization
- Identify keywords from the job description
- Naturally incorporate these keywords throughout the resume
- Match the language used in the job posting
- Include variations of key terms

STEP 2: Create Standard Resume Structure
Follow the exact section order and formatting standards above. Ensure:
- Professional appearance
- Clear hierarchy and readability
- Consistent formatting throughout
- ATS-friendly structure

STEP 3: Content Optimization
- Tailor each section to the job requirements using recommended text
- Use action verbs and quantifiable achievements where possible
- Highlight skills and experiences most relevant to the position
- Ensure content is professional and compelling

STEP 4: Format Verification
- Verify all sections follow standard format
- Check section headings are in ALL CAPS
- Ensure consistent date formatting
- Confirm proper spacing and organization

After creating the resume, analyze the improvements:
- Compare the new resume with the original profile
- Explain how using the recommended text improved the resume
- Estimate the ATS score improvement (e.g., "Expected to increase ATS score from X to Y")

Please respond ONLY with valid JSON (no markdown code blocks) in the following format:
{{
    "generated_resume": "<complete resume in standard format following the structure above. Use proper section headings (ALL CAPS), consistent formatting, clear hierarchy. Format as plain text with line breaks. Example format:\n\nJOHN DOE\nPhone: (555) 123-4567 | Email: john.doe@email.com | Location: City, State\n\nPROFESSIONAL SUMMARY\n[2-4 sentences summarizing qualifications]\n\nSKILLS\n[Skills listed, prioritized by job relevance]\n\nEXPERIENCE\n[If provided, formatted with company, dates, and bullet points]\n\nEDUCATION\n[Degree, Institution, Year]\n\n>",
    "sections": {{
        "header": "<name and contact info formatted properly>",
        "summary": "<professional summary using recommended phrasing, 2-4 sentences>",
        "skills": "<skills section with recommended text, properly formatted>",
        "experience": "<experience section with recommended text, formatted with company/position/dates and bullet points>",
        "education": "<education section with degree, institution, year>"
    }},
    "optimized_content": "<ATS-optimized version with emphasis on keywords from recommended text>",
    "keywords_used": ["<keyword1>", "<keyword2>", ...],
    "formatting_suggestions": "<specific formatting recommendations for ATS compatibility and standard resume format>",
    "improvements_made": "<explanation of how recommended text was incorporated and what improvements were made>",
    "ats_improvement": "<explanation of expected ATS score improvement. Compare old profile vs new resume. Estimate score increase>"
}}

IMPORTANT FORMATTING RULES:
- Use ALL CAPS for section headings (PROFESSIONAL SUMMARY, SKILLS, EXPERIENCE, EDUCATION)
- Use consistent date formats
- Use bullet points (•) for experience descriptions
- Start experience bullets with action verbs
- Maintain clear spacing between sections
- Follow standard resume structure exactly as specified above

Make the resume professional, compelling, optimized for ATS systems, and follow standard resume formatting conventions. Ensure you use the recommended text provided above."""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json_from_response(response.text)
            
            # Ensure required fields
            if "generated_resume" not in result:
                result["generated_resume"] = response.text
            if "sections" not in result:
                result["sections"] = {}
            if "optimized_content" not in result:
                result["optimized_content"] = result.get("generated_resume", "")
            if "keywords_used" not in result:
                result["keywords_used"] = []
            if "formatting_suggestions" not in result:
                result["formatting_suggestions"] = "Use standard formatting, avoid graphics and tables."
            if "improvements_made" not in result:
                result["improvements_made"] = "Resume optimized using recommended text and phrasing."
            if "ats_improvement" not in result:
                result["ats_improvement"] = "Resume incorporates recommended keywords and phrasing, expected to significantly improve ATS score."
            
            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "Quota exceeded" in error_msg:
                error_msg = "API Quota Exceeded. Please wait a few minutes or use GEMINI_MODEL=gemini-pro in .env"
            return {
                "generated_resume": f"Error generating resume: {error_msg}",
                "sections": {},
                "optimized_content": "",
                "keywords_used": [],
                "formatting_suggestions": "",
                "improvements_made": "",
                "ats_improvement": ""
            }
    
    def calculate_ats_confidence(self, user_profile: Dict, internship: Dict) -> Dict[str, Any]:
        """
        Calculate ATS confidence score with detailed analysis.
        """
        prompt = f"""You are an ATS (Applicant Tracking System) expert analyzing how well a candidate's profile matches a job posting for ATS compatibility.

CANDIDATE PROFILE:
Skills: {', '.join(user_profile.get('skills', []))}
Experience: {user_profile.get('experience', 'Not provided')}
Education: {user_profile.get('education', 'Not provided')}

JOB POSTING:
Title: {internship.get('title', 'N/A')}
Required Skills: {', '.join(internship.get('requirements', []))}
Job Description: {internship.get('description', '')}

TASK: Analyze ATS compatibility and calculate a confidence score.

Please perform this comprehensive analysis:

STEP 1: Keyword Matching Analysis
- Identify all keywords in the job description (skills, technologies, tools, qualifications)
- Check which keywords appear in the candidate's profile
- Calculate keyword match percentage
- Identify missing critical keywords
- Note keyword variations and synonyms

STEP 2: Skill Alignment Assessment
- Compare candidate skills against required skills
- Assess skill level match (entry-level, intermediate, advanced)
- Identify skill gaps that would cause ATS rejection
- Note transferable skills that might be recognized

STEP 3: Resume Structure Compatibility
- Assess if the profile information is structured in an ATS-friendly way
- Check for standard section headings
- Evaluate keyword placement and density
- Assess formatting compatibility

STEP 4: Confidence Score Calculation
Calculate an ATS confidence score (0-100) based on:
- Keyword match (40%): How many required keywords are present
- Skill alignment (30%): How well skills match requirements
- Profile completeness (20%): How complete and well-structured the profile is
- Overall fit (10%): General alignment with the role

STEP 5: Improvement Recommendations
- Provide specific, actionable suggestions to improve ATS score
- Prioritize by impact on score
- Focus on keyword optimization and skill presentation

Please respond in the following JSON format:
{{
    "ats_score": <number 0-100>,
    "confidence_percentage": <number 0-100>,
    "analysis": "<detailed ATS analysis with reasoning>",
    "keyword_matching": {{
        "matched_keywords": ["<keyword1>", "<keyword2>"],
        "missing_keywords": ["<keyword1>", "<keyword2>"],
        "match_percentage": <percentage>,
        "critical_missing": ["<critical keyword1>", ...]
    }},
    "improvement_suggestions": ["<suggestion1>", "<suggestion2>", ...],
    "reasoning": "<step-by-step reasoning for the confidence score, explaining each factor>"
}}

Be thorough, specific, and provide actionable insights. Focus on what would cause ATS systems to rank this candidate."""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._extract_json_from_response(response.text)
            
            # Ensure required fields
            if "ats_score" not in result:
                result["ats_score"] = 0.0
            if "confidence_percentage" not in result:
                result["confidence_percentage"] = result.get("ats_score", 0.0)
            if "analysis" not in result:
                result["analysis"] = response.text
            if "keyword_matching" not in result:
                result["keyword_matching"] = {}
            if "improvement_suggestions" not in result:
                result["improvement_suggestions"] = []
            if "reasoning" not in result:
                result["reasoning"] = result.get("analysis", "")
            
            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "Quota exceeded" in error_msg:
                error_msg = "API Quota Exceeded. Please wait a few minutes or use GEMINI_MODEL=gemini-pro in .env"
            return {
                "ats_score": 0.0,
                "confidence_percentage": 0.0,
                "analysis": f"Error calculating ATS confidence: {error_msg}",
                "keyword_matching": {},
                "improvement_suggestions": [],
                "reasoning": ""
            }

