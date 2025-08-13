#!/usr/bin/env python3
"""
ETL Runner for Joy of Painting API
Extracts, transforms, and loads Bob Ross episode data into MongoDB
"""

import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.etl.load import main as run_etl

if __name__ == "__main__":
    print("🎨 Joy of Painting ETL Process")
    print("=" * 50)
    print("This will extract Bob Ross episode data from CSV files,")
    print("transform it for consistency, and load it into MongoDB.")
    print("")
    
    from config import Config
    
    files_to_check = [
        Config.EPISODE_DATES_FILE,
        Config.COLORS_USED_FILE,
        Config.SUBJECT_MATTER_FILE
    ]
    
    missing_files = []
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            missing_files.append(os.path.basename(file_path))
    
    if missing_files:
        print("❌ Missing required data files:")
        for file_name in missing_files:
            print(f"   - {file_name}")
        print("")
        print("Please ensure all data files are in the data/raw/ directory.")
        sys.exit(1)
    
    print("✅ All required data files found")
    print("")
    
    run_etl()
