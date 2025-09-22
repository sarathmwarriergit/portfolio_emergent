#!/usr/bin/env python3
"""
Backend API Test Suite for Sarath M Warrier Portfolio
Tests all portfolio endpoints with comprehensive validation
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"❌ Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("❌ Could not get backend URL from frontend/.env")
    sys.exit(1)

API_BASE = f"{BASE_URL}/api"

class PortfolioAPITester:
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        
        if not success:
            self.failed_tests.append(result)
            if details:
                print(f"   Details: {details}")
    
    def test_api_health(self):
        """Test basic API health"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Health Check", True, f"API is running - {data.get('message', 'OK')}")
                return True
            else:
                self.log_test("API Health Check", False, f"API returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"Failed to connect to API: {str(e)}")
            return False
    
    def test_personal_info(self):
        """Test GET /api/personal-info endpoint"""
        try:
            response = requests.get(f"{API_BASE}/personal-info", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate required fields
                required_fields = ['name', 'role', 'sub_role', 'location', 'email', 'phone', 'linkedin', 'about_summary']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Personal Info - Structure", False, 
                                f"Missing required fields: {missing_fields}", {'response': data})
                    return False
                
                # Validate specific data
                if data['name'] == "Sarath M Warrier" and data['email'] == "sarathmwarrier@gmail.com":
                    self.log_test("Personal Info - Data", True, 
                                f"Personal info retrieved successfully with correct data")
                    self.log_test("Personal Info - Fields", True, 
                                f"All required fields present: {len(required_fields)} fields")
                    return True
                else:
                    self.log_test("Personal Info - Data", False, 
                                f"Data doesn't match expected values", {'response': data})
                    return False
            else:
                self.log_test("Personal Info", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Personal Info", False, f"Request failed: {str(e)}")
            return False
    
    def test_skills(self):
        """Test GET /api/skills endpoint"""
        try:
            response = requests.get(f"{API_BASE}/skills", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Skills - Structure", False, "Response is not a list", {'response': data})
                    return False
                
                if len(data) != 6:
                    self.log_test("Skills - Count", False, 
                                f"Expected 6 skill categories, got {len(data)}", {'count': len(data)})
                    return False
                
                # Validate skill structure
                for skill in data:
                    required_fields = ['category', 'items', 'order']
                    missing_fields = [field for field in required_fields if field not in skill]
                    if missing_fields:
                        self.log_test("Skills - Structure", False, 
                                    f"Skill missing fields: {missing_fields}", {'skill': skill})
                        return False
                    
                    if not isinstance(skill['items'], list):
                        self.log_test("Skills - Items", False, 
                                    f"Items field is not a list in category: {skill.get('category')}")
                        return False
                
                # Check for expected categories
                categories = [skill['category'] for skill in data]
                expected_categories = [
                    "Microsoft & Directory Services",
                    "Endpoint & Device Management", 
                    "Networking & Security",
                    "Backup & Recovery",
                    "RMM & Monitoring Tools",
                    "Ticketing & ITSM Tools"
                ]
                
                missing_categories = [cat for cat in expected_categories if cat not in categories]
                if missing_categories:
                    self.log_test("Skills - Categories", False, 
                                f"Missing expected categories: {missing_categories}")
                    return False
                
                self.log_test("Skills - Data", True, 
                            f"All 6 skill categories retrieved with correct structure")
                return True
                
            else:
                self.log_test("Skills", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Skills", False, f"Request failed: {str(e)}")
            return False
    
    def test_experience(self):
        """Test GET /api/experience endpoint"""
        try:
            response = requests.get(f"{API_BASE}/experience", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Experience - Structure", False, "Response is not a list", {'response': data})
                    return False
                
                if len(data) != 5:
                    self.log_test("Experience - Count", False, 
                                f"Expected 5 experience entries, got {len(data)}", {'count': len(data)})
                    return False
                
                # Validate experience structure
                for exp in data:
                    required_fields = ['title', 'company', 'start_date', 'duration', 'highlights', 'order']
                    missing_fields = [field for field in required_fields if field not in exp]
                    if missing_fields:
                        self.log_test("Experience - Structure", False, 
                                    f"Experience missing fields: {missing_fields}", {'experience': exp})
                        return False
                    
                    if not isinstance(exp['highlights'], list):
                        self.log_test("Experience - Highlights", False, 
                                    f"Highlights field is not a list for: {exp.get('title')}")
                        return False
                
                # Check for expected companies
                companies = [exp['company'] for exp in data]
                expected_companies = ["Headout Inc.", "Worksent Technologies Pvt Ltd", 
                                    "Corrohealth Infotech Pvt Ltd", "Way Dot Com India Pvt Ltd", 
                                    "Pacer Automation Pvt Ltd"]
                
                missing_companies = [comp for comp in expected_companies if comp not in companies]
                if missing_companies:
                    self.log_test("Experience - Companies", False, 
                                f"Missing expected companies: {missing_companies}")
                    return False
                
                self.log_test("Experience - Data", True, 
                            f"All 5 experience entries retrieved with correct structure")
                return True
                
            else:
                self.log_test("Experience", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Experience", False, f"Request failed: {str(e)}")
            return False
    
    def test_education(self):
        """Test GET /api/education endpoint"""
        try:
            response = requests.get(f"{API_BASE}/education", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Education - Structure", False, "Response is not a list", {'response': data})
                    return False
                
                if len(data) != 2:
                    self.log_test("Education - Count", False, 
                                f"Expected 2 education records, got {len(data)}", {'count': len(data)})
                    return False
                
                # Validate education structure
                for edu in data:
                    required_fields = ['degree', 'institution', 'year', 'description', 'order']
                    missing_fields = [field for field in required_fields if field not in edu]
                    if missing_fields:
                        self.log_test("Education - Structure", False, 
                                    f"Education missing fields: {missing_fields}", {'education': edu})
                        return False
                
                # Check for expected degrees
                degrees = [edu['degree'] for edu in data]
                expected_degrees = ["B.Tech in Electronics & Communication", "Diploma in Network Engineering"]
                
                missing_degrees = [deg for deg in expected_degrees if deg not in degrees]
                if missing_degrees:
                    self.log_test("Education - Degrees", False, 
                                f"Missing expected degrees: {missing_degrees}")
                    return False
                
                self.log_test("Education - Data", True, 
                            f"All 2 education records retrieved with correct structure")
                return True
                
            else:
                self.log_test("Education", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Education", False, f"Request failed: {str(e)}")
            return False
    
    def test_languages(self):
        """Test GET /api/languages endpoint"""
        try:
            response = requests.get(f"{API_BASE}/languages", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Languages - Structure", False, "Response is not a list", {'response': data})
                    return False
                
                if len(data) != 4:
                    self.log_test("Languages - Count", False, 
                                f"Expected 4 language records, got {len(data)}", {'count': len(data)})
                    return False
                
                # Validate language structure
                for lang in data:
                    required_fields = ['name', 'level', 'order']
                    missing_fields = [field for field in required_fields if field not in lang]
                    if missing_fields:
                        self.log_test("Languages - Structure", False, 
                                    f"Language missing fields: {missing_fields}", {'language': lang})
                        return False
                    
                    # Validate level is a number between 0-100
                    if not isinstance(lang['level'], int) or lang['level'] < 0 or lang['level'] > 100:
                        self.log_test("Languages - Level", False, 
                                    f"Invalid level for {lang['name']}: {lang['level']}")
                        return False
                
                # Check for expected languages
                languages = [lang['name'] for lang in data]
                expected_languages = ["English", "Malayalam", "Hindi", "Tamil"]
                
                missing_languages = [lang for lang in expected_languages if lang not in languages]
                if missing_languages:
                    self.log_test("Languages - Names", False, 
                                f"Missing expected languages: {missing_languages}")
                    return False
                
                self.log_test("Languages - Data", True, 
                            f"All 4 language records retrieved with correct structure and levels")
                return True
                
            else:
                self.log_test("Languages", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Languages", False, f"Request failed: {str(e)}")
            return False
    
    def test_contact_post(self):
        """Test POST /api/contact endpoint"""
        try:
            # Test data
            contact_data = {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "message": "Hello, I'm interested in your portfolio and would like to discuss potential opportunities."
            }
            
            response = requests.post(f"{API_BASE}/contact", 
                                   json=contact_data, 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ['name', 'email', 'message', 'id', 'status', 'created_at']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Contact POST - Structure", False, 
                                f"Missing fields in response: {missing_fields}", {'response': data})
                    return False
                
                # Validate data matches input
                if (data['name'] == contact_data['name'] and 
                    data['email'] == contact_data['email'] and 
                    data['message'] == contact_data['message']):
                    self.log_test("Contact POST - Data", True, 
                                f"Contact message submitted successfully with correct data")
                    return True
                else:
                    self.log_test("Contact POST - Data", False, 
                                f"Response data doesn't match input", 
                                {'input': contact_data, 'response': data})
                    return False
                    
            else:
                self.log_test("Contact POST", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Contact POST", False, f"Request failed: {str(e)}")
            return False
    
    def test_contact_get(self):
        """Test GET /api/contact endpoint"""
        try:
            response = requests.get(f"{API_BASE}/contact", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Contact GET - Structure", False, "Response is not a list", {'response': data})
                    return False
                
                # Should have at least the message we just posted
                if len(data) >= 1:
                    # Validate structure of first message
                    message = data[0]
                    required_fields = ['name', 'email', 'message', 'id', 'status', 'created_at']
                    missing_fields = [field for field in required_fields if field not in message]
                    
                    if missing_fields:
                        self.log_test("Contact GET - Structure", False, 
                                    f"Missing fields in message: {missing_fields}", {'message': message})
                        return False
                    
                    self.log_test("Contact GET - Data", True, 
                                f"Retrieved {len(data)} contact messages with correct structure")
                    return True
                else:
                    self.log_test("Contact GET - Data", False, 
                                f"No contact messages found, expected at least 1")
                    return False
                    
            else:
                self.log_test("Contact GET", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Contact GET", False, f"Request failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print(f"🚀 Starting Portfolio API Tests")
        print(f"📍 Backend URL: {BASE_URL}")
        print(f"📍 API Base: {API_BASE}")
        print("=" * 60)
        
        # Test API health first
        if not self.test_api_health():
            print("❌ API health check failed. Stopping tests.")
            return False
        
        # Run all endpoint tests
        tests = [
            self.test_personal_info,
            self.test_skills,
            self.test_experience,
            self.test_education,
            self.test_languages,
            self.test_contact_post,
            self.test_contact_get
        ]
        
        for test in tests:
            test()
        
        # Print summary
        print("=" * 60)
        print(f"📊 TEST SUMMARY")
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {len(self.test_results) - len(self.failed_tests)}")
        print(f"Failed: {len(self.failed_tests)}")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        else:
            print("\n✅ ALL TESTS PASSED!")
        
        return len(self.failed_tests) == 0

if __name__ == "__main__":
    tester = PortfolioAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)