#!/bin/bash

set -euo pipefail

STREAMLIT_GIT_BRANCH=${STREAMLIT_GIT_BRANCH:-master}
echo "Setting STREAMLIT_GIT_BRANCH to $STREAMLIT_GIT_BRANCH..."

git clone $STREAMLIT_GIT_URL_REPOSITORY --branch $STREAMLIT_GIT_BRANCH --single-branch --depth 1 app

cd app

pip install -r ./requirements.txt

export STREAMLIT_URL_BASE_PATHNAME=${SAAGIE_BASE_PATH}"/"

streamlit run ./app.py
