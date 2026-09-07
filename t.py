#!/usr/bin/env python3

import os
import subprocess
import sys


# ============================================================
#                  OPERATING SYSTEMS LAB
#                     EXPERIMENT NO. 3
#
# PART A:
# Commands for Sending Messages to Logged-in Users
# who, cat, wall, write, mesg
#
# PART B:
# List Processes Attached to a Shared Memory Segment
# ipcs
# ============================================================


# ============================================================
# GENERAL FUNCTION TO RUN LINUX COMMANDS
# ============================================================

def run_command(command, input_data=None):

    try:

        result = subprocess.run(
            command,
            input=input_data,
            text=True,
            capture_output=True
        )

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print("Error:", result.stderr.strip())

        return result.returncode

    except FileNotFoundError:

        print("\nCommand not found:", command[0])
        return 1

    except Exception as error:

        print("\nError:", error)
        return 1


# ============================================================
# PAUSE FUNCTION
# ============================================================

def pause():

    input("\nPress ENTER to continue...")


# ============================================================
# 1. WHO COMMAND
# ============================================================

def who_command():

    print("\n")
    print("=" * 65)
    print("                       WHO COMMAND")
    print("=" * 65)

    print("\nPurpose:")
    print("Displays the users currently logged into the Linux system.")

    print("\nCommand executed:")
    print("who")

    print("\nOutput:")
    print("-" * 65)

    run_command(["who"])

    pause()


# ============================================================
# 2. TTY COMMAND
# ============================================================

def tty_command():

    print("\n")
    print("=" * 65)
    print("                       TTY COMMAND")
    print("=" * 65)

    print("\nPurpose:")
    print("Displays the terminal associated with the current session.")

    print("\nCommand executed:")
    print("tty")

    print("\nOutput:")
    print("-" * 65)

    run_command(["tty"])

    pause()


# ============================================================
# 3. CAT COMMAND
# ============================================================

def cat_command():

    print("\n")
    print("=" * 65)
    print("                       CAT COMMAND")
    print("=" * 65)

    print("\nPurpose:")
    print("The cat command can be used to write data")
    print("to a terminal device.")

    print("\nCurrently logged-in users:")

    print("-" * 65)

    run_command(["who"])

    print("\nExample:")
    print("Terminal: pts/3")
    print("Terminal: pts/21")
    print("Terminal: pts/2")

    print()

    terminal = input(
        "Enter terminal (example pts/3): "
    ).strip()

    # --------------------------------------------------------
    # Check terminal format
    # --------------------------------------------------------

    if not terminal.startswith("pts/"):

        print("\nInvalid terminal format.")
        print("Example: pts/3")

        pause()
        return

    terminal_number = terminal[4:]

    if not terminal_number.isdigit():

        print("\nInvalid terminal.")
        print("Example: pts/3")

        pause()
        return

    device = "/dev/" + terminal

    # --------------------------------------------------------
    # Check whether terminal exists
    # --------------------------------------------------------

    if not os.path.exists(device):

        print("\nTerminal does not exist:")
        print(device)

        print("\nRun 'who' and enter an existing pts terminal.")

        pause()
        return

    # --------------------------------------------------------
    # Enter message
    # --------------------------------------------------------

    print("\nEnter the message:")

    message = input("Message: ").strip()

    if not message:

        print("\nMessage cannot be empty.")

        pause()
        return

    # --------------------------------------------------------
    # Write message to terminal
    # --------------------------------------------------------

    try:

        with open(device, "w") as terminal_file:

            terminal_file.write("\n")
            terminal_file.write(
                "========== MESSAGE FROM EXPERIMENT 3 ==========\n"
            )
            terminal_file.write(message + "\n")
            terminal_file.write(
                "===============================================\n"
            )

        print("\nMessage sent successfully using CAT.")

    except PermissionError:

        print("\nPermission denied.")
        print("You do not have permission to write to this terminal.")

    except Exception as error:

        print("\nError:", error)

    pause()


# ============================================================
# 4. WALL COMMAND
# ============================================================

def wall_command():

    print("\n")
    print("=" * 65)
    print("                       WALL COMMAND")
    print("=" * 65)

    print("\nPurpose:")
    print("Sends a message to all logged-in users.")

    print("\nCommand:")
    print("wall")

    print()

    message = input("Enter message: ").strip()

    if not message:

        print("\nMessage cannot be empty.")

        pause()
        return

    try:

        result = subprocess.run(
            ["wall"],
            input=message + "\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:

            print("\nBroadcast message sent successfully!")

        else:

            print("\nUnable to send wall message.")

            if result.stderr:

                print("Reason:")
                print(result.stderr.strip())

    except FileNotFoundError:

        print("\nwall command is not available.")

    except Exception as error:

        print("\nError:", error)

    pause()


# ============================================================
# 5. WRITE COMMAND
# ============================================================

def write_command():

    print("\n")
    print("=" * 65)
    print("                      WRITE COMMAND")
    print("=" * 65)

    print("\nPurpose:")
    print("Sends a message to a particular user's terminal.")

    print("\nCurrently logged-in users:")
    print("-" * 65)

    # --------------------------------------------------------
    # Get WHO output
    # --------------------------------------------------------

    try:

        who_result = subprocess.run(
            ["who"],
            capture_output=True,
            text=True
        )

        who_output = who_result.stdout

        print(who_output)

    except Exception as error:

        print("\nUnable to execute who command.")
        print(error)

        pause()
        return

    print("\n------------------------------------------------------------")
    print("Enter the EXACT username and terminal shown above.")
    print("Example:")
    print("Username : dce")
    print("Terminal : pts/3")
    print("------------------------------------------------------------")

    # --------------------------------------------------------
    # Enter username
    # --------------------------------------------------------

    username = input("\nEnter username: ").strip()

    if not username:

        print("\nUsername cannot be empty.")

        pause()
        return

    # --------------------------------------------------------
    # Enter terminal
    # --------------------------------------------------------

    terminal = input(
        "Enter terminal (example pts/3): "
    ).strip()

    if not terminal:

        print("\nTerminal cannot be empty.")

        pause()
        return

    # --------------------------------------------------------
    # Validate terminal format
    # --------------------------------------------------------

    if not terminal.startswith("pts/"):

        print("\nInvalid terminal format.")
        print("Correct format:")
        print("pts/3")
        print("pts/21")
        print("pts/2")

        pause()
        return

    terminal_number = terminal[4:]

    if not terminal_number.isdigit():

        print("\nInvalid terminal.")
        print("Example: pts/3")

        pause()
        return

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Your Kali 'who' output looks like:
    #
    # dce sshd pts/3 2026-09-07 15:09 (...)
    #
    # Therefore:
    #
    # parts[0] = username
    # parts[1] = sshd
    # parts[2] = terminal
    #
    # --------------------------------------------------------

    logged_in = False

    for line in who_output.splitlines():

        parts = line.split()

        if len(parts) >= 3:

            current_username = parts[0]
            current_terminal = parts[2]

            if (
                current_username == username
                and current_terminal == terminal
            ):

                logged_in = True
                break

    # --------------------------------------------------------
    # User/terminal not found
    # --------------------------------------------------------

    if not logged_in:

        print("\n============================================================")
        print("              USER / TERMINAL NOT FOUND")
        print("============================================================")

        print("\nYou entered:")

        print("Username :", username)
        print("Terminal :", terminal)

        print("\nPlease enter the EXACT username and terminal")
        print("shown in the 'who' output.")

        print("\nFor example, if you see:")

        print("dce  sshd  pts/3")

        print("enter:")

        print("Username : dce")
        print("Terminal : pts/3")

        pause()
        return

    # --------------------------------------------------------
    # User found
    # --------------------------------------------------------

    print("\n============================================================")
    print("                USER / TERMINAL FOUND")
    print("============================================================")

    print("\nUsername :", username)
    print("Terminal :", terminal)

    # --------------------------------------------------------
    # Check whether messaging is allowed
    # --------------------------------------------------------

    print("\nEnter your message:")

    message = input("Message: ").strip()

    if not message:

        print("\nMessage cannot be empty.")

        pause()
        return

    # --------------------------------------------------------
    # Execute WRITE command
    # --------------------------------------------------------

    print("\nSending message...")
    print("-" * 65)

    try:

        result = subprocess.run(
            ["write", username, terminal],
            input=message + "\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:

            print("\nMessage sent successfully!")

            print("\nMessage details:")
            print("--------------------------------")
            print("Username :", username)
            print("Terminal :", terminal)
            print("Message  :", message)
            print("--------------------------------")

        else:

            print("\nUnable to send the message.")

            if result.stderr:

                print("\nReason:")
                print(result.stderr.strip())

            print("\nPossible reasons:")
            print("1. The target terminal does not allow messages.")
            print("2. You do not have permission.")
            print("3. The target session has ended.")

    except FileNotFoundError:

        print("\nThe 'write' command is not installed.")

    except Exception as error:

        print("\nError:", error)

    pause()


# ============================================================
# 6. MESG COMMAND
# ============================================================

def mesg_command():

    print("\n")
    print("=" * 65)
    print("                       MESG COMMAND")
    print("=" * 65)

    print("\nPurpose:")
    print("Checks whether messages are allowed on your terminal.")

    print("\nCommand:")
    print("mesg")

    print("\nOutput:")
    print("-" * 65)

    run_command(["mesg"])

    pause()


# ============================================================
# 7. ENABLE MESSAGES
# ============================================================

def enable_messages():

    print("\n")
    print("=" * 65)
    print("                    ENABLE MESSAGES")
    print("=" * 65)

    print("\nCommand:")
    print("mesg y")

    result = run_command(["mesg", "y"])

    if result == 0:

        print("\nMessages have been ENABLED.")

        print("\nCurrent status:")

        run_command(["mesg"])

    pause()


# ============================================================
# 8. DISABLE MESSAGES
# ============================================================

def disable_messages():

    print("\n")
    print("=" * 65)
    print("                    DISABLE MESSAGES")
    print("=" * 65)

    print("\nCommand:")
    print("mesg n")

    result = run_command(["mesg", "n"])

    if result == 0:

        print("\nMessages have been DISABLED.")

        print("\nCurrent status:")

        run_command(["mesg"])

    pause()


# ============================================================
# 9. IPCS -M
# ============================================================

def ipcs_shared_memory():

    print("\n")
    print("=" * 65)
    print("                       IPCS -M")
    print("=" * 65)

    print("\nPurpose:")
    print("Displays System V shared memory segments.")

    print("\nCommand:")
    print("ipcs -m")

    print("\nOutput:")
    print("-" * 65)

    run_command(["ipcs", "-m"])

    pause()


# ============================================================
# 10. IPCS -M -P
# ============================================================

def ipcs_processes():

    print("\n")
    print("=" * 65)
    print("                     IPCS -M -P")
    print("=" * 65)

    print("\nPurpose:")
    print("Displays creator PID and last-operation PID")
    print("for shared memory segments.")

    print("\nCommand:")
    print("ipcs -m -p")

    print("\nOutput:")
    print("-" * 65)

    run_command(["ipcs", "-m", "-p"])

    pause()


# ============================================================
# 11. IPCS -M -T
# ============================================================

def ipcs_time():

    print("\n")
    print("=" * 65)
    print("                     IPCS -M -T")
    print("=" * 65)

    print("\nPurpose:")
    print("Displays time information for shared memory segments.")

    print("\nCommand:")
    print("ipcs -m -t")

    print("\nOutput:")
    print("-" * 65)

    run_command(["ipcs", "-m", "-t"])

    pause()


# ============================================================
# 12. COMPLETE IPC INFORMATION
# ============================================================

def complete_ipcs():

    print("\n")
    print("=" * 65)
    print("                         IPCS")
    print("=" * 65)

    print("\nPurpose:")
    print("Displays System V IPC resources.")

    print("\nThis includes:")
    print("1. Message Queues")
    print("2. Shared Memory")
    print("3. Semaphores")

    print("\nCommand:")
    print("ipcs")

    print("\nOutput:")
    print("-" * 65)

    run_command(["ipcs"])

    pause()


# ============================================================
# 13. COMPLETE EXPERIMENT
# ============================================================

def complete_experiment():

    print("\n")
    print("=" * 70)
    print("                 COMPLETE EXPERIMENT NO. 3")
    print("=" * 70)

    # ========================================================
    # PART A
    # ========================================================

    print("\n")
    print("=" * 70)
    print("PART A")
    print("COMMANDS FOR SENDING MESSAGES TO LOGGED-IN USERS")
    print("=" * 70)

    # --------------------------------------------------------
    # WHO
    # --------------------------------------------------------

    print("\n1. WHO COMMAND")
    print("-" * 70)

    print("Displays currently logged-in users.\n")

    run_command(["who"])

    # --------------------------------------------------------
    # TTY
    # --------------------------------------------------------

    print("\n2. TTY COMMAND")
    print("-" * 70)

    print("Displays the current terminal.\n")

    run_command(["tty"])

    # --------------------------------------------------------
    # MESG
    # --------------------------------------------------------

    print("\n3. MESG COMMAND")
    print("-" * 70)

    print("Displays current message permission.\n")

    run_command(["mesg"])

    # --------------------------------------------------------
    # WALL
    # --------------------------------------------------------

    print("\n4. WALL COMMAND")
    print("-" * 70)

    print("Sending a demonstration broadcast message...\n")

    try:

        result = subprocess.run(
            ["wall"],
            input="Experiment No. 3: Hello from the Python program!\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:

            print("Wall message sent successfully.")

        else:

            print("Wall message could not be sent.")

    except Exception as error:

        print("Error:", error)

    # ========================================================
    # PART B
    # ========================================================

    print("\n")
    print("=" * 70)
    print("PART B")
    print("SHARED MEMORY")
    print("=" * 70)

    # --------------------------------------------------------
    # IPCS -M
    # --------------------------------------------------------

    print("\n5. IPCS -M")
    print("-" * 70)

    run_command(["ipcs", "-m"])

    # --------------------------------------------------------
    # IPCS -M -P
    # --------------------------------------------------------

    print("\n6. IPCS -M -P")
    print("-" * 70)

    run_command(["ipcs", "-m", "-p"])

    # --------------------------------------------------------
    # IPCS -M -T
    # --------------------------------------------------------

    print("\n7. IPCS -M -T")
    print("-" * 70)

    run_command(["ipcs", "-m", "-t"])

    # --------------------------------------------------------
    # FINISH
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("              EXPERIMENT NO. 3 COMPLETED")
    print("=" * 70)

    pause()


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("=" * 70)
        print("                    OPERATING SYSTEMS LAB")
        print("                    EXPERIMENT NO. 3")
        print("=" * 70)

        print("\nPART A - SENDING MESSAGES")
        print("-" * 70)

        print("1.  who       - Display logged-in users")
        print("2.  tty       - Display current terminal")
        print("3.  cat       - Send message using terminal")
        print("4.  wall      - Send message to all users")
        print("5.  write     - Send message to a particular user")
        print("6.  mesg      - Check message permission")
        print("7.  mesg y    - Enable messages")
        print("8.  mesg n    - Disable messages")

        print("\nPART B - SHARED MEMORY")
        print("-" * 70)

        print("9.  ipcs -m       - Display shared memory")
        print("10. ipcs -m -p    - Display process information")
        print("11. ipcs -m -t    - Display time information")
        print("12. ipcs          - Display all IPC information")

        print("\n13. Run Complete Experiment")

        print("0.  Exit")

        print("=" * 70)

        choice = input("\nEnter your choice: ").strip()

        # ----------------------------------------------------
        # MENU SELECTION
        # ----------------------------------------------------

        if choice == "1":

            who_command()

        elif choice == "2":

            tty_command()

        elif choice == "3":

            cat_command()

        elif choice == "4":

            wall_command()

        elif choice == "5":

            write_command()

        elif choice == "6":

            mesg_command()

        elif choice == "7":

            enable_messages()

        elif choice == "8":

            disable_messages()

        elif choice == "9":

            ipcs_shared_memory()

        elif choice == "10":

            ipcs_processes()

        elif choice == "11":

            ipcs_time()

        elif choice == "12":

            complete_ipcs()

        elif choice == "13":

            complete_experiment()

        elif choice == "0":

            print("\n")
            print("=" * 70)
            print("                 PROGRAM TERMINATED")
            print("=" * 70)
            print("Thank you!")
            print()

            sys.exit(0)

        else:

            print("\nInvalid choice!")
            print("Please enter a number between 0 and 13.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
