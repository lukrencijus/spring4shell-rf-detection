#!/usr/bin/env bash
set -e

sudo apt install python3-pandas -y
pip3 install nfstream numpy scikit-learn --break-system-packages

echo "Now you can run the following command from the project root to extract features from the raw data and save them as a .csv file in the root directory:"
echo "python3 scripts/extract_features.py"

