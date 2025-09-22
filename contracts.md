# Backend Integration Contracts - Sarath M Warrier Portfolio

## Overview
This document outlines the API contracts and integration points for converting the frontend-only portfolio to a full-stack application with dynamic data management.

## Current Mock Data Structure

### 1. Personal Information
```javascript
personalInfo: {
  name: "Sarath M Warrier",
  role: "IT Infrastructure & Support Engineer", 
  subRole: "Cybersecurity & DevOps Enthusiast",
  location: "Shoranur, Kerala, India",
  email: "sarathmwarrier@gmail.com",
  phone: "+91-6363-092-902",
  linkedin: "linkedin.com/in/sarathmwarrier",
  avatar: "profile_image_url"
}
```

### 2. Skills Data Structure
```javascript
skills: [
  {
    category: "Microsoft & Directory Services",
    items: ["Active Directory", "Azure AD", "Office 365", ...]
  },
  // 6 categories total with 5 items each
]
```

### 3. Experience Data Structure  
```javascript
experience: [
  {
    id: 1,
    title: "IT & Assets Coordinator",
    company: "Headout Inc.",
    duration: "2025 – Present", 
    logo: "company_logo_url",
    highlights: ["Achievement 1", "Achievement 2", ...]
  },
  // 5 experience entries total
]
```

### 4. Education Data Structure
```javascript
education: [
  {
    degree: "B.Tech in Electronics & Communication",
    institution: "University Name",
    year: "2017",
    description: "Graduation details"
  },
  // 2 education entries
]
```

### 5. Languages Data Structure
```javascript
languages: [
  { name: "English", level: 95 },
  { name: "Malayalam", level: 100 },
  // 4 languages total
]
```

## Required API Endpoints

### Personal Information Endpoints
```
GET /api/personal-info        - Get personal information
PUT /api/personal-info        - Update personal information
```

### Skills Management Endpoints
```
GET /api/skills               - Get all skill categories and items
POST /api/skills              - Create new skill category
PUT /api/skills/:id           - Update skill category
DELETE /api/skills/:id        - Delete skill category
POST /api/skills/:id/items    - Add skill item to category
DELETE /api/skills/:id/items/:itemId - Remove skill item
```

### Experience Management Endpoints
```
GET /api/experience           - Get all work experience (ordered by date)
POST /api/experience          - Create new experience entry
PUT /api/experience/:id       - Update experience entry
DELETE /api/experience/:id    - Delete experience entry
```

### Education Management Endpoints
```
GET /api/education            - Get all education records
POST /api/education           - Create new education record
PUT /api/education/:id        - Update education record
DELETE /api/education/:id     - Delete education record
```

### Languages Management Endpoints
```
GET /api/languages            - Get all languages with proficiency
POST /api/languages           - Add new language
PUT /api/languages/:id        - Update language proficiency
DELETE /api/languages/:id     - Remove language
```

### Contact Form Endpoint
```
POST /api/contact             - Submit contact form message
GET /api/contact              - Get all contact messages (admin)
```

## Database Models

### PersonalInfo Model
```python
class PersonalInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str
    sub_role: str
    location: str
    email: str
    phone: str
    linkedin: str
    avatar: Optional[str] = None
    about_summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Skill Model
```python
class Skill(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str
    items: List[str]
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Experience Model
```python
class Experience(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None  # None for current position
    duration: str  # Computed field
    logo: Optional[str] = None
    highlights: List[str]
    order: int = 0  # For custom ordering
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Education Model
```python
class Education(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    degree: str
    institution: str
    year: str
    description: str
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Language Model
```python
class Language(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    level: int  # 0-100 proficiency
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### ContactMessage Model
```python
class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    message: str
    status: str = "unread"  # unread, read, replied
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Frontend Integration Points

### 1. Replace Mock Data Import
**Current:**
```javascript
import { mockData } from '../mock';
```

**Replace with:**
```javascript
// Remove mock import, use API calls instead
```

### 2. API Service Layer
Create `/frontend/src/services/api.js`:
```javascript
const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api`;

export const portfolioApi = {
  // Personal info
  getPersonalInfo: () => axios.get(`${API_BASE}/personal-info`),
  updatePersonalInfo: (data) => axios.put(`${API_BASE}/personal-info`, data),
  
  // Skills
  getSkills: () => axios.get(`${API_BASE}/skills`),
  
  // Experience  
  getExperience: () => axios.get(`${API_BASE}/experience`),
  
  // Education
  getEducation: () => axios.get(`${API_BASE}/education`),
  
  // Languages
  getLanguages: () => axios.get(`${API_BASE}/languages`),
  
  // Contact
  submitContact: (data) => axios.post(`${API_BASE}/contact`, data),
};
```

### 3. Frontend State Management
Replace static mockData usage with useState/useEffect:

```javascript
const [personalInfo, setPersonalInfo] = useState(null);
const [skills, setSkills] = useState([]);
const [experience, setExperience] = useState([]);
const [education, setEducation] = useState([]);
const [languages, setLanguages] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  const fetchData = async () => {
    try {
      const [personalRes, skillsRes, expRes, eduRes, langRes] = await Promise.all([
        portfolioApi.getPersonalInfo(),
        portfolioApi.getSkills(),
        portfolioApi.getExperience(),
        portfolioApi.getEducation(),
        portfolioApi.getLanguages(),
      ]);
      
      setPersonalInfo(personalRes.data);
      setSkills(skillsRes.data);
      setExperience(expRes.data);
      setEducation(eduRes.data);
      setLanguages(langRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };
  
  fetchData();
}, []);
```

### 4. Contact Form Integration
Replace mock form submission:

**Current:**
```javascript
const handleFormSubmit = (e) => {
  e.preventDefault();
  toast({ title: "Message Sent!", description: "..." });
  setFormData({ name: '', email: '', message: '' });
};
```

**Replace with:**
```javascript
const handleFormSubmit = async (e) => {
  e.preventDefault();
  setSubmitting(true);
  
  try {
    await portfolioApi.submitContact(formData);
    toast({ 
      title: "Message Sent!", 
      description: "Thank you for reaching out. I'll get back to you soon." 
    });
    setFormData({ name: '', email: '', message: '' });
  } catch (error) {
    toast({ 
      title: "Error", 
      description: "Failed to send message. Please try again." 
    });
  } finally {
    setSubmitting(false);
  }
};
```

## Database Seeding Strategy

### Initial Data Population
1. **Personal Info**: Seed with current mock data from mockData.personalInfo
2. **Skills**: Create 6 skill categories with items from mockData.skills  
3. **Experience**: Populate 5 experience entries from mockData.experience
4. **Education**: Add 2 education records from mockData.education
5. **Languages**: Create 4 language proficiency records from mockData.languages

### Seeding Script
Create `/backend/seed_data.py` to populate initial data from mock structure.

## Error Handling Strategy

### Backend Error Responses
```python
# Standardized error response format
{
  "error": "Error type",
  "message": "Human readable message", 
  "details": "Additional details if needed"
}
```

### Frontend Error Handling
```javascript
// Add loading states and error boundaries
if (loading) return <SkeletonLoader />;
if (error) return <ErrorMessage />;
```

## Testing Strategy

### Backend Testing Priority
1. **Experience CRUD** - Most complex with ordering and highlights
2. **Skills CRUD** - Category and items management  
3. **Contact Form** - Form submission and validation
4. **Education CRUD** - Basic CRUD operations
5. **Languages CRUD** - Simple proficiency management

### Frontend Integration Testing
1. **Data Loading** - Verify all sections load from API
2. **Contact Form** - Ensure real form submission works
3. **Error States** - Test network failures gracefully
4. **Loading States** - Verify smooth user experience

## Implementation Order

### Phase 1: Core Backend Setup
1. Create database models
2. Implement basic CRUD for all entities
3. Add data seeding script
4. Test all endpoints

### Phase 2: Frontend Integration  
1. Create API service layer
2. Replace mock data with API calls
3. Add loading and error states
4. Test contact form submission

### Phase 3: Testing & Refinement
1. Backend API testing
2. Frontend integration testing  
3. Error handling validation
4. Performance optimization

## Success Criteria
- ✅ All mock data replaced with database-driven content
- ✅ Contact form saves messages to database
- ✅ Admin can manage all content sections
- ✅ Smooth user experience with loading states  
- ✅ Proper error handling throughout
- ✅ Data persistence across page refreshes