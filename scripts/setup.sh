#!/bin/bash
# Strava Dashboard Setup Script
# This script sets up the virtual environment and installs all dependencies

echo "=========================================="
echo "Strava Dashboard Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Virtual environment created successfully!"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Configure your Strava API credentials:"
echo "   cp .env.example .env"
echo "   # Then edit .env with your credentials"
echo ""
echo "3. Run authentication:"
echo "   python -m src.auth"
echo ""
echo "4. Fetch your data:"
echo "   python -m src.data_manager"
echo ""
