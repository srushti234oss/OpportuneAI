from .models import Opportunity
from .models import Fellowship


def calculate_match_score(student, opportunity):

    score = 0

    student_skills = student.skills.lower().split(',')

    required_skills = opportunity.required_skills.lower().split(',')

    # Skill matching
    for skill in student_skills:
        if skill.strip().lower() in required_skills:
            score += 20

    # CGPA matching
    if student.cgpa >= opportunity.minimum_cgpa:
        score += 30

    # Branch/category matching
    if student.branch.lower() in opportunity.ai_category.lower():
        score += 20

    return score


def get_recommended_opportunities(student):

    opportunities = Opportunity.objects.all()

    recommendations = []

    for opportunity in opportunities:

        score = calculate_match_score(
            student,
            opportunity
        )

        missing_skills = skill_gap_analysis(
            student,
            opportunity
        )

        recommendations.append({

    'opportunity': opportunity,

    'score': score,

    'missing_skills': missing_skills,

    'prediction':
        predict_selection_chance(score)
})

    recommendations.sort(
        key=lambda x: x['score'],
        reverse=True
    )

    return recommendations


def skill_gap_analysis(student, opportunity):

    student_skills = [
        skill.strip().lower()
        for skill in student.skills.split(',')
    ]

    required_skills = [
        skill.strip().lower()
        for skill in opportunity.required_skills.split(',')
    ]

    missing_skills = []

    for skill in required_skills:

        if skill not in student_skills:
            missing_skills.append(skill)

    return missing_skills



def predict_selection_chance(score):

    if score >= 80:
        return "High Chance"

    elif score >= 50:
        return "Medium Chance"

    return "Low Chance"


def get_recommended_fellowships(student):

    fellowships = Fellowship.objects.all()

    recommendations = []

    for fellowship in fellowships:

        score = 0

        student_skills = [
            skill.strip().lower()
            for skill in student.skills.split(',')
        ]

        required_skills = [
            skill.strip().lower()
            for skill in fellowship.required_skills.split(',')
        ]

        for skill in student_skills:
            if skill in required_skills:
                score += 20

        

        missing_skills = []

        for skill in required_skills:
            if skill not in student_skills:
                missing_skills.append(skill)

        if score >= 80:
            prediction = "High Chance"
        elif score >= 50:
            prediction = "Medium Chance"
        else:
            prediction = "Low Chance"

        recommendations.append({
            'fellowship': fellowship,
            'score': score,
            'prediction': prediction,
            'missing_skills': missing_skills
        })

    recommendations.sort(
        key=lambda x: x['score'],
        reverse=True
    )

    return recommendations

def get_recommended_scholarships(student):

    from .models import Scholarship

    scholarships = Scholarship.objects.all()

    recommendations = []

    for scholarship in scholarships:

        score = 0

        student_skills = [
            skill.strip().lower()
            for skill in student.skills.split(',')
        ]

        required_skills = []

        if scholarship.required_skills:

            required_skills = [
                skill.strip().lower()
                for skill in scholarship.required_skills.split(',')
            ]

        matched_skills = 0

        for skill in required_skills:

            if skill in student_skills:
                matched_skills += 1

        score += matched_skills * 20

        missing_skills = []

        for skill in required_skills:

            if skill not in student_skills:
                missing_skills.append(skill)

        if score >= 80:
            prediction = "High Chance"

        elif score >= 50:
            prediction = "Medium Chance"

        else:
            prediction = "Low Chance"

        recommendations.append({

            'scholarship': scholarship,

            'score': score,

            'prediction': prediction,

            'missing_skills': missing_skills
        })

    recommendations.sort(
        key=lambda x: x['score'],
        reverse=True
    )

    return recommendations


def get_recommended_hackathons(student):

    from .models import Hackathon

    hackathons = Hackathon.objects.all()

    recommendations = []

    for hackathon in hackathons:

        score = 0

        student_skills = [
            skill.strip().lower()
            for skill in student.skills.split(',')
        ]

        required_skills = []

        if hackathon.required_skills:

            required_skills = [
                skill.strip().lower()
                for skill in hackathon.required_skills.split(',')
            ]

        matched_skills = 0

        for skill in required_skills:

            if skill in student_skills:
                matched_skills += 20

        score += matched_skills

        missing_skills = []

        for skill in required_skills:

            if skill not in student_skills:
                missing_skills.append(skill)

        if score >= 80:
            prediction = "High Chance"

        elif score >= 50:
            prediction = "Medium Chance"

        else:
            prediction = "Low Chance"

        recommendations.append({

            'hackathon': hackathon,

            'score': score,

            'prediction': prediction,

            'missing_skills': missing_skills
        })

    recommendations.sort(
        key=lambda x: x['score'],
        reverse=True
    )

    return recommendations