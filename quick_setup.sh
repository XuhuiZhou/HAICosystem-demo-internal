#!/bin/bash

# Variables
APP_FILE="app.py"
LOG_FILE="streamlit.log"

# Kill any previously running Streamlit app using nohup
pkill -f "streamlit run $APP_FILE"

nohup streamlit run $APP_FILE 1> $LOG_FILE 2>error.log &
disown

# Wait a moment to ensure the log file is created and the app starts
sleep 2

# Output the log file
tail -f $LOG_FILE

