#!/usr/bin/env python3
"""
Script to create and initialize the database instance
"""
import sys
import argparse
from pathlib import Path
from database import DatabaseManager
from config import settings


def create_database(db_path: str = None, force: bool = False) -> bool:
    """
    Create and initialize database instance
    
    Args:
        db_path: Path to database file. Defaults to settings.DATABASE_PATH
        force: If True, overwrite existing database
        
    Returns:
        True if successful, False otherwise
    """
    db_path = db_path or settings.DATABASE_PATH
    db_file = Path(db_path)
    
    # Check if database already exists
    if db_file.exists() and not force:
        print(f"❌ Database already exists at: {db_path}")
        print("   Use --force to overwrite existing database")
        return False
    
    # Remove existing database if force is True
    if db_file.exists() and force:
        print(f"⚠️  Removing existing database at: {db_path}")
        db_file.unlink()
        # Also remove journal file if exists
        journal_file = Path(f"{db_path}-journal")
        if journal_file.exists():
            journal_file.unlink()
    
    try:
        print(f"📦 Creating database at: {db_path}")
        
        # Create database manager (this will initialize schema)
        db_manager = DatabaseManager(db_path)
        
        print("✅ Database created successfully!")
        print(f"   Location: {db_path}")
        print(f"   Tables: sessions, messages")
        print(f"   Indexes: Created for optimal performance")
        
        # Verify database was created
        if db_file.exists():
            file_size = db_file.stat().st_size
            print(f"   File size: {file_size} bytes")
            
            # Test connection
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            print(f"   Tables created: {', '.join(tables)}")
            return True
        else:
            print("❌ Database file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error creating database: {str(e)}")
        return False


def verify_database(db_path: str = None) -> bool:
    """
    Verify database instance exists and is valid
    
    Args:
        db_path: Path to database file. Defaults to settings.DATABASE_PATH
        
    Returns:
        True if database is valid, False otherwise
    """
    db_path = db_path or settings.DATABASE_PATH
    db_file = Path(db_path)
    
    if not db_file.exists():
        print(f"❌ Database not found at: {db_path}")
        return False
    
    try:
        db_manager = DatabaseManager(db_path)
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = {'sessions', 'messages'}
        if not expected_tables.issubset(set(tables)):
            missing = expected_tables - set(tables)
            print(f"❌ Database is missing tables: {', '.join(missing)}")
            conn.close()
            return False
        
        # Check indexes exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        # Get table info
        cursor.execute("SELECT COUNT(*) FROM sessions")
        session_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        message_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database is valid")
        print(f"   Location: {db_path}")
        print(f"   Tables: {', '.join(tables)}")
        print(f"   Indexes: {len(indexes)} indexes created")
        print(f"   Sessions: {session_count}")
        print(f"   Messages: {message_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {str(e)}")
        return False


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Create and initialize the bot chat database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create database with default path
  python create_db.py

  # Create database at custom path
  python create_db.py --path data/custom.db

  # Overwrite existing database
  python create_db.py --force

  # Verify existing database
  python create_db.py --verify
        """
    )
    
    parser.add_argument(
        '--path',
        type=str,
        default=None,
        help=f'Path to database file (default: {settings.DATABASE_PATH})'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing database if it exists'
    )
    
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify existing database instead of creating new one'
    )
    
    args = parser.parse_args()
    
    if args.verify:
        success = verify_database(args.path)
        sys.exit(0 if success else 1)
    else:
        success = create_database(args.path, args.force)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

