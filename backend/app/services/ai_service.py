
import json
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def generate_json(prompt):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert career coach. Return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )

    return json.loads(response.choices[0].message.content)


def extract_resume_details(resume_text):
    prompt = f"""
    Extract information explicitly mentioned in this resume.

    Return JSON:
    {{
        "name": "",
        "education": [],
        "technical_skills": [],
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "tools": [],
        "projects": [],
        "internships": [],
        "certifications": [],
        "experience": [],
        "summary": ""
    }}

    Do not invent information.

    Resume:
    {resume_text[:15000]}
    """

    return generate_json(prompt)


def extract_job_skills(job_description):
    prompt = f"""
    Extract technical skills required in this job description.

    Return JSON:
    {{
        "required_skills": []
    }}

    Job Description:
    {job_description[:10000]}
    """

    result = generate_json(prompt)
    return result["required_skills"]

def generate_skill_gap_analysis(missing_skills, job_description):

    if not missing_skills:
        return {
            "skill_gaps": [],
            "overall_recommendation": "Your skills match all extracted job requirements."
        }

    prompt = f"""
    You are an expert technical career coach.

    Analyze the missing skills of a student applying for a job.

    Missing skills:
    {json.dumps(missing_skills)}

    Job description:
    {job_description[:8000]}

    Return valid JSON in this format:

    {{
        "skill_gaps": [
            {{
                "skill": "React",
                "priority": "High",
                "reason": "Required for frontend development",
                "action": "Learn React fundamentals and build a project"
            }}
        ],
        "overall_recommendation": "A short personalized recommendation"
    }}

    Rules:
    - Include every missing skill.
    - Priority must be High, Medium, or Low.
    - Base priority on the job description.
    - Do not invent job requirements.
    """

    return generate_json(prompt)

def generate_learning_roadmap(missing_skills, job_description):

    if not missing_skills:
        return {
            "roadmap": [],
            "message": "No major skill gaps found. Focus on advanced practice and projects."
        }

    prompt = f"""
    You are an expert technical career coach.

    Create a personalized 30-day learning roadmap for a student.

    Missing skills:
    {json.dumps(missing_skills)}

    Job description:
    {job_description[:8000]}

    Return valid JSON in this format:

    {{
        "roadmap": [
            {{
                "day": 1,
                "topic": "JavaScript Basics",
                "tasks": [
                    "Understand variables",
                    "Learn data types",
                    "Practice basic programs"
                ],
                "resource": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
            }}
        ],
        "message": "A short motivational recommendation"
    }}

    Rules:
    - Create a complete 30-day roadmap.
    - Cover all missing skills.
    - Arrange topics from beginner to advanced.
    - Include practical coding tasks.
    - Recommend free learning resources.
    - Use genuine learning resource URLs.
    - Keep tasks realistic for a student.
    - Return JSON only.
    """

    return generate_json(prompt)

def generate_course_recommendations(missing_skills):

    if not missing_skills:
        return {
            "recommendations": [],
            "message": "No missing skills found. Continue advanced practice."
        }

    prompt = f"""
    You are an expert technical learning advisor.

    Recommend free learning resources for these missing skills:

    {json.dumps(missing_skills)}

    Return valid JSON in this format:

    {{
        "recommendations": [
            {{
                "skill": "JavaScript",
                "course_name": "JavaScript Guide",
                "platform": "MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                "cost": "Free",
                "description": "Learn JavaScript fundamentals and advanced concepts."
            }}
        ],
        "message": "A short learning recommendation."
    }}

    Rules:
    - Recommend resources for every missing skill.
    - Only recommend genuinely free resources.
    - Prefer official documentation and established learning platforms.
    - Use genuine URLs. Never invent course links.
    - Keep descriptions short.
    - Return JSON only.
    """

    return generate_json(prompt)

def generate_interview_questions(job_description):

    prompt = f"""
    You are an experienced technical interviewer.

    Generate 5 technical interview questions based on this job description:

    {job_description[:8000]}

    Return valid JSON:

    {{
        "questions": [
            {{
                "question": "Explain the difference between let and const in JavaScript.",
                "difficulty": "Easy",
                "topic": "JavaScript"
            }}
        ]
    }}

    Rules:
    - Generate exactly 5 questions.
    - Include easy, medium and hard questions.
    - Focus on skills required by the job.
    - Return JSON only.
    """

    return generate_json(prompt)


def evaluate_interview_answer(question, answer):

    prompt = f"""
    You are an expert technical interview evaluator.

    Interview question:
    {question}

    Student answer:
    {answer}

    Evaluate the answer.

    Return valid JSON:

    {{
        "score": 7,
        "feedback": "Good explanation, but include a practical example.",
        "strengths": ["Correct concept"],
        "improvements": ["Add a practical example"],
        "ideal_answer": "A concise ideal answer."
    }}

    Rules:
    - Score must be between 0 and 10.
    - Be fair and constructive.
    - Do not give full marks for incomplete answers.
    - Return JSON only.
    """

    return generate_json(prompt)
