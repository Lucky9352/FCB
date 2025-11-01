#!/usr/bin/env python
"""
Generate a secure SECRET_KEY for Django production use.
Run this script and copy the output to your Vercel environment variables.
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    print("=" * 70)
    print("🔐 DJANGO SECRET KEY GENERATOR")
    print("=" * 70)
    print("\nGenerated SECRET_KEY:")
    print("-" * 70)
    secret_key = get_random_secret_key()
    print(secret_key)
    print("-" * 70)
    print("\n📋 INSTRUCTIONS:")
    print("1. Copy the SECRET_KEY above")
    print("2. Go to Vercel Dashboard > Your Project > Settings > Environment Variables")
    print("3. Add a new variable:")
    print("   - Name: SECRET_KEY")
    print("   - Value: [paste the key above]")
    print("   - Apply to: Production, Preview, Development")
    print("4. Redeploy your application")
    print("\n⚠️  IMPORTANT: Keep this key secret and never commit it to git!")
    print("=" * 70)
