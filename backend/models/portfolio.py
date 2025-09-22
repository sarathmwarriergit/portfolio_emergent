from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# Personal Information Model
class PersonalInfoCreate(BaseModel):
    name: str
    role: str
    sub_role: str
    location: str
    email: str
    phone: str
    linkedin: str
    avatar: Optional[str] = None
    about_summary: str

class PersonalInfo(PersonalInfoCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Skills Model
class SkillCreate(BaseModel):
    category: str
    items: List[str]
    order: int = 0

class Skill(SkillCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Experience Model
class ExperienceCreate(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    duration: str
    logo: Optional[str] = None
    highlights: List[str]
    order: int = 0

class Experience(ExperienceCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Education Model
class EducationCreate(BaseModel):
    degree: str
    institution: str
    year: str
    description: str
    order: int = 0

class Education(EducationCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Language Model
class LanguageCreate(BaseModel):
    name: str
    level: int  # 0-100 proficiency
    order: int = 0

class Language(LanguageCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Contact Message Model
class ContactMessageCreate(BaseModel):
    name: str
    email: str
    message: str

class ContactMessage(ContactMessageCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "unread"  # unread, read, replied
    created_at: datetime = Field(default_factory=datetime.utcnow)