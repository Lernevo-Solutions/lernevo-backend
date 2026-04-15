# backend/app/vertex_ai_prompts.py

# Professional Summary Prompts
SUMMARY_PROMPTS = {
    'generate': """
You are an expert resume writer. Create a professional summary for a {title} professional.

User Information:
- Job Title: {title}
- Skills: {skills}
- Experience Context: {experience_context}

Requirements:
1. 3-4 sentences maximum
2. Highlight key achievements and skills
3. Use professional, confident language
4. Focus on value proposition

Return ONLY the summary text, no explanations.
""",
    
    'improve': """
Improve this professional summary to be more impactful.

Current Summary: {current_text}

User's Role: {title}
Skills: {skills}

Make it:
1. More action-oriented
2. Include quantifiable achievements
3. Add relevant keywords for ATS

Return ONLY the improved summary text.
"""
}

# Projects Section Prompts
PROJECTS_PROMPTS = {
    'generate': """
Create {num_projects} impressive project descriptions for a {title} professional.

Tech Stack: {tech_stack}
Context: {context}

For each project provide:
- Project Name
- Technologies Used
- 2-3 bullet points with quantifiable achievements

Format:
### Project Name
**Tech:** technologies
- achievement with metric
- achievement with metric
""",
    
    'improve': """
Improve these project descriptions with better metrics and impact.

Current Projects:
{current_projects}

Role: {title}

Add metrics (%, users, performance improvements) where possible.
Use stronger action verbs.

Return improved projects with same format.
"""
}

# Experience Prompts
EXPERIENCE_PROMPTS = {
    'generate': """
Create professional experience bullet points for a {role} at {company}.

Company: {company}
Role: {role}
Duration: {duration}
Key Responsibilities: {responsibilities}
Tech Stack: {tech}

Generate 4-5 bullet points:
1. Start with strong action verbs
2. Include quantifiable results
3. Show business impact

Return each bullet point on new line starting with •
""",
    
    'improve': """
Improve these experience bullet points.

Current Bullets:
{current_bullets}

Role: {role}

For each bullet:
1. Add metrics where possible
2. Use stronger verbs (Led, Built, Optimized, Increased)
3. Show results

Return improved bullets only.
"""
}

# Certifications Prompts
CERTIFICATIONS_PROMPTS = {
    'generate': """
Suggest relevant certifications for a {title} professional.

Current Skills: {skills}
Industry: {industry}

Return as JSON:
{{
    "certifications": [
        {{
            "name": "Certification Name",
            "issuer": "Provider",
            "description": "Brief value description"
        }}
    ]
}}
""",
    
    'improve': """
Format and improve these certifications.

Current: {current_certs}

For each certification:
1. Add issuing authority if missing
2. Use proper capitalization
3. Add relevance note

Return formatted certifications.
"""
}

# Education Prompts
EDUCATION_PROMPTS = {
    'generate': """
Create a professional education section.

Degree: {degree}
Field: {field}
University: {university}
Year: {year}
Coursework: {coursework}

Include:
- Degree and major
- University name
- Graduation year
- Relevant coursework (3-4 subjects)
- Academic achievements (if any)

Return formatted education section.
""",
    
    'improve': """
Improve this education section formatting.

Current: {current_education}

Make it more professional and ATS-friendly.
Add relevant coursework if possible.

Return improved education section.
"""
}

# Skills Prompts
SKILLS_PROMPTS = {
    'generate': """
Suggest relevant skills for a {title} professional.

Current skills mentioned: {current_skills}
Experience level: {level}

Return a JSON object with skills categorized:
{{
    "technical": ["skill1", "skill2", "skill3"],
    "soft": ["skill1", "skill2"],
    "tools": ["tool1", "tool2"]
}}

Include 5-7 technical skills, 3-4 soft skills, 3-4 tools.
"""
}