from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class PROFILE_GROUP(str, Enum):
    HIGH = "high"
    MID_HIGH = "mid_high"
    MID = "mid"
    LOW = "low"


class ProfileEvaluation(BaseModel):
    id: str = Field("", description="ID del perfil")
    linkedin_num_id: str = Field("", description="ID del perfil de LinkedIn")
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


class ProfileClusteringResponse(BaseModel):
    evaluations: List[ProfileEvaluation]
