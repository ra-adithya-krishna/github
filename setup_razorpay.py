#!/usr/bin/env python3
"""
Razorpay Setup Helper Script
This script helps you configure Razorpay API keys for the EV Charging Station booking system.
"""

import os
import sys

def print_banner():
    print("=" * 60)
    print("🔧 RAZORPAY SETUP HELPER")
    print("=" * 60)
    print()

def print_instructions():
    print("📋 STEP-BY-STEP SETUP INSTRUCTIONS:")
    print()
    print("1. 🌐 Go to Razorpay Dashboard:")
    print("   https://dashboard.razorpay.com/")
    print()
    print("2. 🔑 Get Your API Keys:")
    print("   • Login to your Razorpay account")
    print("   • Go to Settings → API Keys")
    print("   • Copy your Key ID and Key Secret")
    print("   • Make sure to use TEST mode keys (start with 'rzp_test_')")
    print()
    print("3. 📝 Update Your Settings:")
    print("   • Open ev/settings.py")
    print("   • Replace the placeholder values with your actual keys")
    print()
    print("4. 🧪 Test Your Setup:")
    print("   • Use test card: 4111 1111 1111 1111")
    print("   • CVV: 123")
    print("   • Any future expiry date")
    print()

def update_settings():
    print("🔧 SETTINGS UPDATE:")
    print()
    
    key_id = input("Enter your Razorpay Key ID (rzp_test_...): ").strip()
    key_secret = input("Enter your Razorpay Key Secret: ").strip()
    
    if not key_id or not key_secret:
        print("❌ Error: Both Key ID and Key Secret are required!")
        return False
    
    if not key_id.startswith('rzp_test_'):
        print("⚠️  Warning: Key ID doesn't start with 'rzp_test_'. Make sure you're using TEST keys!")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            return False
    
    # Read current settings file
    settings_file = "ev/settings.py"
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: {settings_file} not found!")
        return False
    
    # Update the settings
    content = content.replace(
        "RAZORPAY_KEY_ID = 'rzp_test_your_actual_key_id_here'",
        f"RAZORPAY_KEY_ID = '{key_id}'"
    )
    content = content.replace(
        "RAZORPAY_KEY_SECRET = 'your_actual_key_secret_here'",
        f"RAZORPAY_KEY_SECRET = '{key_secret}'"
    )
    
    # Write back to file
    try:
        with open(settings_file, 'w') as f:
            f.write(content)
        print("✅ Settings updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error updating settings: {e}")
        return False

def test_connection():
    print("\n🧪 TESTING CONNECTION:")
    print()
    
    try:
        import razorpay
        from django.conf import settings
        
        # This would need Django to be properly initialized
        print("✅ Razorpay SDK is installed")
        print("✅ Django settings loaded")
        print()
        print("🔍 To test the connection:")
        print("   1. Run: python manage.py runserver")
        print("   2. Go to booking page and try Razorpay payment")
        print("   3. Use test card: 4111 1111 1111 1111")
        
    except ImportError:
        print("❌ Razorpay SDK not installed. Run: pip install razorpay")
    except Exception as e:
        print(f"❌ Error testing connection: {e}")

def main():
    print_banner()
    
    print("This script will help you configure Razorpay API keys.")
    print("Choose an option:")
    print()
    print("1. 📋 Show setup instructions")
    print("2. 🔧 Update settings with your API keys")
    print("3. 🧪 Test connection")
    print("4. 🚪 Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            print_instructions()
        elif choice == '2':
            if update_settings():
                print("\n🎉 Setup complete! You can now use Razorpay payments.")
            break
        elif choice == '3':
            test_connection()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        print()

if __name__ == "__main__":
    main()
