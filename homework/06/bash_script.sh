#!/bin/bash

# Default values
DEFAULT_YEAR="2023"
DEFAULT_MONTH="03"

# Check if arguments are provided
if [ $# -eq 0 ]; then
    # No arguments provided, use default values
    YEAR=$DEFAULT_YEAR
    MONTH=$DEFAULT_MONTH
    echo "No arguments provided. Using default values: Year=$YEAR, Month=$MONTH"
else
    # Arguments provided, use them
    YEAR=$1
    MONTH=$2
    echo "Arguments provided. Using values: Year=$YEAR, Month=$MONTH"
fi

# Define the paths to the Python scripts
PYTHON_SCRIPT1="tests/integration_test.py"
PYTHON_SCRIPT2="tests/test_batch.py"

# Execute the Python scripts with the year and month
echo "Running Python Script 1 in $(dirname $PYTHON_SCRIPT1)"
python $PYTHON_SCRIPT1 $YEAR $MONTH

echo "Running Python Script 2 in $(dirname $PYTHON_SCRIPT2)"
python $PYTHON_SCRIPT2 $YEAR $MONTH

echo "Both scripts have been executed."