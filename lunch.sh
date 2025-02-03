#!/bin/bash

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if requirements.txt exists
if [ -f "requirement.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirement.txt
else
    echo "Warning: requirement.txt not found"
fi

# Check if Flask is installed
if ! pip show flask > /dev/null; then
    echo "Installing Flask..."
    pip install flask
fi

# Run Flask application
echo "Starting Flask application..."
export FLASK_APP=app.py
flask run

