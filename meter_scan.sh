#!/bin/bash

# Configuration
ENDPOINT_ID="91234567"  # Replace with your meter's endpoint ID
FREQUENCY_START=902000000  # Start frequency in Hz
FREQUENCY_END=928000000    # End frequency in Hz
FREQUENCY_STEP=500000      # Frequency step in Hz
GAIN_START=0               # Start gain in dB
GAIN_END=49                # End gain in dB
GAIN_STEP=1                # Gain step in dB
DURATION=240                # Duration to listen on each setting in seconds
OUTPUT_DIR="./" # Directory to store logs
FOUND_LOG="./found_log.txt" # Log file for when the endpoint is found
SERVER_IP="172.0.0.1"

# Ensure the output directory exists
#mkdir -p "$OUTPUT_DIR"

# Function to check for the endpoint ID in the rtlamr output
check_and_log() {
    local freq=$1
    local gain=$2
    local output=$3

    # Check if the endpoint ID is in the output
    if grep -q "\"EndpointID\":$ENDPOINT_ID" <<< "$output"; then
        echo "Endpoint ID $ENDPOINT_ID found at frequency $freq Hz and gain $gain dB"
        echo "$(date) - Endpoint ID $ENDPOINT_ID found at frequency $freq Hz and gain $gain dB" >> "$FOUND_LOG"
        echo "$output" >> "$FOUND_LOG"
        exit 0  # Exit if found
    fi
}

# Loop over frequencies and gains
for freq in $(seq $FREQUENCY_START $FREQUENCY_STEP $FREQUENCY_END); do
    for gain in $(seq $GAIN_START $GAIN_STEP $GAIN_END); do
        echo "Scanning at frequency $freq Hz and gain $gain dB"
        # Run rtlamr with the current frequency and gain, capture the output
        output=$(timeout "$DURATION"s rtlamr -server=$SERVER_IP:1234 -format=json -msgtype="scm,scm+" -tunergain="$gain" -tunergainmode=true -centerfreq="$freq")
        # Log the output
        echo "$output" > "./log_${freq}_${gain}.txt"
        echo "Scan complete for frequency $freq Hz and gain $gain dB"
        echo "Results stored in log_${freq}_${gain}.txt"
        # Check if the endpoint ID was found
        check_and_log "$freq" "$gain" "$output"
        # Wait for 5 seconds before the next attempt
        sleep $((10 + gain))
    done
done

echo "All scans completed. Check the directory for logs."
