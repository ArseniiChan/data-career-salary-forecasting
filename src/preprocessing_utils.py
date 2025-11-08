"""
Data Preprocessing Utilities for AI/ML Salary Analysis

This module contains reusable functions for cleaning and preprocessing
the AI/ML/Data Science salary dataset.

Author: Data Preprocessing Lead
Date: November 2025
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


def load_salary_data(file_path: str) -> pd.DataFrame:
    """
    Load the salary dataset from CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Dataset loaded successfully!")
        print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    except Exception as e:
        raise Exception(f"❌ Error loading file: {str(e)}")


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Summary of missing values
    """
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2)
    })
    missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values(
        'Missing_Count', ascending=False
    )
    
    if len(missing_data) == 0:
        print("✅ No missing values found!")
    else:
        print("⚠️ Missing values detected:")
        print(missing_data)
    
    return missing_data


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with duplicates removed
    """
    before = len(df)
    df_clean = df.drop_duplicates()
    after = len(df_clean)
    removed = before - after
    
    print(f"✅ Removed {removed:,} duplicate rows ({removed/before*100:.2f}%)")
    return df_clean


def filter_by_years(df: pd.DataFrame, 
                    start_year: int = 2020, 
                    end_year: int = 2025) -> pd.DataFrame:
    """
    Filter dataset to include only specified years.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    start_year : int
        Starting year (inclusive)
    end_year : int
        Ending year (inclusive)
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    if 'work_year' not in df.columns:
        raise ValueError("Column 'work_year' not found in dataset")
    
    before = len(df)
    df_filtered = df[df['work_year'].between(start_year, end_year)]
    after = len(df_filtered)
    
    print(f"✅ Filtered to {start_year}-{end_year}: {after:,} rows ({before - after:,} removed)")
    print(f"   Year distribution:")
    print(df_filtered['work_year'].value_counts().sort_index())
    
    return df_filtered


def filter_ai_ml_roles(df: pd.DataFrame, 
                       custom_keywords: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Filter dataset to include only AI/ML/Data Science related roles.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    custom_keywords : List[str], optional
        Custom keywords to filter job titles
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataframe
    """
    if 'job_title' not in df.columns:
        raise ValueError("Column 'job_title' not found in dataset")
    
    # Default keywords
    default_keywords = [
        'data scientist', 'data science', 'machine learning', 'ml engineer',
        'ai engineer', 'artificial intelligence', 'data engineer',
        'analytics engineer', 'data analyst', 'research scientist',
        'deep learning', 'nlp engineer', 'computer vision', 'mlops',
        'data architect', 'big data', 'business intelligence'
    ]
    
    keywords = custom_keywords if custom_keywords else default_keywords
    
    before = len(df)
    pattern = '|'.join(keywords)
    mask = df['job_title'].str.lower().str.contains(pattern, na=False)
    df_filtered = df[mask]
    after = len(df_filtered)
    
    print(f"✅ Filtered to AI/ML/Data Science roles: {after:,} rows ({before - after:,} removed)")
    print(f"\nTop 10 job titles:")
    print(df_filtered['job_title'].value_counts().head(10))
    
    return df_filtered


def remove_salary_outliers(df: pd.DataFrame, 
                          min_salary: float = 10000,
                          max_salary: float = 1000000) -> pd.DataFrame:
    """
    Remove unrealistic salary values.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    min_salary : float
        Minimum acceptable salary
    max_salary : float
        Maximum acceptable salary
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with outliers removed
    """
    if 'salary_in_usd' not in df.columns:
        raise ValueError("Column 'salary_in_usd' not found in dataset")
    
    before = len(df)
    df_clean = df[
        (df['salary_in_usd'] >= min_salary) & 
        (df['salary_in_usd'] <= max_salary)
    ]
    after = len(df_clean)
    
    print(f"✅ Removed salary outliers: {before - after:,} rows")
    print(f"   Salary range: ${df_clean['salary_in_usd'].min():,.0f} - "
          f"${df_clean['salary_in_usd'].max():,.0f}")
    
    return df_clean


def standardize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize categorical variables with full names.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with standardized categories
    """
    df_standard = df.copy()
    
    # Experience levels
    if 'experience_level' in df.columns:
        exp_mapping = {
            'EN': 'Entry',
            'MI': 'Mid',
            'SE': 'Senior',
            'EX': 'Executive'
        }
        df_standard['experience_level_full'] = df['experience_level'].map(exp_mapping)
        print("✅ Mapped experience levels")
    
    # Employment types
    if 'employment_type' in df.columns:
        emp_mapping = {
            'FT': 'Full-time',
            'PT': 'Part-time',
            'CT': 'Contract',
            'FL': 'Freelance'
        }
        df_standard['employment_type_full'] = df['employment_type'].map(emp_mapping)
        print("✅ Mapped employment types")
    
    # Company sizes
    if 'company_size' in df.columns:
        size_mapping = {
            'S': 'Small',
            'M': 'Medium',
            'L': 'Large'
        }
        df_standard['company_size_full'] = df['company_size'].map(size_mapping)
        print("✅ Mapped company sizes")
    
    return df_standard


def create_remote_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create categorical variable for remote work.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with remote category
    """
    if 'remote_ratio' not in df.columns:
        raise ValueError("Column 'remote_ratio' not found in dataset")
    
    df_enhanced = df.copy()
    
    def categorize_remote(ratio):
        if ratio == 0:
            return 'Onsite'
        elif ratio == 100:
            return 'Remote'
        else:
            return 'Hybrid'
    
    df_enhanced['remote_category'] = df['remote_ratio'].apply(categorize_remote)
    print("✅ Created remote work category")
    print(df_enhanced['remote_category'].value_counts())
    
    return df_enhanced


def create_salary_bands(df: pd.DataFrame,
                       bins: Optional[List[float]] = None,
                       labels: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Create salary band categories.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    bins : List[float], optional
        Custom bin edges
    labels : List[str], optional
        Custom labels for bins
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with salary bands
    """
    if 'salary_in_usd' not in df.columns:
        raise ValueError("Column 'salary_in_usd' not found in dataset")
    
    df_banded = df.copy()
    
    # Default bins and labels
    default_bins = [0, 50000, 100000, 150000, 200000, float('inf')]
    default_labels = ['<$50K', '$50K-$100K', '$100K-$150K', '$150K-$200K', '>$200K']
    
    bins = bins if bins else default_bins
    labels = labels if labels else default_labels
    
    df_banded['salary_band'] = pd.cut(
        df['salary_in_usd'],
        bins=bins,
        labels=labels
    )
    
    print("✅ Created salary bands")
    print(df_banded['salary_band'].value_counts().sort_index())
    
    return df_banded


def aggregate_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average salary statistics by year.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Aggregated data by year
    """
    if 'work_year' not in df.columns or 'salary_in_usd' not in df.columns:
        raise ValueError("Required columns not found in dataset")
    
    agg_data = df.groupby('work_year').agg({
        'salary_in_usd': ['mean', 'median', 'count', 'std', 'min', 'max']
    }).round(2)
    
    agg_data.columns = ['avg_salary', 'median_salary', 'count', 
                        'std_salary', 'min_salary', 'max_salary']
    agg_data = agg_data.reset_index()
    
    return agg_data


def aggregate_by_experience(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average salary by year and experience level.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Aggregated data by year and experience
    """
    required_cols = ['work_year', 'experience_level_full', 'salary_in_usd']
    if not all(col in df.columns for col in required_cols):
        raise ValueError("Required columns not found in dataset")
    
    agg_data = df.groupby(['work_year', 'experience_level_full']).agg({
        'salary_in_usd': ['mean', 'median', 'count']
    }).round(2)
    
    agg_data.columns = ['avg_salary', 'median_salary', 'count']
    agg_data = agg_data.reset_index()
    
    return agg_data


def aggregate_by_company_size(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average salary by year and company size.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Aggregated data by year and company size
    """
    required_cols = ['work_year', 'company_size_full', 'salary_in_usd']
    if not all(col in df.columns for col in required_cols):
        raise ValueError("Required columns not found in dataset")
    
    agg_data = df.groupby(['work_year', 'company_size_full']).agg({
        'salary_in_usd': ['mean', 'median', 'count']
    }).round(2)
    
    agg_data.columns = ['avg_salary', 'median_salary', 'count']
    agg_data = agg_data.reset_index()
    
    return agg_data


def get_preprocessing_summary(df_original: pd.DataFrame, 
                             df_clean: pd.DataFrame) -> Dict:
    """
    Generate a summary of preprocessing steps.
    
    Parameters:
    -----------
    df_original : pd.DataFrame
        Original dataset
    df_clean : pd.DataFrame
        Cleaned dataset
        
    Returns:
    --------
    Dict
        Summary statistics
    """
    summary = {
        'original_rows': len(df_original),
        'final_rows': len(df_clean),
        'rows_removed': len(df_original) - len(df_clean),
        'removal_percentage': ((len(df_original) - len(df_clean)) / len(df_original) * 100),
        'final_columns': len(df_clean.columns),
        'salary_mean': df_clean['salary_in_usd'].mean(),
        'salary_median': df_clean['salary_in_usd'].median(),
        'salary_min': df_clean['salary_in_usd'].min(),
        'salary_max': df_clean['salary_in_usd'].max(),
        'salary_std': df_clean['salary_in_usd'].std(),
        'years_covered': f"{df_clean['work_year'].min()}-{df_clean['work_year'].max()}",
        'num_years': df_clean['work_year'].nunique()
    }
    
    return summary


def print_preprocessing_summary(summary: Dict) -> None:
    """
    Print a formatted preprocessing summary.
    
    Parameters:
    -----------
    summary : Dict
        Summary statistics from get_preprocessing_summary()
    """
    print("=" * 60)
    print("DATA PREPROCESSING SUMMARY")
    print("=" * 60)
    print(f"\n📊 Dataset Overview:")
    print(f"   Original rows: {summary['original_rows']:,}")
    print(f"   Final rows: {summary['final_rows']:,}")
    print(f"   Rows removed: {summary['rows_removed']:,} ({summary['removal_percentage']:.2f}%)")
    print(f"   Final columns: {summary['final_columns']}")
    
    print(f"\n💰 Salary Statistics (USD):")
    print(f"   Mean: ${summary['salary_mean']:,.2f}")
    print(f"   Median: ${summary['salary_median']:,.2f}")
    print(f"   Min: ${summary['salary_min']:,.2f}")
    print(f"   Max: ${summary['salary_max']:,.2f}")
    print(f"   Std Dev: ${summary['salary_std']:,.2f}")
    
    print(f"\n📅 Time Period:")
    print(f"   Years covered: {summary['years_covered']}")
    print(f"   Total years: {summary['num_years']}")
    
    print("\n" + "=" * 60)
    print("✅ DATA PREPROCESSING COMPLETE")
    print("=" * 60)


def full_preprocessing_pipeline(file_path: str,
                                output_dir: str = 'data/processed',
                                min_salary: float = 10000,
                                max_salary: float = 1000000) -> Tuple[pd.DataFrame, Dict]:
    """
    Execute the complete preprocessing pipeline.
    
    Parameters:
    -----------
    file_path : str
        Path to raw data file
    output_dir : str
        Directory to save processed files
    min_salary : float
        Minimum acceptable salary
    max_salary : float
        Maximum acceptable salary
        
    Returns:
    --------
    Tuple[pd.DataFrame, Dict]
        Cleaned dataframe and summary statistics
    """
    import os
    
    print("🚀 Starting preprocessing pipeline...\n")
    
    # Load data
    df = load_salary_data(file_path)
    df_original = df.copy()
    
    # Check missing values
    print("\n" + "-" * 60)
    check_missing_values(df)
    
    # Clean data
    print("\n" + "-" * 60)
    df = remove_duplicates(df)
    df = filter_by_years(df)
    df = filter_ai_ml_roles(df)
    df = remove_salary_outliers(df, min_salary, max_salary)
    
    # Drop rows with missing critical values
    print("\n" + "-" * 60)
    critical_cols = ['work_year', 'salary_in_usd', 'experience_level', 'employment_type']
    before = len(df)
    df = df.dropna(subset=critical_cols)
    print(f"✅ Removed rows with missing critical values: {before - len(df):,} rows")
    
    # Standardize and engineer features
    print("\n" + "-" * 60)
    df = standardize_categories(df)
    df = create_remote_category(df)
    df = create_salary_bands(df)
    
    # Create aggregations
    print("\n" + "-" * 60)
    print("Creating aggregated datasets...")
    avg_by_year = aggregate_by_year(df)
    avg_by_exp = aggregate_by_experience(df)
    avg_by_size = aggregate_by_company_size(df)
    
    # Save outputs
    print("\n" + "-" * 60)
    os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(f'{output_dir}/salary_data_cleaned.csv', index=False)
    print(f"✅ Saved: {output_dir}/salary_data_cleaned.csv")
    
    avg_by_year.to_csv(f'{output_dir}/average_salary_by_year.csv', index=False)
    print(f"✅ Saved: {output_dir}/average_salary_by_year.csv")
    
    avg_by_exp.to_csv(f'{output_dir}/salary_by_year_experience.csv', index=False)
    print(f"✅ Saved: {output_dir}/salary_by_year_experience.csv")
    
    avg_by_size.to_csv(f'{output_dir}/salary_by_year_company_size.csv', index=False)
    print(f"✅ Saved: {output_dir}/salary_by_year_company_size.csv")
    
    # Generate summary
    print("\n" + "-" * 60)
    summary = get_preprocessing_summary(df_original, df)
    print_preprocessing_summary(summary)
    
    return df, summary


if __name__ == "__main__":
    # Example usage
    print("This module contains preprocessing utilities.")
    print("Import and use the functions in your notebook or script.")
