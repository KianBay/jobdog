from enum import StrEnum
from pydantic import BaseModel, HttpUrl
from typing import Optional

class LocationType(StrEnum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"

class ExperienceLevel(StrEnum):
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXECUTIVE = "executive"

class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    VOLUNTEER = "volunteer"
    INTERNSHIP = "internship"

class JobListing(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    job_listing_url: HttpUrl
    location: Optional[str] = None
    location_type: Optional[LocationType] = None
    employment_type: Optional[EmploymentType] = None
    experience_level: Optional[ExperienceLevel] = None
    salary: Optional[str] = None
    currency: Optional[str] = None
    apply_url: Optional[HttpUrl] = None
    job_posting_date: Optional[str] = None
    job_expiry_date: Optional[str] = None
    skills: Optional[list[str]] = None
    industry: Optional[str] = None
    