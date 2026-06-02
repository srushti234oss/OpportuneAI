# core/ai_engine.py
# Drop-in replacement — same function names, same return format
# Added: Sentence-BERT semantic similarity + spaCy skill extraction

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

# ── Load models once at startup (not on every request) ──
print("Loading AI models... (first time only)")
_embedder = SentenceTransformer("all-MiniLM-L6-v2")
_nlp = spacy.load("en_core_web_sm")
print("AI models ready.")

# ── Skill vocabulary for NLP extraction ──────────────────
SKILL_VOCAB = {
    "python", "java", "javascript", "typescript", "c++", "c", "rust", "go",
    "kotlin", "swift", "r", "matlab", "sql", "scala", "php", "ruby",
    "react", "vue", "angular", "node.js", "django", "flask", "fastapi",
    "spring", "express", "html", "css", "rest api", "graphql",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "data analysis", "data science", "tableau", "power bi",
    "aws", "gcp", "azure", "docker", "kubernetes", "git", "linux",
    "android", "ios", "flutter", "react native",
    "data structures", "algorithms", "dsa", "system design",
    "communication", "teamwork", "leadership", "research",
    "problem solving", "mathematics", "statistics", "excel",
}


# ── CORE: Build a text string from any model object ──────

def _profile_to_text(student):
    """Convert StudentProfile to a descriptive sentence for embedding."""
    return (
        f"{student.branch} student with skills in {student.skills}. "
        f"CGPA: {student.cgpa}. {student.bio}"
    )


def _opportunity_to_text(opp):
    """Convert any opportunity model to text for embedding."""
    # Works for Opportunity, Scholarship, Hackathon, Fellowship
    # Each has slightly different field names — handle all
    parts = []

    # title
    parts.append(getattr(opp, 'title', ''))

    # company/provider/organizer/organization
    for field in ['company', 'provider', 'organizer', 'organization']:
        val = getattr(opp, field, None)
        if val:
            parts.append(val)
            break

    # description
    parts.append(getattr(opp, 'description', ''))

    # required_skills
    parts.append(getattr(opp, 'required_skills', '') or '')

    # ai_category
    parts.append(getattr(opp, 'ai_category', '') or '')

    return " ".join(filter(None, parts))


# ── NLP: Extract skills from any text ────────────────────

def _extract_skills_nlp(text: str) -> list:
    """
    Use spaCy + vocab matching to pull skill keywords from text.
    Much better than simple string split.
    """
    text_lower = text.lower()
    found = set()

    # 1. Exact vocab match
    for skill in SKILL_VOCAB:
        if skill in text_lower:
            found.add(skill)

    # 2. spaCy noun chunks (catches skills not in vocab)
    doc = _nlp(text[:3000])
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        if 2 < len(chunk_text) < 30:
            found.add(chunk_text)

    return list(found)


# ── AI SKILL GAP: NLP-based, replaces the old split() logic ─

def skill_gap_analysis(student, opportunity):
    """
    NLP-powered skill gap.
    Extracts skills from opportunity description using spaCy,
    then compares against student's skills semantically.
    """
    # Get student skills (still from profile text field)
    student_skills_raw = student.skills.lower()
    student_skill_list = [s.strip() for s in student_skills_raw.split(',')]

    # Extract required skills using NLP (not just split)
    opp_text = (getattr(opportunity, 'required_skills', '') or '') + \
               " " + (getattr(opportunity, 'description', '') or '')
    required_skills = _extract_skills_nlp(opp_text)

    # Find missing: required skills not in student profile
    missing = []
    for skill in required_skills:
        # Check if any student skill is semantically similar
        matched = False
        for s_skill in student_skill_list:
            if s_skill in skill or skill in s_skill:
                matched = True
                break
        if not matched:
            missing.append(skill)

    # Return only the most important missing skills (top 5)
    return missing[:5]


# ── AI MATCH SCORE: Sentence-BERT cosine similarity ──────

def _calculate_ai_match_score(student, opportunity) -> int:
    """
    Uses Sentence-BERT to compute semantic similarity
    between student profile and opportunity.
    Returns score 0-100.
    """
    profile_text = _profile_to_text(student)
    opp_text = _opportunity_to_text(opportunity)

    # Generate embeddings
    profile_vec = _embedder.encode([profile_text])
    opp_vec = _embedder.encode([opp_text])

    # Cosine similarity → 0.0 to 1.0 → scale to 0-100
    similarity = cosine_similarity(profile_vec, opp_vec)[0][0]
    ai_score = int(similarity * 100)

    # Bonus: CGPA check (same as before, keeps old logic)
    min_cgpa = getattr(opportunity, 'minimum_cgpa', 0) or 0
    if float(student.cgpa) >= float(min_cgpa):
        ai_score = min(100, ai_score + 10)

    return ai_score


# ── PREDICTION: Keep your original algorithm (unchanged) ─

def predict_selection_chance(score: int) -> str:
    if score >= 70:
        return "High Chance"
    elif score >= 45:
        return "Medium Chance"
    return "Low Chance"


# ══════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS — same names as before, views.py unchanged
# ══════════════════════════════════════════════════════════

def get_recommended_opportunities(student):
    from .models import Opportunity
    opportunities = Opportunity.objects.all()
    recommendations = []

    for opp in opportunities:
        score = _calculate_ai_match_score(student, opp)
        missing_skills = skill_gap_analysis(student, opp)
        recommendations.append({
         'opportunity': opp,
         'score': score,
         'missing_skills': missing_skills,
         'prediction': predict_selection_chance(score),
         'required_skills_list': [s.strip() for s in (opp.required_skills or '').split(',')][:5],
         })
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations


def get_recommended_scholarships(student):
    from .models import Scholarship
    scholarships = Scholarship.objects.all()
    recommendations = []

    for s in scholarships:
        score = _calculate_ai_match_score(student, s)
        missing_skills = skill_gap_analysis(student, s)
        recommendations.append({
            'scholarship': s,
            'score': score,
            'missing_skills': missing_skills,
            'prediction': predict_selection_chance(score),
        })

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations


def get_recommended_hackathons(student):
    from .models import Hackathon
    hackathons = Hackathon.objects.all()
    recommendations = []

    for h in hackathons:
        score = _calculate_ai_match_score(student, h)
        missing_skills = skill_gap_analysis(student, h)
        recommendations.append({
            'hackathon': h,
            'score': score,
            'missing_skills': missing_skills,
            'prediction': predict_selection_chance(score),
        })

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations


def get_recommended_fellowships(student):
    from .models import Fellowship
    fellowships = Fellowship.objects.all()
    recommendations = []

    for f in fellowships:
        score = _calculate_ai_match_score(student, f)
        missing_skills = skill_gap_analysis(student, f)
        recommendations.append({
            'fellowship': f,
            'score': score,
            'missing_skills': missing_skills,
            'prediction': predict_selection_chance(score),
        })

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations

    # ── ADD THIS to the bottom of core/ai_engine.py ──────────

# Curated free learning resources map
LEARNING_RESOURCES = {
    "python": [
        {"title": "Python for Everybody — freeCodeCamp", "url": "https://www.youtube.com/watch?v=8DvywoWv6fI", "platform": "YouTube", "duration": "13 hrs"},
        {"title": "CS50P — Harvard Python Course", "url": "https://cs50.harvard.edu/python", "platform": "edX (Free)", "duration": "10 hrs"},
    ],
    "react": [
        {"title": "React Full Course 2024 — freeCodeCamp", "url": "https://www.youtube.com/watch?v=CgkZ7MvWUAA", "platform": "YouTube", "duration": "8 hrs"},
        {"title": "React Official Tutorial", "url": "https://react.dev/learn", "platform": "react.dev (Free)", "duration": "4 hrs"},
    ],
    "machine learning": [
        {"title": "Machine Learning Specialization — Andrew Ng", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "platform": "Coursera (Audit Free)", "duration": "90 hrs"},
        {"title": "ML Zero to Hero — Google", "url": "https://www.youtube.com/watch?v=VwVg9jCtqaU", "platform": "YouTube", "duration": "4 hrs"},
    ],
    "dsa": [
        {"title": "DSA Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=8hly31xKli0", "platform": "YouTube", "duration": "8 hrs"},
        {"title": "LeetCode Study Plan", "url": "https://leetcode.com/study-plan/data-structure/", "platform": "LeetCode (Free)", "duration": "Self-paced"},
    ],
    "sql": [
        {"title": "SQL Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "platform": "YouTube", "duration": "4 hrs"},
        {"title": "SQLZoo Interactive", "url": "https://sqlzoo.net", "platform": "SQLZoo (Free)", "duration": "Self-paced"},
    ],
    "system design": [
        {"title": "System Design Primer — GitHub", "url": "https://github.com/donnemartin/system-design-primer", "platform": "GitHub (Free)", "duration": "Self-paced"},
        {"title": "System Design by Gaurav Sen", "url": "https://www.youtube.com/watch?v=xpDnVSmNFX0", "platform": "YouTube", "duration": "6 hrs"},
    ],
    "docker": [
        {"title": "Docker Full Course — TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "platform": "YouTube", "duration": "3 hrs"},
    ],
    "kubernetes": [
        {"title": "Kubernetes Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=d6WC5n9G_sM", "platform": "YouTube", "duration": "4 hrs"},
    ],
    "aws": [
        {"title": "AWS Free Tier + Training", "url": "https://aws.amazon.com/training/digital/", "platform": "AWS (Free tier)", "duration": "Self-paced"},
        {"title": "AWS Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=3hLmDS179YE", "platform": "YouTube", "duration": "5 hrs"},
    ],
    "gcp": [
        {"title": "Google Cloud Skills Boost", "url": "https://cloudskillsboost.google/", "platform": "Google (Free)", "duration": "Self-paced"},
    ],
    "tensorflow": [
        {"title": "TensorFlow 2.0 Complete Course", "url": "https://www.youtube.com/watch?v=tPYj3fFJGjk", "platform": "YouTube", "duration": "7 hrs"},
        {"title": "TensorFlow Official Tutorials", "url": "https://www.tensorflow.org/tutorials", "platform": "TensorFlow.org (Free)", "duration": "Self-paced"},
    ],
    "pytorch": [
        {"title": "PyTorch Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "platform": "YouTube", "duration": "10 hrs"},
    ],
    "javascript": [
        {"title": "JavaScript Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=PkZNo7MFNFg", "platform": "YouTube", "duration": "3 hrs"},
        {"title": "The Odin Project", "url": "https://www.theodinproject.com/", "platform": "TheOdinProject (Free)", "duration": "Self-paced"},
    ],
    "django": [
        {"title": "Django Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=F5mRW0jo-U4", "platform": "YouTube", "duration": "3 hrs"},
    ],
    "java": [
        {"title": "Java Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=GoXwIVyNvX0", "platform": "YouTube", "duration": "12 hrs"},
    ],
    "flutter": [
        {"title": "Flutter Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=VPvVD8t02U8", "platform": "YouTube", "duration": "6 hrs"},
    ],
    "git": [
        {"title": "Git & GitHub Crash Course", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "platform": "YouTube", "duration": "1 hr"},
    ],
    "data science": [
        {"title": "Data Science Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=ua-CiDNNj30", "platform": "YouTube", "duration": "6 hrs"},
    ],
    "nlp": [
        {"title": "NLP with Python — Hugging Face", "url": "https://huggingface.co/learn/nlp-course/", "platform": "HuggingFace (Free)", "duration": "Self-paced"},
    ],
    "linux": [
        {"title": "Linux Command Line Full Course", "url": "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "platform": "YouTube", "duration": "5 hrs"},
    ],
    "statistics": [
        {"title": "Statistics for Data Science — freeCodeCamp", "url": "https://www.youtube.com/watch?v=xxpc-HPKN28", "platform": "YouTube", "duration": "8 hrs"},
    ],
}


def get_learning_resources(missing_skills: list) -> list:
    """
    Given a list of missing skill strings,
    return matched free learning resources.
    Called from views.py for the skillmap page.
    """
    result = []
    seen_skills = set()

    for skill in missing_skills:
        skill_lower = skill.lower().strip()
        if skill_lower in seen_skills:
            continue

        # Direct match
        if skill_lower in LEARNING_RESOURCES:
            result.append({
                "skill": skill,
                "resources": LEARNING_RESOURCES[skill_lower]
            })
            seen_skills.add(skill_lower)
            continue

        # Partial match (e.g. "machine learning basics" → "machine learning")
        for key in LEARNING_RESOURCES:
            if key in skill_lower or skill_lower in key:
                result.append({
                    "skill": skill,
                    "resources": LEARNING_RESOURCES[key]
                })
                seen_skills.add(skill_lower)
                break

    return result


def get_full_skill_report(student) -> dict:
    """
    Master skill report for the skillmap page.
    Shows all missing skills across ALL opportunity types
    + learning resources for each gap.
    """
    from .models import Opportunity, Scholarship, Hackathon, Fellowship

    all_missing = set()

    # Collect missing skills from top 5 of each category
    for opp in Opportunity.objects.all()[:5]:
        for skill in skill_gap_analysis(student, opp):
            all_missing.add(skill)

    for s in Scholarship.objects.all()[:3]:
        for skill in skill_gap_analysis(student, s):
            all_missing.add(skill)

    for h in Hackathon.objects.all()[:3]:
        for skill in skill_gap_analysis(student, h):
            all_missing.add(skill)

    for f in Fellowship.objects.all()[:3]:
        for skill in skill_gap_analysis(student, f):
            all_missing.add(skill)

    missing_list = list(all_missing)[:10]  # top 10 gaps
    resources = get_learning_resources(missing_list)

    # Student's existing skills
    student_skills = [s.strip() for s in student.skills.split(',')]

    return {
        "student_skills": student_skills,
        "missing_skills": missing_list,
        "learning_resources": resources,
        "total_gaps": len(missing_list),
    }