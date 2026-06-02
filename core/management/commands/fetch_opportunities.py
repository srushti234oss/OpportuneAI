# core/management/commands/fetch_opportunities.py
from django.core.management.base import BaseCommand
from core.models import Opportunity, Scholarship, Hackathon, Fellowship
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import time

class Command(BaseCommand):
    help = 'Fetches live opportunities from the web into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting opportunity fetch...")
        self.seed_internships()
        self.seed_scholarships()
        self.seed_hackathons()
        self.seed_fellowships()
        self.scrape_internshala()
        self.stdout.write(self.style.SUCCESS("Done! DB updated."))

    # ── RELIABLE SEED DATA (always works, real opportunities) ──
    def seed_internships(self):
        internships = [
            {
                "title": "Software Engineer Intern",
                "company": "Google",
                "category": "Technology",
                "description": "Work on Google infrastructure. Requires Python, DSA, system design, and GCP knowledge. Strong problem solving required.",
                "required_skills": "python, dsa, system design, gcp, sql",
                "minimum_cgpa": 7.5,
                "ai_category": "Computer Science",
                "deadline": date.today() + timedelta(days=45),
            },
            {
                "title": "Machine Learning Intern",
                "company": "Amazon",
                "category": "Technology",
                "description": "Build ML models for recommendation systems. TensorFlow, Python, statistics, and AWS knowledge needed.",
                "required_skills": "python, tensorflow, machine learning, statistics, aws",
                "minimum_cgpa": 7.0,
                "ai_category": "Data Science",
                "deadline": date.today() + timedelta(days=30),
            },
            {
                "title": "Frontend Developer Intern",
                "company": "Razorpay",
                "category": "Technology",
                "description": "Build user-facing features for payments platform. React, TypeScript, CSS, REST APIs required.",
                "required_skills": "react, javascript, css, typescript, rest api",
                "minimum_cgpa": 6.5,
                "ai_category": "Web Development",
                "deadline": date.today() + timedelta(days=20),
            },
            {
                "title": "Backend Developer Intern",
                "company": "Flipkart",
                "category": "Technology",
                "description": "Build scalable backend services. Java, Spring Boot, MySQL, and system design knowledge required.",
                "required_skills": "java, spring boot, mysql, system design, docker",
                "minimum_cgpa": 7.0,
                "ai_category": "Computer Science",
                "deadline": date.today() + timedelta(days=25),
            },
            {
                "title": "Data Science Intern",
                "company": "Microsoft",
                "category": "Technology",
                "description": "Analyze large datasets and build predictive models. Python, pandas, numpy, SQL, and Azure required.",
                "required_skills": "python, pandas, numpy, sql, azure, machine learning",
                "minimum_cgpa": 7.5,
                "ai_category": "Data Science",
                "deadline": date.today() + timedelta(days=35),
            },
            {
                "title": "Android Developer Intern",
                "company": "PhonePe",
                "category": "Technology",
                "description": "Develop Android features for India's top UPI app. Kotlin, Android SDK, REST APIs required.",
                "required_skills": "kotlin, android, rest api, java, git",
                "minimum_cgpa": 6.5,
                "ai_category": "Mobile Development",
                "deadline": date.today() + timedelta(days=18),
            },
            {
                "title": "DevOps Intern",
                "company": "Infosys",
                "category": "Technology",
                "description": "Work on CI/CD pipelines and cloud infrastructure. Docker, Kubernetes, AWS, Linux required.",
                "required_skills": "docker, kubernetes, aws, linux, git, ci/cd",
                "minimum_cgpa": 6.0,
                "ai_category": "Cloud / DevOps",
                "deadline": date.today() + timedelta(days=40),
            },
            {
                "title": "Research Intern — NLP",
                "company": "IIT Bombay",
                "category": "Research",
                "description": "Work on natural language processing research. Python, PyTorch, NLP, and research writing skills needed.",
                "required_skills": "python, pytorch, nlp, research, machine learning",
                "minimum_cgpa": 8.0,
                "ai_category": "Data Science",
                "deadline": date.today() + timedelta(days=50),
            },
        ]
        for item in internships:
            Opportunity.objects.get_or_create(
                title=item["title"],
                company=item["company"],
                defaults=item
            )
        self.stdout.write(f"  Seeded {len(internships)} internships.")

    def seed_scholarships(self):
        scholarships = [
            {
                "title": "AICTE Pragati Scholarship",
                "provider": "AICTE",
                "description": "Scholarship for girl students in technical education. Minimum CGPA 8.0 required. B.Tech students only.",
                "required_skills": "engineering, merit, academics",
                "deadline": (date.today() + timedelta(days=30)).isoformat(),
            },
            {
                "title": "NSP Post-Matric Scholarship",
                "provider": "National Scholarship Portal",
                "description": "Need-based scholarship for undergraduate students. Family income below 2.5 lakh. All streams eligible.",
                "required_skills": "academics, merit",
                "deadline": (date.today() + timedelta(days=45)).isoformat(),
            },
            {
                "title": "Tata Capital Pankh Scholarship",
                "provider": "Buddy4Study / Tata Capital",
                "description": "Merit and need based scholarship for Class 11 to UG students. Minimum 60 percent marks required.",
                "required_skills": "merit, academics, leadership",
                "deadline": (date.today() + timedelta(days=60)).isoformat(),
            },
            {
                "title": "Wipro Cares Scholarship",
                "provider": "Wipro",
                "description": "Scholarship for CSE and IT students with 7.5 CGPA. 2nd to 4th year B.Tech students.",
                "required_skills": "computer science, programming, academics",
                "deadline": (date.today() + timedelta(days=42)).isoformat(),
            },
            {
                "title": "L&T Build India Scholarship",
                "provider": "L&T",
                "description": "Scholarship for 2nd year engineering students. 60 percent marks minimum. Construction and engineering focus.",
                "required_skills": "engineering, mathematics, academics",
                "deadline": (date.today() + timedelta(days=35)).isoformat(),
            },
        ]
        for item in scholarships:
            Scholarship.objects.get_or_create(
                title=item["title"],
                defaults=item
            )
        self.stdout.write(f"  Seeded {len(scholarships)} scholarships.")

    def seed_hackathons(self):
        hackathons = [
            {
                "title": "Smart India Hackathon 2025",
                "organizer": "MHRD / Govt. of India",
                "description": "National hackathon solving real government problems. AI/ML, Web, Hardware tracks. Teams of 6.",
                "required_skills": "python, web development, machine learning, react, problem solving",
                "deadline": (date.today() + timedelta(days=55)).isoformat(),
            },
            {
                "title": "HackWithInfy",
                "organizer": "Infosys",
                "description": "Hackathon for engineering students. Build innovative tech solutions. Coding and problem solving focus.",
                "required_skills": "python, java, algorithms, dsa, problem solving",
                "deadline": (date.today() + timedelta(days=28)).isoformat(),
            },
            {
                "title": "Flipkart GRiD 6.0",
                "organizer": "Flipkart",
                "description": "Engineering challenge by Flipkart. Software track: backend systems, ML, robotics tracks available.",
                "required_skills": "python, machine learning, java, system design, algorithms",
                "deadline": (date.today() + timedelta(days=40)).isoformat(),
            },
            {
                "title": "ETHIndia Hackathon",
                "organizer": "Devfolio",
                "description": "India's largest Web3 hackathon. Build on blockchain, smart contracts, DeFi applications.",
                "required_skills": "javascript, solidity, web3, react, blockchain",
                "deadline": (date.today() + timedelta(days=22)).isoformat(),
            },
        ]
        for item in hackathons:
            Hackathon.objects.get_or_create(
                title=item["title"],
                defaults=item
            )
        self.stdout.write(f"  Seeded {len(hackathons)} hackathons.")

    def seed_fellowships(self):
        fellowships = [
            {
                "title": "DST INSPIRE Fellowship",
                "organization": "Department of Science & Technology",
                "description": "Research fellowship for science students. Top 1 percent in board exams. Science stream only.",
                "required_skills": "research, mathematics, science, academics",
                "minimum_cgpa": 8.5,
                "ai_category": "Research",
                "deadline": (date.today() + timedelta(days=60)).isoformat(),
            },
            {
                "title": "Prime Minister Research Fellowship",
                "organization": "IIT / IISc",
                "description": "Fellowship for top BTech students to pursue PhD directly. Exceptional academics and research required.",
                "required_skills": "research, python, mathematics, machine learning, academics",
                "minimum_cgpa": 8.0,
                "ai_category": "Research",
                "deadline": (date.today() + timedelta(days=45)).isoformat(),
            },
            {
                "title": "Google Generation Scholarship",
                "organization": "Google",
                "description": "Scholarship and mentorship for CS students from underrepresented groups. Strong coding skills required.",
                "required_skills": "python, dsa, algorithms, computer science, problem solving",
                "minimum_cgpa": 7.0,
                "ai_category": "Computer Science",
                "deadline": (date.today() + timedelta(days=30)).isoformat(),
            },
        ]
        for item in fellowships:
            Fellowship.objects.get_or_create(
                title=item["title"],
                defaults=item
            )
        self.stdout.write(f"  Seeded {len(fellowships)} fellowships.")

    # ── LIVE SCRAPER: Internshala (best effort) ──
    def scrape_internshala(self):
        self.stdout.write("  Scraping Internshala (live)...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            resp = requests.get(
                "https://internshala.com/internships/",
                headers=headers,
                timeout=10
            )
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".individual_internship")
            count = 0
            for card in cards[:10]:  # limit to 10
                try:
                    title_el = card.select_one(".job-internship-name")
                    company_el = card.select_one(".company-name")
                    stipend_el = card.select_one(".stipend")
                    skills_els = card.select(".round_tabs span")
                    link_el = card.select_one("a.job-title-href")

                    title = title_el.text.strip() if title_el else None
                    company = company_el.text.strip() if company_el else "Unknown"
                    skills = ", ".join([s.text.strip() for s in skills_els])
                    stipend = stipend_el.text.strip() if stipend_el else ""
                    url_path = link_el["href"] if link_el else ""

                    if not title:
                        continue

                    Opportunity.objects.get_or_create(
                        title=title,
                        company=company,
                        defaults={
                            "category": "Internship",
                            "description": f"{title} at {company}. {stipend}. Skills: {skills}",
                            "required_skills": skills,
                            "minimum_cgpa": 0,
                            "ai_category": "Technology",
                            "deadline": date.today() + timedelta(days=30),
                        }
                    )
                    count += 1
                except Exception:
                    continue
            self.stdout.write(f"  Scraped {count} live internships from Internshala.")
            time.sleep(1)
        except Exception as e:
            self.stdout.write(f"  Internshala scrape failed (network/structure change): {e}")
            self.stdout.write("  Seed data already loaded as fallback.")