#!/usr/bin/env python3
"""
File Cleanup Utility for DevOps Project.
Finds and removes files older than specified days.
"""

import os
import argparse
import time
from datetime import datetime, timedelta
import logging

def find_old_files(directory, extension, days_old):
    """
    Find files with specific extension older than specified days.
    
    Args:
        directory (str): Path to search in
        extension (str): File extension to look for (e.g., '.log', '.tmp')
        days_old (int): Minimum age of files to delete (in days)
    
    Returns:
        list: Paths to files matching criteria
    """
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)
    old_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extension and not file.endswith(extension):
                continue
                
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    old_files.append(file_path)
    
    return old_files

def delete_files(file_list, dry_run=True):
    """
    Delete files from list with optional dry-run mode.
    
    Args:
        file_list (list): List of file paths to delete
        dry_run (bool): If True, only show what would be deleted
    
    Returns:
        tuple: (deleted_count, failed_count)
    """
    deleted_count = 0
    failed_count = 0
    
    for file_path in file_list:
        try:
            if dry_run:
                print(f"[DRY RUN] Would delete: {file_path}")
            else:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_count += 1
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
            failed_count += 1
    
    return deleted_count, failed_count

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Clean up old files')
    parser.add_argument('directory', help='Directory to search in')
    parser.add_argument('--extension', default='.log', 
                       help='File extension to look for (default: .log)')
    parser.add_argument('--days', type=int, default=7,
                       help='Delete files older than N days (default: 7)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deleted without actually deleting')
    
    args = parser.parse_args()
    
    # Validate directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        return
    
    print(f"Searching for {args.extension} files older than {args.days} days in {args.directory}")
    
    # Find old files
    old_files = find_old_files(args.directory, args.extension, args.days)
    
    if not old_files:
        print("No matching files found.")
        return
    
    print(f"Found {len(old_files)} file(s) matching criteria:")
    for file_path in old_files[:5]:  # Show first 5
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"  - {file_path} (modified: {mtime})")
    if len(old_files) > 5:
        print(f"  ... and {len(old_files) - 5} more")
    
    # Ask for confirmation (unless dry-run)
    if not args.dry_run and old_files:
        response = input(f"\nDelete {len(old_files)} file(s)? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    # Delete files
    deleted, failed = delete_files(old_files, dry_run=args.dry_run)
    
    if args.dry_run:
        print(f"\n[DRY RUN] Would delete {deleted} file(s)")
    else:
        print(f"\nDeleted {deleted} file(s), failed to delete {failed} file(s)")

if __name__ == "__main__":
    main()
