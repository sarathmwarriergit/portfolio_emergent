from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models.portfolio import (
    PersonalInfo, PersonalInfoCreate,
    Skill, SkillCreate,
    Experience, ExperienceCreate,
    Education, EducationCreate,
    Language, LanguageCreate,
    ContactMessage, ContactMessageCreate
)
from typing import List
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Get database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/api")

# Personal Information Endpoints
@router.get("/personal-info", response_model=PersonalInfo)
async def get_personal_info():
    """Get personal information"""
    personal_info = await db.personal_info.find_one()
    if not personal_info:
        raise HTTPException(status_code=404, detail="Personal information not found")
    return PersonalInfo(**personal_info)

@router.put("/personal-info", response_model=PersonalInfo)
async def update_personal_info(info: PersonalInfoCreate):
    """Update personal information"""
    existing = await db.personal_info.find_one()
    if existing:
        # Update existing record
        update_data = info.dict()
        update_data["updated_at"] = datetime.utcnow()
        result = await db.personal_info.update_one(
            {"id": existing["id"]}, 
            {"$set": update_data}
        )
        if result.modified_count:
            updated = await db.personal_info.find_one({"id": existing["id"]})
            return PersonalInfo(**updated)
        raise HTTPException(status_code=400, detail="Failed to update personal info")
    else:
        # Create new record
        new_info = PersonalInfo(**info.dict())
        await db.personal_info.insert_one(new_info.dict())
        return new_info

# Skills Endpoints
@router.get("/skills", response_model=List[Skill])
async def get_skills():
    """Get all skill categories ordered by order field"""
    skills_cursor = db.skills.find().sort("order", 1)
    skills = await skills_cursor.to_list(1000)
    return [Skill(**skill) for skill in skills]

@router.post("/skills", response_model=Skill)
async def create_skill(skill: SkillCreate):
    """Create new skill category"""
    new_skill = Skill(**skill.dict())
    await db.skills.insert_one(new_skill.dict())
    return new_skill

@router.put("/skills/{skill_id}", response_model=Skill)
async def update_skill(skill_id: str, skill: SkillCreate):
    """Update skill category"""
    update_data = skill.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await db.skills.update_one(
        {"id": skill_id}, 
        {"$set": update_data}
    )
    if result.modified_count:
        updated = await db.skills.find_one({"id": skill_id})
        return Skill(**updated)
    raise HTTPException(status_code=404, detail="Skill category not found")

@router.delete("/skills/{skill_id}")
async def delete_skill(skill_id: str):
    """Delete skill category"""
    result = await db.skills.delete_one({"id": skill_id})
    if result.deleted_count:
        return {"message": "Skill category deleted successfully"}
    raise HTTPException(status_code=404, detail="Skill category not found")

# Experience Endpoints
@router.get("/experience", response_model=List[Experience])
async def get_experience():
    """Get all work experience ordered by order field"""
    exp_cursor = db.experience.find().sort("order", 1)
    experience = await exp_cursor.to_list(1000)
    return [Experience(**exp) for exp in experience]

@router.post("/experience", response_model=Experience)
async def create_experience(experience: ExperienceCreate):
    """Create new experience entry"""
    new_exp = Experience(**experience.dict())
    await db.experience.insert_one(new_exp.dict())
    return new_exp

@router.put("/experience/{exp_id}", response_model=Experience)
async def update_experience(exp_id: str, experience: ExperienceCreate):
    """Update experience entry"""
    update_data = experience.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await db.experience.update_one(
        {"id": exp_id}, 
        {"$set": update_data}
    )
    if result.modified_count:
        updated = await db.experience.find_one({"id": exp_id})
        return Experience(**updated)
    raise HTTPException(status_code=404, detail="Experience entry not found")

@router.delete("/experience/{exp_id}")
async def delete_experience(exp_id: str):
    """Delete experience entry"""
    result = await db.experience.delete_one({"id": exp_id})
    if result.deleted_count:
        return {"message": "Experience entry deleted successfully"}
    raise HTTPException(status_code=404, detail="Experience entry not found")

# Education Endpoints
@router.get("/education", response_model=List[Education])
async def get_education():
    """Get all education records ordered by order field"""
    edu_cursor = db.education.find().sort("order", 1)
    education = await edu_cursor.to_list(1000)
    return [Education(**edu) for edu in education]

@router.post("/education", response_model=Education)
async def create_education(education: EducationCreate):
    """Create new education record"""
    new_edu = Education(**education.dict())
    await db.education.insert_one(new_edu.dict())
    return new_edu

@router.put("/education/{edu_id}", response_model=Education)
async def update_education(edu_id: str, education: EducationCreate):
    """Update education record"""
    update_data = education.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await db.education.update_one(
        {"id": edu_id}, 
        {"$set": update_data}
    )
    if result.modified_count:
        updated = await db.education.find_one({"id": edu_id})
        return Education(**updated)
    raise HTTPException(status_code=404, detail="Education record not found")

@router.delete("/education/{edu_id}")
async def delete_education(edu_id: str):
    """Delete education record"""
    result = await db.education.delete_one({"id": edu_id})
    if result.deleted_count:
        return {"message": "Education record deleted successfully"}
    raise HTTPException(status_code=404, detail="Education record not found")

# Languages Endpoints
@router.get("/languages", response_model=List[Language])
async def get_languages():
    """Get all languages ordered by order field"""
    lang_cursor = db.languages.find().sort("order", 1)
    languages = await lang_cursor.to_list(1000)
    return [Language(**lang) for lang in languages]

@router.post("/languages", response_model=Language)
async def create_language(language: LanguageCreate):
    """Create new language record"""
    new_lang = Language(**language.dict())
    await db.languages.insert_one(new_lang.dict())
    return new_lang

@router.put("/languages/{lang_id}", response_model=Language)
async def update_language(lang_id: str, language: LanguageCreate):
    """Update language record"""
    update_data = language.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await db.languages.update_one(
        {"id": lang_id}, 
        {"$set": update_data}
    )
    if result.modified_count:
        updated = await db.languages.find_one({"id": lang_id})
        return Language(**updated)
    raise HTTPException(status_code=404, detail="Language record not found")

@router.delete("/languages/{lang_id}")
async def delete_language(lang_id: str):
    """Delete language record"""
    result = await db.languages.delete_one({"id": lang_id})
    if result.deleted_count:
        return {"message": "Language record deleted successfully"}
    raise HTTPException(status_code=404, detail="Language record not found")

# Contact Form Endpoint
@router.post("/contact", response_model=ContactMessage)
async def submit_contact(contact: ContactMessageCreate):
    """Submit contact form message"""
    new_message = ContactMessage(**contact.dict())
    await db.contact_messages.insert_one(new_message.dict())
    return new_message

@router.get("/contact", response_model=List[ContactMessage])
async def get_contact_messages():
    """Get all contact messages (admin endpoint)"""
    messages_cursor = db.contact_messages.find().sort("created_at", -1)
    messages = await messages_cursor.to_list(1000)
    return [ContactMessage(**msg) for msg in messages]