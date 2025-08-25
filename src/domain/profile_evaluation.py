from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class PROFILE_GROUP(str, Enum):
    HIGH = "high"
    MID_HIGH = "mid_high"
    MID = "mid"
    LOW = "low"


class CompanyExperience(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: str
    duration: Optional[str] = None


class CurrentCompany(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: str


class Education(BaseModel):
    institution: str
    title: str
    end_year: str


class Candidate(BaseModel):
    name: str
    country_code: str
    city: str
    position: List[str]
    about: str
    url_linkedin: str
    email: Optional[str] = None
    phone: Optional[str] = None
    current_company: List[CurrentCompany]
    experience: List[CompanyExperience]
    education: List[Education]


class ProfileEvaluation(BaseModel):
    id: str = Field("", description="ID del perfil")
    linkedin_num_id: Optional[str] = Field("", description="ID del perfil de LinkedIn")
    group: PROFILE_GROUP
    score: float = Field(..., description="Puntaje de la evaluación", min=0, max=10)
    description: str = Field(..., description="Análisis de por qué hace match con la vacante.")
    vulnerabilities: List[str] = Field(
        ...,
        description=(
            "Análisis de qué cosas le hacen falta para cumplir con los criterios de la vacante."
        ),
    )
    recomendations: List[str] = Field(
        ..., description="Recomendaciones de por qué sí o por qué no avanzar con ese candidato."
    )
    candidate: Optional[Candidate] = None


class ProfileClusteringResponse(BaseModel):
    evaluations: List[ProfileEvaluation]
