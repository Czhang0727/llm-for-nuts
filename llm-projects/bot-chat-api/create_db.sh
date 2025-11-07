#!/bin/bash

# Script to create and initialize the database instance
# Usage: ./create_db.sh [--path PATH] [--force] [--verify]

set -e  # Exit on error

# Default values
DB_PATH=""
FORCE=false
VERIFY=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            DB_PATH="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --verify)
            VERIFY=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Create and initialize the bot chat database"
            echo ""
            echo "Options:"
            echo "  --path PATH    Path to database file (default: data/chat.db)"
            echo "  --force        Overwrite existing database if it exists"
            echo "  --verify       Verify existing database instead of creating new one"
            echo "  -h, --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  # Create database with default path"
            echo "  $0"
            echo ""
            echo "  # Create database at custom path"
            echo "  $0 --path data/custom.db"
            echo ""
            echo "  # Overwrite existing database"
            echo "  $0 --force"
            echo ""
            echo "  # Verify existing database"
            echo "  $0 --verify"
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)

# Build Python command arguments
PYTHON_ARGS=""
if [ -n "$DB_PATH" ]; then
    PYTHON_ARGS="$PYTHON_ARGS --path $DB_PATH"
fi
if [ "$FORCE" = true ]; then
    PYTHON_ARGS="$PYTHON_ARGS --force"
fi
if [ "$VERIFY" = true ]; then
    PYTHON_ARGS="$PYTHON_ARGS --verify"
fi

# Execute the Python script
echo -e "${BLUE}Running database initialization...${NC}"
$PYTHON_CMD create_db.py $PYTHON_ARGS

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Database operation completed successfully${NC}"
else
    echo -e "${RED}✗ Database operation failed${NC}"
    exit $EXIT_CODE
fi

