import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models.portfolio import PersonalInfo, Skill, Experience, Education, Language
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Mock data from frontend
SEED_DATA = {
    "personal_info": {
        "name": "Sarath M Warrier",
        "role": "IT Infrastructure & Support Engineer",
        "sub_role": "Cybersecurity & DevOps Enthusiast",
        "location": "Shoranur, Kerala, India",
        "email": "sarathmwarrier@gmail.com",
        "phone": "+91-6363-092-902",
        "linkedin": "linkedin.com/in/sarathmwarrier",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
        "about_summary": "Experienced IT Infrastructure & Support Engineer with 7+ years of expertise in Microsoft technologies, endpoint management, and cybersecurity. Passionate about implementing robust IT solutions and continuously learning emerging technologies in DevOps and security domains."
    },
    
    "skills": [
        {
            "category": "Microsoft & Directory Services",
            "items": ["Active Directory", "Azure AD", "Office 365", "Exchange Server", "SharePoint"],
            "order": 1
        },
        {
            "category": "Endpoint & Device Management", 
            "items": ["Microsoft Intune", "SCCM", "Group Policy", "Windows Deployment", "Mobile Device Management"],
            "order": 2
        },
        {
            "category": "Networking & Security",
            "items": ["Firewall Configuration", "VPN Setup", "Network Monitoring", "Security Policies", "Vulnerability Assessment"],
            "order": 3
        },
        {
            "category": "Backup & Recovery",
            "items": ["Veeam Backup", "Azure Backup", "Disaster Recovery", "Data Protection", "Business Continuity"],
            "order": 4
        },
        {
            "category": "RMM & Monitoring Tools",
            "items": ["ConnectWise", "SolarWinds", "PRTG", "Nagios", "System Monitoring"],
            "order": 5
        },
        {
            "category": "Ticketing & ITSM Tools",
            "items": ["ServiceNow", "Jira Service Desk", "Freshservice", "ManageEngine", "Help Desk Systems"],
            "order": 6
        }
    ],
    
    "experience": [
        {
            "title": "IT & Assets Coordinator",
            "company": "Headout Inc.",
            "start_date": "2025-01-01",
            "end_date": None,
            "duration": "2025 – Present",
            "logo": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=80&h=80&fit=crop",
            "highlights": [
                "Managing global IT infrastructure and asset lifecycle",
                "Implementing security policies and compliance frameworks",
                "Coordinating with vendors and managing IT budgets",
                "Leading digital transformation initiatives"
            ],
            "order": 1
        },
        {
            "title": "System Engineer",
            "company": "Worksent Technologies Pvt Ltd",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "duration": "2024 – 2025",
            "logo": None,
            "highlights": [
                "Designed and implemented enterprise network solutions",
                "Managed Windows Server environments and virtualization",
                "Automated deployment processes using PowerShell",
                "Provided L2/L3 technical support and troubleshooting"
            ],
            "order": 2
        },
        {
            "title": "Senior System Analyst",
            "company": "Corrohealth Infotech Pvt Ltd",
            "start_date": "2022-01-01",
            "end_date": "2023-12-31",
            "duration": "2022 – 2024",
            "logo": None,
            "highlights": [
                "Led system integration projects and infrastructure upgrades",
                "Implemented backup and disaster recovery solutions",
                "Managed Active Directory and Exchange environments",
                "Coordinated with cross-functional teams for project delivery"
            ],
            "order": 3
        },
        {
            "title": "IT Support Engineer",
            "company": "Way Dot Com India Pvt Ltd",
            "start_date": "2021-01-01",
            "end_date": "2021-12-31",
            "duration": "2021 – 2022",
            "logo": None,
            "highlights": [
                "Provided comprehensive technical support to end users",
                "Managed endpoint security and compliance",
                "Implemented ticketing system workflows",
                "Documented IT processes and procedures"
            ],
            "order": 4
        },
        {
            "title": "Technical Associate",
            "company": "Pacer Automation Pvt Ltd",
            "start_date": "2018-01-01",
            "end_date": "2020-12-31",
            "duration": "2018 – 2021",
            "logo": None,
            "highlights": [
                "Started career in IT support and system administration",
                "Gained expertise in Windows environments and networking",
                "Developed troubleshooting and problem-solving skills",
                "Built foundation in IT service management"
            ],
            "order": 5
        }
    ],
    
    "education": [
        {
            "degree": "B.Tech in Electronics & Communication",
            "institution": "University Name",
            "year": "2017",
            "description": "Graduated with strong foundation in electronics and communication engineering",
            "order": 1
        },
        {
            "degree": "Diploma in Network Engineering", 
            "institution": "Institute Name",
            "year": "2018",
            "description": "Specialized training in network infrastructure and management",
            "order": 2
        }
    ],
    
    "languages": [
        {"name": "English", "level": 95, "order": 1},
        {"name": "Malayalam", "level": 100, "order": 2},
        {"name": "Hindi", "level": 80, "order": 3},
        {"name": "Tamil", "level": 70, "order": 4}
    ]
}

async def seed_database():
    """Seed the database with initial portfolio data"""
    print("🌱 Starting database seeding...")
    
    try:
        # Clear existing data
        collections = ['personal_info', 'skills', 'experience', 'education', 'languages']
        for collection in collections:
            await db[collection].delete_many({})
            print(f"✅ Cleared {collection} collection")
        
        # Seed Personal Info
        personal_info = PersonalInfo(**SEED_DATA["personal_info"])
        await db.personal_info.insert_one(personal_info.dict())
        print("✅ Seeded personal information")
        
        # Seed Skills
        for skill_data in SEED_DATA["skills"]:
            skill = Skill(**skill_data)
            await db.skills.insert_one(skill.dict())
        print(f"✅ Seeded {len(SEED_DATA['skills'])} skill categories")
        
        # Seed Experience
        for exp_data in SEED_DATA["experience"]:
            experience = Experience(**exp_data)
            await db.experience.insert_one(experience.dict())
        print(f"✅ Seeded {len(SEED_DATA['experience'])} experience entries")
        
        # Seed Education
        for edu_data in SEED_DATA["education"]:
            education = Education(**edu_data)
            await db.education.insert_one(education.dict())
        print(f"✅ Seeded {len(SEED_DATA['education'])} education records")
        
        # Seed Languages
        for lang_data in SEED_DATA["languages"]:
            language = Language(**lang_data)
            await db.languages.insert_one(language.dict())
        print(f"✅ Seeded {len(SEED_DATA['languages'])} language records")
        
        print("🎉 Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())