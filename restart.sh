#!/bin/bash


run_command() {
    echo "Running..."
    python frontend
    echo "Restarting..."
    run_command
}

run_command
