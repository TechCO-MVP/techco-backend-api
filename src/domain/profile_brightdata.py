from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from datetime import date, datetime


class Company(BaseModel):
    company_id: str
    link: HttpUrl
    name: str


class Post(BaseModel):
    created_at: datetime
    id: str
    img: Optional[HttpUrl]
    interaction: Optional[str]
    link: HttpUrl
    title: str


class PersonAlsoViewed(BaseModel):
    about: Optional[str]
    location: str
    name: str
    profile_link: HttpUrl


class Education(BaseModel):
    description: Optional[str]
    description_html: Optional[str]
    end_year: Optional[str]
    institute_logo_url: Optional[HttpUrl]
    start_year: Optional[str]
    title: str


class Language(BaseModel):
    subtitle: str
    title: str


class Certification(BaseModel):
    credential_url: Optional[HttpUrl]
    meta: str
    subtitle: str
    title: str


class VolunteerExperience(BaseModel):
    cause: Optional[str]
    duration: Optional[str]
    duration_short: Optional[str]
    end_date: Optional[str]
    info: Optional[str]
    start_date: Optional[str]
    subtitle: Optional[str]
    title: str


class Course(BaseModel):
    subtitle: str
    title: str


class Organization(BaseModel):
    end_date: Optional[str]
    membership_number: Optional[str]
    membership_type: str
    start_date: Optional[str]
    title: str


class Activity(BaseModel):
    id: str
    img: Optional[HttpUrl]
    interaction: Optional[str]
    link: HttpUrl
    title: Optional[str]


class HonorsAndAwards(BaseModel):
    title: str
    date: str
    description: str
    publication: str


class SimilarProfile(BaseModel):
    name: str
    title: str
    url: str
    url_text: str


class ProfileBrightDataDTO(BaseModel):
    timestamp: date
    linkedin_num_id: str
    name: str
    country_code: str
    position: Optional[str]
    city: str
    current_company: Optional[Company]
    about: Optional[str]
    posts: List[Post]
    experience: Optional[str]
    url: HttpUrl
    people_also_viewed: List[PersonAlsoViewed]
    educations_details: Optional[str]
    education: List[Education]
    recommendations_count: int
    avatar: Optional[HttpUrl]
    languages: List[Language]
    certifications: List[Certification]
    recommendations: List[str]
    volunteer_experience: List[VolunteerExperience]
    courses: List[Course]
    followers: int
    connections: int
    current_company_company_id: Optional[str]
    current_company_name: Optional[str]
    publications: Optional[str]
    patents: Optional[str]
    projects: Optional[str]
    organizations: List[Organization]
    input_url: HttpUrl
    linkedin_id: str
    activity: List[Activity]
    banner_image: str
    honors_and_awards: List[HonorsAndAwards]
    similar_profiles: List[SimilarProfile]
    default_avatar: bool
    memorialized_account: bool
