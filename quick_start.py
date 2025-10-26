#!/usr/bin/env python3
"""Quick start script to test the VC Scout Agent with a sample founder."""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_setup():
    """Check if the environment is properly configured."""
    import os
    
    missing_keys = []
    
    if not os.getenv("OPENROUTER_API_KEY"):
        missing_keys.append("OPENROUTER_API_KEY")
    
    if not os.getenv("EXA_API_KEY"):
        missing_keys.append("EXA_API_KEY")
    
    if missing_keys:
        print("❌ ERROR: Missing required API keys in .env file:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n💡 Please create a .env file from .env.example and add your API keys.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True


def run_sample_scout():
    """Run a sample founder scout to verify everything works."""
    from vc_scout_agent import FounderScoutCrew
    
    print("\n" + "="*80)
    print("🎯 VC SCOUT AGENT - QUICK START TEST")
    print("="*80)
    print("\n📋 This will scout a sample founder to verify your setup.")
    print("⏱️  This may take 2-3 minutes as agents research and analyze...\n")
    
    # Ask user for founder or use default
    use_default = input("Use default founder (Sam Altman, OpenAI)? [Y/n]: ").strip().lower()
    
    if use_default in ['', 'y', 'yes']:
        founder_info = "Sam Altman, OpenAI"
    else:
        founder_info = input("Enter founder name and company: ").strip()
        if not founder_info:
            print("❌ No founder provided. Exiting.")
            return
    
    print(f"\n🔍 Starting scout for: {founder_info}")
    print("-" * 80)
    
    try:
        scout = FounderScoutCrew()
        result = scout.scout_founder(founder_info)
        
        print("\n" + "="*80)
        print("📊 FINAL EVALUATION REPORT")
        print("="*80 + "\n")
        print(result)
        
        # Save report
        output_dir = Path("scout_reports")
        output_dir.mkdir(exist_ok=True)
        
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in founder_info)
        safe_filename = safe_filename.replace(' ', '_').lower()[:50]
        
        output_file = output_dir / f"{safe_filename}_quickstart.txt"
        output_file.write_text(str(result))
        
        print("\n" + "="*80)
        print(f"✅ Success! Report saved to: {output_file}")
        print("="*80 + "\n")
        
        print("🎉 Your VC Scout Agent is working perfectly!")
        print("\n📖 Next steps:")
        print("   1. Run 'uv run python -m vc_scout_agent.main' for interactive mode")
        print("   2. Check example.py for more usage examples")
        print("   3. Read README.md for full documentation\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify your API keys in .env")
        print("   2. Check your internet connection")
        print("   3. Ensure you have sufficient API credits")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main function."""
    print("\n🚀 VC Scout Agent - Quick Start Setup\n")
    
    if not check_setup():
        sys.exit(1)
    
    run_sample_scout()


if __name__ == "__main__":
    main()
