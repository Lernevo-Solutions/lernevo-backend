import json
import logging
from typing import Dict
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
from vertexai import init
from django.conf import settings
from .vertex_ai_prompts import (
    SUMMARY_PROMPTS, PROJECTS_PROMPTS, EXPERIENCE_PROMPTS,
    CERTIFICATIONS_PROMPTS, EDUCATION_PROMPTS, SKILLS_PROMPTS
)

logger = logging.getLogger(__name__)


class VertexAIService:
    """Vertex AI Service for Resume Builder"""

    def __init__(self):
        try:
            project_id = getattr(settings, "VERTEX_PROJECT_ID", None)
            location = getattr(settings, "VERTEX_LOCATION", None)

            if not project_id or not location:
                raise Exception("Vertex AI config missing")

            init(project=project_id, location=location)

            self.model = GenerativeModel(
                getattr(settings, "VERTEX_MODEL", "gemini-1.5-flash")
            )

            self.config = GenerationConfig(
                temperature=0.5,
                top_p=0.95,
                max_output_tokens=800
            )

            logger.info("Vertex AI initialized successfully")

        except Exception as e:
            logger.error(f"Vertex AI init failed: {e}")
            raise

    # ---------------- SUMMARY ----------------
    def generate_summary(self, user_data: Dict, action: str, current_text: str = "") -> str:
        try:
            if action == "generate":
                prompt = SUMMARY_PROMPTS["generate"].format(
                    title=user_data.get("title", "Professional"),
                    skills=user_data.get("skills", ""),
                    experience_context=user_data.get("experience_context", "")
                )
            else:
                prompt = SUMMARY_PROMPTS["improve"].format(
                    current_text=current_text,
                    title=user_data.get("title", "Professional"),
                    skills=user_data.get("skills", "")
                )

            response = self.model.generate_content(prompt, generation_config=self.config)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Summary error: {e}")
            raise

    # ---------------- PROJECTS ----------------
    def generate_projects(self, user_data: Dict, action: str, current_projects: str = "") -> str:
        try:
            if action == "generate":
                prompt = PROJECTS_PROMPTS["generate"].format(
                    num_projects=user_data.get("num_projects", 3),
                    title=user_data.get("title", "Developer"),
                    tech_stack=user_data.get("tech_stack", ""),
                    context=user_data.get("context", "")
                )
            else:
                prompt = PROJECTS_PROMPTS["improve"].format(
                    current_projects=current_projects,
                    title=user_data.get("title", "Developer")
                )

            response = self.model.generate_content(prompt, generation_config=self.config)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Projects error: {e}")
            raise

    # ---------------- EXPERIENCE ----------------
    def generate_experience(self, user_data: Dict, action: str, current_bullets: str = "") -> str:
        try:
            if action == "generate":
                prompt = EXPERIENCE_PROMPTS["generate"].format(
                    role=user_data.get("role", "Professional"),
                    company=user_data.get("company", "Company"),
                    duration=user_data.get("duration", "Present"),
                    responsibilities=user_data.get("responsibilities", ""),
                    tech=user_data.get("tech_stack", "")
                )
            else:
                prompt = EXPERIENCE_PROMPTS["improve"].format(
                    current_bullets=current_bullets,
                    role=user_data.get("role", "Professional")
                )

            response = self.model.generate_content(prompt, generation_config=self.config)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Experience error: {e}")
            raise

    # ---------------- CERTIFICATIONS ----------------
    def generate_certifications(self, user_data: Dict, action: str, current_certs: str = "") -> Dict:
        try:
            if action == "generate":
                prompt = CERTIFICATIONS_PROMPTS["generate"].format(
                    title=user_data.get("title", "Professional"),
                    skills=user_data.get("skills", ""),
                    industry=user_data.get("industry", "Technology")
                )
            else:
                prompt = CERTIFICATIONS_PROMPTS["improve"].format(
                    current_certs=current_certs
                )

            response = self.model.generate_content(prompt, generation_config=self.config)

            try:
                return json.loads(response.text.strip())
            except:
                return {"certifications": [{"name": line} for line in response.text.split("\n") if line.strip()]}

        except Exception as e:
            logger.error(f"Certifications error: {e}")
            raise

    # ---------------- EDUCATION ----------------
    def generate_education(self, user_data: Dict, action: str, current_education: str = "") -> str:
        try:
            if action == "generate":
                prompt = EDUCATION_PROMPTS["generate"].format(
                    degree=user_data.get("degree", "Bachelor's Degree"),
                    field=user_data.get("field", "Computer Science"),
                    university=user_data.get("university", "University"),
                    year=user_data.get("year", "2024"),
                    coursework=user_data.get("coursework", "")
                )
            else:
                prompt = EDUCATION_PROMPTS["improve"].format(
                    current_education=current_education
                )

            response = self.model.generate_content(prompt, generation_config=self.config)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Education error: {e}")
            raise

    # ---------------- SKILLS ----------------
    def generate_skills(self, user_data: Dict) -> Dict:
        try:
            prompt = SKILLS_PROMPTS["generate"].format(
                title=user_data.get("title", "Professional"),
                current_skills=user_data.get("current_skills", ""),
                level=user_data.get("level", "Intermediate")
            )

            response = self.model.generate_content(prompt, generation_config=self.config)

            try:
                return json.loads(response.text.strip())
            except:
                return {"raw": response.text}

        except Exception as e:
            logger.error(f"Skills error: {e}")
            raise


# Singleton
vertex_service = VertexAIService()