#!/usr/bin/env python3

import pyautogui
import time
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init()

def get_user_inputs():
    print(Fore.CYAN + "\n--- Message Configuration ---" + Style.RESET_ALL)
    message = input(Fore.GREEN + "Enter the message to send: " + Style.RESET_ALL)
    
    while True:
        times_input = input(Fore.GREEN + "How many times to send the message (or type 'infinity' for endless): " + Style.RESET_ALL).strip()
        if times_input.lower() == "infinity":
            times = float("inf")  # Use infinity as the signal for an endless loop
            break
        else:
            try:
                times = int(times_input)
                break  # Exit loop if input is valid
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number or type 'infinity'." + Style.RESET_ALL)
    
    while True:
        try:
            delay = float(input(Fore.GREEN + "Enter delay between each message (in seconds): " + Style.RESET_ALL))
            break  # Exit loop if input is valid
        except ValueError:
            print(Fore.RED + "Invalid input for 'delay'. Please enter a valid number." + Style.RESET_ALL)
    
    return message, times, delay

def send_texts(message, times, delay, mode):
    print(Fore.YELLOW + "\nStarting in 3 seconds. Switch to the target window..." + Style.RESET_ALL)
    time.sleep(3)  # Give user time to switch to the target application
    
    count = 0  # Keep track of the number of messages sent
    while count < times:
        if mode == "bot":
            pyautogui.typewrite(message)  # No delay (like a bot)
        elif mode == "human":
            pyautogui.typewrite(message, interval=0.1)  # Add delay for human-like typing
        pyautogui.press("enter")
        time.sleep(delay)
        count += 1
        # Stop if not in infinite mode
        if times == float("inf"):
            count = 0  # Reset count to loop infinitely

    print(Fore.YELLOW + "\nCompleted sending messages." + Style.RESET_ALL)

def main():
    message, times, delay = get_user_inputs()

    # Typing Mode Selection
    while True:
        print(Fore.CYAN + "\n--- Typing Mode Selection ---" + Style.RESET_ALL)
        print(Fore.BLUE + "Press '1' for bot (fast typing)")
        print("Press '2' for human (slow typing)" + Style.RESET_ALL)
        typing_choice = input(Fore.GREEN + "Choose typing mode: " + Style.RESET_ALL).strip()
        
        if typing_choice == "1":
            typing_mode = "bot"
            break
        elif typing_choice == "2":
            typing_mode = "human"
            break
        else:
            print(Fore.RED + "Invalid choice. Please select '1' or '2'." + Style.RESET_ALL)

    # Main Options Loop
    while True:
        print(Fore.CYAN + "\n--- Main Options ---" + Style.RESET_ALL)
        print(Fore.BLUE + "Press '1' to run the message sender")
        print("Press '2' to edit the message configuration")
        print("Press '3' to exit the program" + Style.RESET_ALL)
        command = input(Fore.GREEN + "Choose an option: " + Style.RESET_ALL).strip()

        if command == "1":  # Run
            send_texts(message, times, delay, typing_mode)
            print(Fore.YELLOW + "\nMessages sent. Exiting." + Style.RESET_ALL)
            break
        elif command == "2":  # Edit
            message, times, delay = get_user_inputs()
            while True:
                print(Fore.CYAN + "\n--- Typing Mode Selection ---" + Style.RESET_ALL)
                print(Fore.BLUE + "Press '1' for bot (fast typing)")
                print("Press '2' for human (slow typing)" + Style.RESET_ALL)
                typing_choice = input(Fore.GREEN + "Choose typing mode: " + Style.RESET_ALL).strip()
                
                if typing_choice == "1":
                    typing_mode = "bot"
                    break
                elif typing_choice == "2":
                    typing_mode = "human"
                    break
                else:
                    print(Fore.RED + "Invalid choice. Please select '1' or '2'." + Style.RESET_ALL)
        elif command == "3":  # Exit
            print(Fore.YELLOW + "\nExiting the program." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Unknown command. Please press '1', '2', or '3'." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
