"""Main entry point for the VC Scout Agent."""

import sys
from typing import Optional
from pathlib import Path

from dotenv import load_dotenv

from .workflows import FounderScoutCrew
from .config import settings


def main(founder_info: Optional[str] = None):
    """
    Main function to run the VC Scout Agent.
    
    Args:
        founder_info: Information about the founder to scout
                     (e.g., "Sam Altman, OpenAI" or "Patrick Collison, Stripe")
    """
    # Load environment variables
    load_dotenv()
    
    # Verify API keys are set
    try:
        _ = settings.openrouter_api_key
        _ = settings.exa_api_key
    except Exception as e:
        print("ERROR: Missing required API keys. Please check your .env file.")
        print(f"Details: {e}")
        print("\nRequired environment variables:")
        print("  - OPENROUTER_API_KEY")
        print("  - EXA_API_KEY")
        sys.exit(1)
    
    # Get founder info from command line if not provided
    if not founder_info:
        if len(sys.argv) > 1:
            founder_info = " ".join(sys.argv[1:])
        else:
            print("VC Scout Agent - Founder Intelligence System")
            print("=" * 60)
            founder_info = input("\nEnter founder name and company (e.g., 'Sam Altman, OpenAI'): ")
    
    if not founder_info.strip():
        print("ERROR: Founder information is required.")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"Starting comprehensive founder scout for: {founder_info}")
    print(f"{'='*80}\n")
    
    # Initialize the scout crew
    scout_crew = FounderScoutCrew()
    
    # Run the scouting workflow
    try:
        result = scout_crew.scout_founder(founder_info)
        
        print(f"\n{'='*80}")
        print("FINAL EVALUATION REPORT")
        print(f"{'='*80}\n")
        print(result)
        
        # Optionally save results
        output_dir = Path("scout_reports")
        output_dir.mkdir(exist_ok=True)
        
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in founder_info)
        safe_filename = safe_filename.replace(' ', '_').lower()[:50]
        
        output_file = output_dir / f"{safe_filename}_report.txt"
        output_file.write_text(str(result))
        
        print(f"\n{'='*80}")
        print(f"Report saved to: {output_file}")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\nERROR during scouting: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def scout_multiple():
    """Scout multiple founders from a list."""
    load_dotenv()
    
    print("VC Scout Agent - Batch Processing Mode")
    print("=" * 60)
    print("Enter founder names (one per line, format: 'Name, Company')")
    print("Enter a blank line when done:\n")
    
    founders_list = []
    while True:
        founder = input("> ").strip()
        if not founder:
            break
        founders_list.append(founder)
    
    if not founders_list:
        print("No founders provided. Exiting.")
        return
    
    print(f"\nScouting {len(founders_list)} founders...\n")
    
    scout_crew = FounderScoutCrew()
    results = scout_crew.scout_multiple_founders(founders_list)
    
    # Save all results
    output_dir = Path("scout_reports")
    output_dir.mkdir(exist_ok=True)
    
    summary_file = output_dir / "batch_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("BATCH FOUNDER SCOUTING RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        for founder_info, result in results.items():
            f.write(f"\n{'='*80}\n")
            f.write(f"FOUNDER: {founder_info}\n")
            f.write(f"{'='*80}\n\n")
            f.write(str(result))
            f.write("\n\n")
    
    print(f"\nAll reports saved to: {summary_file}")


if __name__ == "__main__":
    main()
