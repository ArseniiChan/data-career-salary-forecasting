"""
Quick Preprocessing Script
Run this after downloading the dataset to `data/raw/ai_ml_salaries.csv`

Author: Data Preprocessing Lead
"""

import sys
import os

# Add src folder to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from preprocessing_utils import full_preprocessing_pipeline

def main():
    print("🔧 AI/ML Salary Data Preprocessing")
    print("=" * 60)
    
    # Configuration
    INPUT_FILE = 'data/raw/ai_ml_salaries.csv'
    OUTPUT_DIR = 'data/processed'
    MIN_SALARY = 10000  # $10K
    MAX_SALARY = 1000000  # $1M
    
    # Check if file exists first
    if not os.path.exists(INPUT_FILE):
        print(f"\n❌ ERROR: Could not find input file: {INPUT_FILE}")
        print("\n💡 TIP: Make sure you've:")
        print("   1. Downloaded the dataset from Kaggle")
        print("   2. Saved it to data/raw/ai_ml_salaries.csv")
        print("   3. Created the data/raw/ directory")
        print(f"\n📁 Looking for file at: {os.path.abspath(INPUT_FILE)}")
        return 1
    
    try:
        # Run preprocessing pipeline
        df_clean, summary = full_preprocessing_pipeline(
            file_path=INPUT_FILE,
            output_dir=OUTPUT_DIR,
            min_salary=MIN_SALARY,
            max_salary=MAX_SALARY
        )
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Preprocessing completed.")
        print("=" * 60)
        print(f"\n📁 Output files saved to: {OUTPUT_DIR}/")
        print("\n✅ Ready for next steps:")
        print("   1. Share cleaned data with EDA Lead")
        print("   2. Share average_salary_by_year.csv with Modeling Lead")
        print("   3. Document any findings with Presentation Lead")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n💡 Check the error message above and try again.")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)