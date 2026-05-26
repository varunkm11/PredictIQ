#!/usr/bin/env python3
"""
Local verification script for Streamlit Cloud deployment.
Run this before pushing to verify everything is configured correctly.

Usage:
    python verify_deployment.py
"""

import os
import sys
import importlib.util

def check_file_exists(path, description):
    """Check if a file exists."""
    if os.path.exists(path):
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} (NOT FOUND)")
        return False

def check_package_exists(package_name):
    """Check if a package can be imported."""
    try:
        __import__(package_name)
        print(f"✅ Package installed: {package_name}")
        return True
    except ImportError:
        print(f"❌ Package missing: {package_name}")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 PredictIQ Streamlit Cloud Deployment Verification")
    print("="*60 + "\n")
    
    all_checks = []
    
    # Check 1: Required files exist
    print("📁 Checking Required Files...")
    all_checks.append(check_file_exists("app.py", "Root entry point"))
    all_checks.append(check_file_exists("requirements.txt", "Requirements file"))
    all_checks.append(check_file_exists("model/__init__.py", "Model package marker"))
    all_checks.append(check_file_exists("model/auto_trainer.py", "Model trainer module"))
    all_checks.append(check_file_exists("api/__init__.py", "API package marker"))
    all_checks.append(check_file_exists(".streamlit/config.toml", "Streamlit config"))
    all_checks.append(check_file_exists(".gitignore", "Git ignore file"))
    
    print()
    
    # Check 2: Critical packages
    print("📦 Checking Critical Packages...")
    critical_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "sklearn",
        "xgboost",
        "joblib"
    ]
    for pkg in critical_packages:
        all_checks.append(check_package_exists(pkg))
    
    print()
    
    # Check 3: Import model module
    print("🔗 Checking Model Module Import...")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from model.auto_trainer import (
            train_on_dataset,
            load_metadata,
            predict_single,
            detect_column_types
        )
        print("✅ Model module imported successfully")
        print("   - train_on_dataset: ✅")
        print("   - load_metadata: ✅")
        print("   - predict_single: ✅")
        print("   - detect_column_types: ✅")
        all_checks.append(True)
    except ImportError as e:
        print(f"❌ Failed to import model module: {e}")
        all_checks.append(False)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        all_checks.append(False)
    
    print()
    
    # Check 4: Model files
    print("🤖 Checking Model Files...")
    model_files = [
        ("model/churn_model.pkl", "Trained model"),
        ("model/model_metadata.json", "Model metadata"),
        ("model/train_data.csv", "Training data"),
    ]
    for file_path, description in model_files:
        if os.path.exists(file_path):
            size_kb = os.path.getsize(file_path) / 1024
            print(f"✅ {description}: {file_path} ({size_kb:.1f} KB)")
            all_checks.append(True)
        else:
            print(f"⚠️  {description}: {file_path} (NOT FOUND - will be created on first model training)")
    
    print()
    
    # Summary
    passed = sum(all_checks)
    total = len(all_checks)
    
    print("="*60)
    if passed == total:
        print(f"✅ All checks passed! ({passed}/{total})")
        print("You're ready to deploy to Streamlit Cloud!")
    else:
        print(f"⚠️  Some checks failed ({passed}/{total})")
        print("Please fix the issues above before deploying.")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
