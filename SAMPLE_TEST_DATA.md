# Sample Test Data for InternHub AI

## Quick Copy-Paste Examples

### Example 1: Software Engineering Intern

#### Your Profile:
**Skills:**
```
Python, JavaScript, React, Git, SQL, Problem-solving, Team collaboration, Communication
```

**Interests:**
```
Web Development, Full-stack Development, Software Engineering, Open Source
```

**Experience (optional):**
```
Developed a personal portfolio website using React and Node.js. Contributed to open-source projects on GitHub. Completed 3 web development projects including a todo app and weather dashboard.
```

**Education (optional):**
```
Bachelor of Science in Computer Science, Expected Graduation: 2025
Relevant coursework: Data Structures, Algorithms, Database Systems, Web Development
```

#### Internship Details:
**Job Title:**
```
Software Engineering Intern
```

**Company (optional):**
```
TechCorp Inc.
```

**Job Description:**
```
We are looking for a motivated Software Engineering Intern to join our dynamic development team. You will work on building scalable web applications using modern technologies. The ideal candidate will assist in developing frontend and backend features, participate in code reviews, and collaborate with cross-functional teams. You'll gain hands-on experience with our tech stack and contribute to real-world projects that impact millions of users.
```

**Requirements:**
```
Python, JavaScript, React, Git, Problem-solving skills, Strong communication, Ability to work in a team
```

---

### Example 2: Data Science Intern

#### Your Profile:
**Skills:**
```
Python, Machine Learning, Data Analysis, Pandas, NumPy, SQL, Statistics, Data Visualization
```

**Interests:**
```
Data Science, Machine Learning, Artificial Intelligence, Data Analytics
```

**Experience (optional):**
```
Completed multiple data science projects including customer segmentation analysis and sales forecasting. Worked with datasets containing 10,000+ records. Built predictive models using scikit-learn.
```

**Education (optional):**
```
Master's in Data Science, Graduated 2024
Specialization: Machine Learning and Statistical Analysis
```

#### Internship Details:
**Job Title:**
```
Data Science Intern
```

**Company (optional):**
```
DataAnalytics Solutions
```

**Job Description:**
```
Join our data science team to help extract insights from large datasets and build machine learning models. You'll work on real-world problems including customer behavior analysis, predictive modeling, and data visualization. The role involves cleaning and preprocessing data, feature engineering, model development, and presenting findings to stakeholders. You'll use Python, SQL, and various ML libraries.
```

**Requirements:**
```
Python, Machine Learning, SQL, Statistics, Data Analysis, Pandas, scikit-learn, Strong analytical skills
```

---

### Example 3: Frontend Development Intern

#### Your Profile:
**Skills:**
```
HTML, CSS, JavaScript, React, TypeScript, Responsive Design, UI/UX Design, Git
```

**Interests:**
```
Frontend Development, User Interface Design, Web Design, Mobile Development
```

**Experience (optional):**
```
Built 5 responsive web applications using React. Created custom UI components and implemented modern design patterns. Experience with CSS frameworks like Tailwind CSS.
```

**Education (optional):**
```
Bachelor's in Computer Science, Currently in 3rd year
Focus: Web Technologies and Human-Computer Interaction
```

#### Internship Details:
**Job Title:**
```
Frontend Development Intern
```

**Company (optional):**
```
WebDesign Studio
```

**Job Description:**
```
We're seeking a Frontend Development Intern to help create beautiful and functional user interfaces. You'll work with our design team to implement responsive web applications, optimize performance, and ensure cross-browser compatibility. You'll use React, TypeScript, and modern CSS to build components that provide excellent user experiences.
```

**Requirements:**
```
React, JavaScript, TypeScript, HTML, CSS, UI/UX Design, Responsive Design, Git
```

---

## JSON Format for API Testing

### Example Request Body (for use with `/docs` or Postman):

```json
{
  "user_profile": {
    "skills": [
      "Python",
      "JavaScript",
      "React",
      "Git",
      "SQL",
      "Problem-solving",
      "Team collaboration",
      "Communication"
    ],
    "interests": [
      "Web Development",
      "Full-stack Development",
      "Software Engineering",
      "Open Source"
    ],
    "experience": "Developed a personal portfolio website using React and Node.js. Contributed to open-source projects on GitHub. Completed 3 web development projects including a todo app and weather dashboard.",
    "education": "Bachelor of Science in Computer Science, Expected Graduation: 2025. Relevant coursework: Data Structures, Algorithms, Database Systems, Web Development"
  },
  "internship": {
    "title": "Software Engineering Intern",
    "description": "We are looking for a motivated Software Engineering Intern to join our dynamic development team. You will work on building scalable web applications using modern technologies. The ideal candidate will assist in developing frontend and backend features, participate in code reviews, and collaborate with cross-functional teams. You'll gain hands-on experience with our tech stack and contribute to real-world projects that impact millions of users.",
    "requirements": [
      "Python",
      "JavaScript",
      "React",
      "Git",
      "Problem-solving skills",
      "Strong communication",
      "Ability to work in a team"
    ],
    "company": "TechCorp Inc."
  }
}
```

---

## Testing All 5 Endpoints

### 1. Match Summary
- **Endpoint**: `POST /api/match-summary`
- **What it does**: Analyzes compatibility and provides match score
- **Expected**: Match score (0-100), strengths, weaknesses, reasoning

### 2. Skill Gap Analysis
- **Endpoint**: `POST /api/skill-gap`
- **What it does**: Identifies missing skills and learning paths
- **Expected**: Missing skills list, prioritized gaps, learning recommendations

### 3. Recommendations
- **Endpoint**: `POST /api/recommendation`
- **What it does**: Provides actionable steps to increase match
- **Expected**: Recommendations, short-term/long-term strategies, impact analysis

### 4. Resume Generation
- **Endpoint**: `POST /api/resume`
- **What it does**: Generates ATS-optimized resume
- **Expected**: Complete resume text, structured sections, keywords used

### 5. ATS Confidence
- **Endpoint**: `POST /api/confidence`
- **What it does**: Calculates ATS compatibility score
- **Expected**: ATS score, keyword matching analysis, improvement suggestions

---

## Quick Test Steps

1. **Start the server**: `uvicorn app.main:app --reload`

2. **Open the web UI**: Navigate to `http://localhost:8000/`

3. **Copy the sample data** from Example 1 above into the form fields

4. **Click each button** to test all 5 endpoints:
   - Get Match Summary
   - Analyze Skill Gaps
   - Get Recommendations
   - Generate Resume
   - Calculate ATS Confidence

5. **Or use API docs**: Go to `http://localhost:8000/docs` and test endpoints directly with the JSON example above

---

## Tips for Testing

- **Test with different skill levels**: Try with fewer skills to see skill gap analysis
- **Test with perfect match**: Use skills that exactly match requirements
- **Test with partial match**: Use some matching and some missing skills
- **Compare results**: See how recommendations change based on different profiles




