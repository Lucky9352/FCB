#!/usr/bin/env python
"""
Script to create test users for Razorpay testing
Usage: python create_test_user.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_cafe.settings')
django.setup()

from django.contrib.auth.models import User
from authentication.models import Customer


def create_test_user():
    """Create a test user for Razorpay testing"""
    
    print("=" * 60)
    print("TapNex - Create Test User for Razorpay Testing")
    print("=" * 60)
    print()
    
    # Get user details
    username = input("Enter username (default: razorpay_tester): ").strip() or "razorpay_tester"
    email = input("Enter email (default: tester@razorpay.com): ").strip() or "tester@razorpay.com"
    password = input("Enter password (default: TestPass123!): ").strip() or "TestPass123!"
    first_name = input("Enter first name (default: Razorpay): ").strip() or "Razorpay"
    last_name = input("Enter last name (default: Tester): ").strip() or "Tester"
    
    print()
    print("-" * 60)
    print("Creating user with the following details:")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"  Name: {first_name} {last_name}")
    print("-" * 60)
    print()
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"⚠️  User '{username}' already exists!")
        overwrite = input("Do you want to delete and recreate? (yes/no): ").strip().lower()
        if overwrite == 'yes':
            User.objects.filter(username=username).delete()
            print(f"✅ Deleted existing user '{username}'")
        else:
            print("❌ Operation cancelled.")
            return
    
    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"✅ User created successfully: {username}")
        
        # Create customer profile
        customer = Customer.objects.create(
            user=user,
            phone_number="+919876543210"  # Default test phone
        )
        print(f"✅ Customer profile created for: {username}")
        
        print()
        print("=" * 60)
        print("✅ SUCCESS! Test user created.")
        print("=" * 60)
        print()
        print("Login Credentials:")
        print(f"  URL: http://localhost:8000/accounts/login/")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print()
        print("You can now use these credentials to test the Razorpay integration.")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error creating user: {str(e)}")
        sys.exit(1)


def create_multiple_test_users():
    """Create multiple test users at once"""
    
    test_users = [
        {
            'username': 'razorpay_tester1',
            'email': 'tester1@razorpay.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User One'
        },
        {
            'username': 'razorpay_tester2',
            'email': 'tester2@razorpay.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User Two'
        },
        {
            'username': 'razorpay_tester3',
            'email': 'tester3@razorpay.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User Three'
        }
    ]
    
    print("Creating multiple test users...")
    print()
    
    created_count = 0
    for user_data in test_users:
        try:
            # Check if user exists
            if User.objects.filter(username=user_data['username']).exists():
                print(f"⚠️  Skipping {user_data['username']} (already exists)")
                continue
            
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Create customer profile
            Customer.objects.create(user=user, phone_number="+919876543210")
            
            print(f"✅ Created: {user_data['username']}")
            created_count += 1
            
        except Exception as e:
            print(f"❌ Error creating {user_data['username']}: {str(e)}")
    
    print()
    print(f"✅ Created {created_count} test users successfully!")
    print()
    print("Test Credentials (All use password: TestPass123!):")
    for user_data in test_users:
        print(f"  - {user_data['username']} ({user_data['email']})")


if __name__ == '__main__':
    print()
    print("Choose an option:")
    print("1. Create a single test user (interactive)")
    print("2. Create multiple test users (batch)")
    print("3. Exit")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        create_test_user()
    elif choice == '2':
        create_multiple_test_users()
    elif choice == '3':
        print("Exiting...")
    else:
        print("❌ Invalid choice. Exiting...")
