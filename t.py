#!/usr/bin/env python3

import os
import subprocess
import sys


# ============================================================
#             OPERATING SYSTEMS LAB
#                 EXPERIMENT NO. 3
#
# Topic:
# a. Commands for Sending Messages to Logged-in Users
#    who, cat, wall, write, mesg
#
# b. List Processes Attached to Shared Memory Segment
#    ipcs
# ============================================================


def run_command(command, input_text=None):
    """
    Execute a Linux command and display its output.
    """

    try:
        result = subprocess.run(
            command,
            input=input_text,
            text=True,
            capture_output=True
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print("Error:", result.stderr)

        return result.returncode

    except FileNotFoundError:
        print("Command not found:", command[0])
        return 1

    except Exception as e:
        print("Error:", e)
        return 1


# ------------------------------------------------------------
# 1. WHO COMMAND
# ------------------------------------------------------------

def show_logged_users():

    print("\n============================================================")
    print("                 WHO COMMAND")
    print("============================================================")

    print("\nPurpose:")
    print("Displays all users currently logged into the Linux system.\n")

    run_command(["who"])


# ------------------------------------------------------------
# 2. TTY COMMAND
# ------------------------------------------------------------

def show_current_terminal():

    print("\n============================================================")
    print("                 CURRENT TERMINAL")
    print("============================================================")

    print("\nYour current terminal is:\n")

    run_command(["tty"])


# ------------------------------------------------------------
# 3. CAT COMMAND
# ------------------------------------------------------------

def send_using_cat():

    print("\n============================================================")
    print("                 CAT COMMAND")
    print("============================================================")

    print("\nThe cat command can write text to a terminal device.")
    print("First, check the logged-in users:\n")

    run_command(["who"])

    print("\nExample terminal:")
    print("/dev/pts/1")

    print("\nEnter the terminal device where you want to send")
    print("the message.")
    print("Example: /dev/pts/1\n")

    terminal = input("Terminal device: ").strip()

    if not terminal:
        print("No terminal entered.")
        return

    # Security check: only allow terminal device paths
    if not terminal.startswith("/dev/pts/"):
        print("Invalid terminal.")
        print("Use a terminal such as /dev/pts/1")
        return

    if not os.path.exists(terminal):
        print("Terminal does not exist:", terminal)
        return

    print("\nEnter your message.")
    print("Press ENTER when finished.\n")

    message = input("Message: ")

    try:
        # Equivalent idea to:
        # echo "message" > /dev/pts/1

        with open(terminal, "w") as terminal_file:
            terminal_file.write(
                "\n\nMessage from Experiment 3:\n"
                + message
                + "\n\n"
            )

        print("\nMessage sent successfully using terminal device.")

    except PermissionError:
        print("\nPermission denied.")
        print("You may not have permission to write to that terminal.")

    except Exception as e:
        print("\nError:", e)


# ------------------------------------------------------------
# 4. WALL COMMAND
# ------------------------------------------------------------

def send_wall_message():

    print("\n============================================================")
    print("                 WALL COMMAND")
    print("============================================================")

    print("\nThe wall command broadcasts a message to")
    print("all logged-in users.\n")

    message = input("Enter message: ")

    if not message:
        print("Message cannot be empty.")
        return

    try:

        result = subprocess.run(
            ["wall"],
            input=message + "\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:
            print("\nBroadcast message sent successfully.")

        else:
            print("\nUnable to send wall message.")

            if result.stderr:
                print(result.stderr)

    except Exception as e:
        print("Error:", e)


# ------------------------------------------------------------
# 5. WRITE COMMAND
# ------------------------------------------------------------

def send_write_message():

    print("\n============================================================")
    print("                 WRITE COMMAND")
    print("============================================================")

    print("\nThe write command sends a message to a particular")
    print("user's terminal.\n")

    print("Currently logged-in users:\n")

    run_command(["who"])

    print("\nExample:")
    print("Username : kali")
    print("Terminal : pts/1")
    print()

    username = input("Enter username: ").strip()
    terminal = input("Enter terminal (example pts/1): ").strip()

    if not username or not terminal:
        print("Username and terminal are required.")
        return

    # Basic validation
    if "/" in username or "/" in terminal:
        print("Invalid username or terminal.")
        return

    print("\nEnter your message.")
    message = input("Message: ")

    if not message:
        print("Message cannot be empty.")
        return

    try:

        result = subprocess.run(
            ["write", username, terminal],
            input=message + "\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:
            print("\nMessage sent successfully using write.")

        else:
            print("\nUnable to send message.")

            if result.stderr:
                print("Reason:", result.stderr)

    except FileNotFoundError:
        print("The write command is not available on this system.")

    except Exception as e:
        print("Error:", e)


# ------------------------------------------------------------
# 6. MESG COMMAND
# ------------------------------------------------------------

def check_mesg():

    print("\n============================================================")
    print("                 MESG COMMAND")
    print("============================================================")

    print("\nmesg controls whether other users can send")
    print("messages to your terminal.\n")

    run_command(["mesg"])


# ------------------------------------------------------------
# 7. ENABLE MESG
# ------------------------------------------------------------

def enable_mesg():

    print("\n============================================================")
    print("              ENABLE MESSAGES")
    print("============================================================")

    result = run_command(["mesg", "y"])

    if result == 0:
        print("Messages have been enabled.")
        print("\nCurrent status:")
        run_command(["mesg"])


# ------------------------------------------------------------
# 8. DISABLE MESG
# ------------------------------------------------------------

def disable_mesg():

    print("\n============================================================")
    print("              DISABLE MESSAGES")
    print("============================================================")

    result = run_command(["mesg", "n"])

    if result == 0:
        print("Messages have been disabled.")
        print("\nCurrent status:")
        run_command(["mesg"])


# ------------------------------------------------------------
# 9. IPCS -M
# ------------------------------------------------------------

def show_shared_memory():

    print("\n============================================================")
    print("                 IPCS -M")
    print("============================================================")

    print("\nipcs -m displays shared memory segments.\n")

    run_command(["ipcs", "-m"])


# ------------------------------------------------------------
# 10. IPCS -M -P
# ------------------------------------------------------------

def show_shared_memory_processes():

    print("\n============================================================")
    print("              IPCS -M -P")
    print("============================================================")

    print("\nThis command displays process IDs associated")
    print("with shared memory segments.\n")

    run_command(["ipcs", "-m", "-p"])


# ------------------------------------------------------------
# 11. IPCS -M -T
# ------------------------------------------------------------

def show_shared_memory_time():

    print("\n============================================================")
    print("              IPCS -M -T")
    print("============================================================")

    print("\nThis command displays time information about")
    print("shared memory segments.\n")

    run_command(["ipcs", "-m", "-t"])


# ------------------------------------------------------------
# 12. COMPLETE IPC INFORMATION
# ------------------------------------------------------------

def show_all_ipc():

    print("\n============================================================")
    print("                   IPCS")
    print("============================================================")

    print("\nipcs displays information about IPC resources.")
    print("These include:")
    print("1. Message queues")
    print("2. Shared memory")
    print("3. Semaphores\n")

    run_command(["ipcs"])


# ------------------------------------------------------------
# 13. COMPLETE EXPERIMENT
# ------------------------------------------------------------

def complete_experiment():

    print("\n")
    print("============================================================")
    print("             COMPLETE EXPERIMENT NO. 3")
    print("============================================================")

    print("\n\nPART A")
    print("============================================================")
    print("COMMANDS FOR SENDING MESSAGES TO LOGGED-IN USERS")
    print("============================================================")

    # WHO
    print("\n1. WHO COMMAND")
    print("------------------------------------------------------------")
    show_logged_users()

    # TTY
    print("\n2. CURRENT TERMINAL")
    print("------------------------------------------------------------")
    show_current_terminal()

    # MESG
    print("\n3. MESG COMMAND")
    print("------------------------------------------------------------")
    check_mesg()

    # WALL
    print("\n4. WALL COMMAND")
    print("------------------------------------------------------------")
    print("A demonstration message will be sent to logged-in users.")

    try:
        result = subprocess.run(
            ["wall"],
            input="Experiment No. 3: Test message from Python program.\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:
            print("Wall message sent successfully.")
        else:
            print("Wall message could not be sent.")

    except Exception as e:
        print("Error:", e)

    # Shared Memory
    print("\n\nPART B")
    print("============================================================")
    print("SHARED MEMORY")
    print("============================================================")

    # IPCS -M
    print("\n5. IPCS -M")
    print("------------------------------------------------------------")
    run_command(["ipcs", "-m"])

    # IPCS -M -P
    print("\n6. IPCS -M -P")
    print("------------------------------------------------------------")
    run_command(["ipcs", "-m", "-p"])

    # IPCS -M -T
    print("\n7. IPCS -M -T")
    print("------------------------------------------------------------")
    run_command(["ipcs", "-m", "-t"])

    print("\n============================================================")
    print("          EXPERIMENT NO. 3 COMPLETED")
    print("============================================================")


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

def main():

    while True:

        print("\n")
        print("============================================================")
        print("                 OPERATING SYSTEMS LAB")
        print("                 EXPERIMENT NO. 3")
        print("============================================================")

        print("\nCommands for Sending Messages:")
        print("1.  who       - Show logged-in users")
        print("2.  tty       - Show current terminal")
        print("3.  cat       - Send message using terminal device")
        print("4.  wall      - Send message to all users")
        print("5.  write     - Send message to specific user")
        print("6.  mesg      - Check message permission")
        print("7.  mesg y    - Enable messages")
        print("8.  mesg n    - Disable messages")

        print("\nShared Memory:")
        print("9.  ipcs -m   - Show shared memory")
        print("10. ipcs -m -p - Show related process IDs")
        print("11. ipcs -m -t - Show time information")
        print("12. ipcs      - Show all IPC information")

        print("\n13. Run Complete Experiment")
        print("0.  Exit")

        print("============================================================")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            show_logged_users()

        elif choice == "2":
            show_current_terminal()

        elif choice == "3":
            send_using_cat()

        elif choice == "4":
            send_wall_message()

        elif choice == "5":
            send_write_message()

        elif choice == "6":
            check_mesg()

        elif choice == "7":
            enable_mesg()

        elif choice == "8":
            disable_mesg()

        elif choice == "9":
            show_shared_memory()

        elif choice == "10":
            show_shared_memory_processes()

        elif choice == "11":
            show_shared_memory_time()

        elif choice == "12":
            show_all_ipc()

        elif choice == "13":
            complete_experiment()

        elif choice == "0":
            print("\nProgram terminated.")
            print("Thank you!")
            sys.exit(0)

        else:
            print("\nInvalid choice!")
            print("Please select a number from 0 to 13.")


# ------------------------------------------------------------
# PROGRAM START
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
