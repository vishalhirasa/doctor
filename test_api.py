#!/usr/bin/env python3
"""
Test script for the Flask Registration API
This script demonstrates the API functionality by registering a user and retrieving users.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_register_user():
    """Test user registration via API"""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com", 
        "phone": "1234567890",
        "username": "johndoe",
        "password": "password123",
        "date_of_birth": "1990-01-15",
        "gender": "male",
        "country": "us",
        "newsletter": True
    }
    
    print("🚀 Testing user registration via API...")
    print(f"📤 Sending POST request to {BASE_URL}/api/register")
    print(f"📊 User data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/register", 
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📈 Response Status Code: {response.status_code}")
        print(f"📋 Response Data: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ User registration successful!")
            return True
        else:
            print("❌ User registration failed!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_get_users():
    """Test getting all users via API"""
    print("\n📋 Testing get all users via API...")
    print(f"📤 Sending GET request to {BASE_URL}/api/users")
    
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        
        print(f"📈 Response Status Code: {response.status_code}")
        print(f"📋 Response Data: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Get users successful!")
            return True
        else:
            print("❌ Get users failed!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_duplicate_registration():
    """Test duplicate user registration to check validation"""
    user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "john.doe@example.com",  # Same email as previous user
        "phone": "9876543210",
        "username": "janedoe",
        "password": "password456",
        "date_of_birth": "1992-05-20",
        "gender": "female",
        "country": "ca",
        "newsletter": False
    }
    
    print("\n🔄 Testing duplicate email registration...")
    print(f"📤 Sending POST request with duplicate email")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/register", 
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📈 Response Status Code: {response.status_code}")
        print(f"📋 Response Data: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✅ Duplicate validation working correctly!")
            return True
        else:
            print("❌ Duplicate validation not working!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Flask Registration API Test Suite")
    print("=" * 50)
    
    # Test 1: Register a new user
    success1 = test_register_user()
    
    # Test 2: Get all users
    success2 = test_get_users()
    
    # Test 3: Test duplicate registration
    success3 = test_duplicate_registration()
    
    # Test 4: Get users again to see the registered user
    print("\n📋 Getting users again to see registered user...")
    success4 = test_get_users()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"{'✅' if success1 else '❌'} User Registration: {'PASS' if success1 else 'FAIL'}")
    print(f"{'✅' if success2 else '❌'} Get Users (Empty): {'PASS' if success2 else 'FAIL'}")
    print(f"{'✅' if success3 else '❌'} Duplicate Validation: {'PASS' if success3 else 'FAIL'}")
    print(f"{'✅' if success4 else '❌'} Get Users (With Data): {'PASS' if success4 else 'FAIL'}")
    
    if all([success1, success2, success3, success4]):
        print("\n🎉 All tests passed! The API is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Please check the application.")

if __name__ == "__main__":
    main()