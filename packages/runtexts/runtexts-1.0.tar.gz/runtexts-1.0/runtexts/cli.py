#!/usr/bin/env python3

# Paste your existing code here
import pyautogui
import time
import sys

def get_user_inputs():
    # Prompt the user for the message to send, how many times, and delay
    message = input("Enter the message to send: ")
    try:
        times = int(input("How many times to send the message: "))
        delay = float(input("Enter delay between each message (in seconds): "))
    except ValueError:
        print("Invalid input. Please enter numeric values for times and delay.")
        sys.exit(1)
    return message, times, delay

def send_texts(message, times, delay):
    print("Starting in 3 seconds. Switch to the target window...")
    time.sleep(3)  # Give user time to switch to the target application
    for _ in range(times):
        pyautogui.typewrite(message)
        pyautogui.press("enter")
        time.sleep(delay)
    print("Completed sending messages.")

def main():
    # Initial prompt for user inputs
    message, times, delay = get_user_inputs()

    while True:
        # Show options after getting initial inputs
        command = input("Type 'run' to start sending messages, 'edit' to change the message, or 'exit' to quit: ").strip().lower()

        if command == "run":
            send_texts(message, times, delay)
            print("Messages sent. Exiting.")
            break
        elif command == "edit":
            # Allow editing of message, times, and delay
            message, times, delay = get_user_inputs()
        elif command == "exit":
            print("Exiting the program.")
            break
        else:
            print("Unknown command. Please type 'run', 'edit', or 'exit'.")

if __name__ == "__main__":
    main()
