from pydantic import BaseModel, Field
from typing import List, Optional

class EducationSchema(BaseModel):
    degree: str = Field(description="Degree name, e.g., Bachelor of Science in Computer Science")
    institution: str = Field(description="University or Institution name")
    year: Optional[str] = Field(description="Graduation year of duration")

class CVDataSchema(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address of the candidate")
    phone: Optional[str] = Field(description="Phone number of the candidate")
    skills: List[str] = Field(description="List of core technical or soft skills extracted from the CV")
    experience_years: float = Field(description="Total estimated years of professional experience")
    education: List[EducationSchema] = Field(description="List of educational qualifications")
    summary: str = Field(description="A brief professional summary of the candidate based on the CV")