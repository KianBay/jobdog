from enum import StrEnum
from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional


class LocationType(StrEnum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"


class ExperienceLevel(StrEnum):
    INTERN = "intern"
    ENTRY = "entry"
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
    job_function: Optional[str] = None
    job_listing_url: Optional[HttpUrl] = None
    location: Optional[list[str]] = None
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

    @field_validator("location_type", mode="before")
    @classmethod
    def validate_location_type(cls, v):
        if isinstance(v, str):
            return LocationType(v.lower())
        return v

    @field_validator("employment_type", mode="before")
    @classmethod
    def validate_employment_type(cls, v):
        if isinstance(v, str):
            return EmploymentType(v.lower().replace("-", "_").replace(" ", "_"))
        return v

    @field_validator("experience_level", mode="before")
    @classmethod
    def validate_experience_level(cls, v):
        if isinstance(v, str):
            mapping = {
                "entry level": ExperienceLevel.ENTRY,
                "associate": ExperienceLevel.JUNIOR,
                "mid-senior level": ExperienceLevel.MID,
                "director": ExperienceLevel.SENIOR,
            }
            return mapping.get(v.lower(), v)
        return v
