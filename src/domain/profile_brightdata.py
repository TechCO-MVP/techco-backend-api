from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from src.domain.profile_evaluation import ProfileEvaluation


class Company(BaseModel):
    company_id: Optional[str] = None
    link: Optional[str] = None
    name: Optional[str] = None


class Post(BaseModel):
    created_at: Optional[datetime] = None
    id: Optional[str] = None
    img: Optional[str] = None
    interaction: Optional[str] = None
    link: Optional[str] = None
    title: Optional[str] = None


class PersonAlsoViewed(BaseModel):
    about: Optional[str] = None
    location: Optional[str] = None
    name: Optional[str] = None
    profile_link: Optional[str] = None


class ExperienceProfile(BaseModel):
    company: Optional[str] = Field(None, description="Company name")
    company_id: Optional[str] = Field(None, description="Unique identifier for the company")
    company_logo_url: Optional[str] = Field(None, description="URL of the company logo")
    description: Optional[str] = Field(None, description="Text description of the experience")
    description_html: Optional[str] = Field(
        None, description="HTML formatted description of the experience"
    )
    duration: Optional[str] = Field(
        None, description="Full duration of the experience including months and years"
    )
    duration_short: Optional[str] = Field(None, description="Shortened version of duration")
    end_date: Optional[str] = Field(
        None, description="End date of the experience, or 'Present' if ongoing"
    )
    location: Optional[str] = Field(None, description="Location where the experience took place")
    start_date: Optional[str] = Field(None, description="Start date of the experience")
    title: Optional[str] = Field(None, description="Job title in the company")
    url: Optional[str] = Field(None, description="Company's LinkedIn or official website URL")


class Education(BaseModel):
    description: Optional[str] = None
    description_html: Optional[str] = None
    end_year: Optional[str] = None
    institute_logo_url: Optional[str] = None
    start_year: Optional[str] = None
    title: Optional[str] = None


class Language(BaseModel):
    subtitle: Optional[str] = None
    title: Optional[str] = None


class Certification(BaseModel):
    credential_url: Optional[str] = None
    meta: Optional[str] = None
    subtitle: Optional[str] = None
    title: Optional[str] = None


class VolunteerExperience(BaseModel):
    cause: Optional[str] = None
    duration: Optional[str] = None
    duration_short: Optional[str] = None
    end_date: Optional[str] = None
    info: Optional[str] = None
    start_date: Optional[str] = None
    subtitle: Optional[str] = None
    title: Optional[str] = None


class Course(BaseModel):
    subtitle: Optional[str] = None
    title: Optional[str] = None


class Organization(BaseModel):
    end_date: Optional[str] = None
    membership_number: Optional[str] = None
    membership_type: Optional[str] = None
    start_date: Optional[str] = None
    title: Optional[str] = None


class Activity(BaseModel):
    id: Optional[str] = None
    img: Optional[str] = None
    interaction: Optional[str] = None
    link: Optional[str] = None
    title: Optional[str] = None


class HonorsAndAwards(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    publication: Optional[str] = None


class SimilarProfile(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    url_text: Optional[str] = None


class ProfileBrightDataDTO(BaseModel):
    timestamp: str
    linkedin_num_id: str
    name: Optional[str] = None
    country_code: Optional[str] = None
    position: Optional[str] = None
    city: Optional[str] = None
    current_company: Optional[Company] = None
    about: Optional[str] = None
    posts: Optional[List[Post]] = None
    experience: Optional[List[ExperienceProfile]] = None
    url: Optional[str] = None
    people_also_viewed: Optional[List[PersonAlsoViewed]] = None
    educations_details: Optional[str] = None
    education: Optional[List[Education]] = None
    recommendations_count: Optional[int] = None
    avatar: Optional[str] = None
    languages: Optional[List[Language]] = None
    certifications: Optional[List[Certification]] = None
    recommendations: Optional[List[str]] = None
    volunteer_experience: Optional[List[VolunteerExperience]] = None
    courses: Optional[List[Course]] = None
    followers: Optional[int] = None
    connections: Optional[int] = None
    current_company_company_id: Optional[str] = None
    current_company_name: Optional[str] = None
    publications: Optional[str] = None
    patents: Optional[str] = None
    projects: Optional[str] = None
    organizations: Optional[List[Organization]] = None
    input_url: Optional[str] = None
    linkedin_id: Optional[str] = None
    activity: Optional[List[Activity]] = None
    banner_image: Optional[str] = None
    honors_and_awards: Optional[List[HonorsAndAwards]] = None
    similar_profiles: Optional[List[SimilarProfile]] = None
    default_avatar: Optional[bool] = None
    memorialized_account: Optional[bool] = None
    profile_evaluation: Optional[ProfileEvaluation] = None
    link_vacancy_form: Optional[str] = None
    card_id: Optional[str] = None
