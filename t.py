#!/usr/bin/env python3

import os
import subprocess
import sys


# ============================================================
#                OPERATING SYSTEMS LAB
#                  EXPERIMENT NO. 3
#
# a. Commands for Sending Messages to Logged-in Users
#    who, cat, wall, write, mesg
#
# b. List Processes Attached to a Shared Memory Segment
#    ipcs
# ============================================================


# ------------------------------------------------------------
# FUNCTION: Run Linux command
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# FUNCTION: Pause
# ------------------------------------------------------------

def pause():

    input("\nPress ENTER to continue...")


# ------------------------------------------------------------
# 1. WHO COMMAND
# ------------------------------------------------------------

def who_command():

    print("\n")
    print("=" * 60)
    print("                    WHO COMMAND")
    print("=" * 60)

    print("\nPurpose:")
    print("Displays users currently logged into the Linux system.\n")

    run_command(["who"])

    pause()


# ------------------------------------------------------------
# 2. TTY COMMAND
# ------------------------------------------------------------

def tty_command():

    print("\n")
    print("=" * 60)
    print("                    TTY COMMAND")
    print("=" * 60)

    print("\nPurpose:")
    print("Displays the terminal associated with the current session.\n")

    run_command(["tty"])

    pause()


# ------------------------------------------------------------
# 3. CAT COMMAND
# ------------------------------------------------------------

def cat_command():

    print("\n")
    print("=" * 60)
    print("                    CAT COMMAND")
    print("=" * 60)

    print("\nThe cat command can be used to write a message")
    print("to a terminal device.\n")

    print("Currently logged-in users:\n")

    run_command(["who"])

    print("\nExample terminal:")
    print("pts/3")
    print("pts/21")
    print("pts/2")

    print()

    terminal = input(
        "Enter terminal (example pts/3): "
    ).strip()

    # --------------------------------------------------------
    # Validate terminal
    # --------------------------------------------------------

    if not terminal.startswith("pts/"):

        print("\nInvalid terminal!")
        print("Use a terminal such as pts/3 or pts/21.")
        pause()
        return

    terminal_number = terminal[4:]

    if not terminal_number.isdigit():

        print("\nInvalid terminal!")
        print("Example: pts/3")
        pause()
        return

    device = "/dev/" + terminal

    # --------------------------------------------------------
    # Check whether terminal exists
    # --------------------------------------------------------

    if not os.path.exists(device):

        print("\nTerminal does not exist:", device)
        print("Check the output of the 'who' command.")

        pause()
        return

    # --------------------------------------------------------
    # Enter message
    # --------------------------------------------------------

    print("\nEnter your message:")

    message = input("Message: ")

    if not message:

        print("\nMessage cannot be empty.")
        pause()
        return

    # --------------------------------------------------------
    # Send message
    # --------------------------------------------------------

    try:

        with open(device, "w") as terminal_file:

            terminal_file.write(
                "\n"
                "====================================\n"
                "Message from Experiment No. 3\n"
                "====================================\n"
                + message +
                "\n"
                "====================================\n"
            )

        print("\nMessage sent successfully!")

    except PermissionError:

        print("\nPermission denied.")
        print("You do not have permission to write to this terminal.")

    except Exception as error:

        print("\nError:", error)

    pause()


# ------------------------------------------------------------
# 4. WALL COMMAND
# ------------------------------------------------------------

def wall_command():

    print("\n")
    print("=" * 60)
    print("                    WALL COMMAND")
    print("=" * 60)

    print("\nPurpose:")
    print("Sends a message to all logged-in users.\n")

    message = input("Enter message: ")

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

            print("\nUnable to send the message.")

            if result.stderr:
                print("Reason:", result.stderr.strip())

    except FileNotFoundError:

        print("\nwall command is not available.")

    except Exception as error:

        print("\nError:", error)

    pause()


# ------------------------------------------------------------
# 5. WRITE COMMAND
# ------------------------------------------------------------

def write_command():

    print("\n")
    print("=" * 60)
    print("                   WRITE COMMAND")
    print("=" * 60)

    print("\nPurpose:")
    print("Sends a message to a particular user's terminal.\n")

    print("Currently logged-in users:\n")

    run_command(["who"])

    print("\n")
    print("From the above list, use a username and its")
    print("corresponding terminal.")
    print()
    print("Example:")
    print("Username : dce")
    print("Terminal : pts/3")
    print()

    # --------------------------------------------------------
    # Get username
    # --------------------------------------------------------

    username = input("Enter username: ").strip()

    if not username:

        print("\nUsername cannot be empty.")
        pause()
        return

    # --------------------------------------------------------
    # Get terminal
    # --------------------------------------------------------

    terminal = input(
        "Enter terminal (example pts/3): "
    ).strip()

    if not terminal:

        print("\nTerminal cannot be empty.")
        pause()
        return

    # --------------------------------------------------------
    # Correct terminal validation
    #
    # pts/3 is VALID.
    # pts/21 is VALID.
    # pts/2 is VALID.
    # --------------------------------------------------------

    if not terminal.startswith("pts/"):

        print("\nInvalid terminal!")
        print("Enter a terminal such as:")
        print("pts/3")
        print("pts/21")
        print("pts/2")

        pause()
        return

    terminal_number = terminal[4:]

    if not terminal_number.isdigit():

        print("\nInvalid terminal!")
        print("The terminal should look like pts/3.")

        pause()
        return

    # --------------------------------------------------------
    # Check whether this username + terminal exists
    # --------------------------------------------------------

    try:

        who_result = subprocess.run(
            ["who"],
            capture_output=True,
            text=True
        )

        logged_in = False

        for line in who_result.stdout.splitlines():

            parts = line.split()

            if len(parts) >= 2:

                current_user = parts[0]
                current_terminal = parts[1]

                if (
                    current_user == username
                    and current_terminal == terminal
                ):

                    logged_in = True
                    break

        if not logged_in:

            print("\nThe following user/terminal combination")
            print("was not found in the current 'who' output.")

            print("\nYou entered:")
            print("Username :", username)
            print("Terminal :", terminal)

            print("\nPlease use an exact username and terminal")
            print("shown by the 'who' command.")

            pause()
            return

    except Exception as error:

        print("\nCould not verify the login information.")
        print("Error:", error)

        pause()
        return

    # --------------------------------------------------------
    # Enter message
    # --------------------------------------------------------

    print("\nUser and terminal found successfully.")

    print("\nEnter your message:")

    message = input("Message: ")

    if not message:

        print("\nMessage cannot be empty.")
        pause()
        return

    # --------------------------------------------------------
    # Send message using write
    # --------------------------------------------------------

    print("\nSending message...")
    print("-" * 40)

    try:

        result = subprocess.run(
            ["write", username, terminal],
            input=message + "\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:

            print("Message sent successfully!")
            print()
            print("Username :", username)
            print("Terminal :", terminal)
            print("Message  :", message)

        else:

            print("Unable to send the message.")

            if result.stderr:

                print("\nReason:")
                print(result.stderr.strip())

    except FileNotFoundError:

        print("\nThe 'write' command is not installed.")

    except Exception as error:

        print("\nError:", error)

    pause()


# ------------------------------------------------------------
# 6. MESG COMMAND
# ------------------------------------------------------------

def mesg_command():

    print("\n")
    print("=" * 60)
    print("                    MESG COMMAND")
    print("=" * 60)

    print("\nPurpose:")
    print("Checks whether other users can send messages")
    print("to your terminal.\n")

    run_command(["mesg"])

    pause()


# ------------------------------------------------------------
# 7. ENABLE MESSAGES
# ------------------------------------------------------------

def enable_messages():

    print("\n")
    print("=" * 60)
    print("                 ENABLE MESSAGES")
    print("=" * 60)

    result = run_command(["mesg", "y"])

    if result == 0:

        print("\nMessages have been ENABLED.")

        print("\nCurrent status:")
        run_command(["mesg"])

    pause()


# ------------------------------------------------------------
# 8. DISABLE MESSAGES
# ------------------------------------------------------------

def disable_messages():

    print("\n")
    print("=" * 60)
    print("                 DISABLE MESSAGES")
    print("=" * 60)

    result = run_command(["mesg", "n"])

    if result == 0:

        print("\nMessages have been DISABLED.")

        print("\nCurrent status:")
        run_command(["mesg"])

    pause()


# ------------------------------------------------------------
# 9. IPCS -M
# ------------------------------------------------------------

def ipcs_shared_memory():

    print("\n")
    print("=" * 60)
    print("                   IPCS -M")
    print("=" * 60)

    print("\nPurpose:")
    print("Displays shared memory segments.\n")

    run_command(["ipcs", "-m"])

    pause()


# ------------------------------------------------------------
# 10. IPCS -M -P
# ------------------------------------------------------------

def ipcs_processes():

    print("\n")
    print("=" * 60)
    print("                 IPCS -M -P")
    print("=" * 60)

    print("\nPurpose:")
    print("Displays the creator PID and last-operation PID")
    print("associated with shared memory segments.\n")

    run_command(["ipcs", "-m", "-p"])

    pause()


# ------------------------------------------------------------
# 11. IPCS -M -T
# ------------------------------------------------------------

def ipcs_time():

    print("\n")
    print("=" * 60)
    print("                 IPCS -M -T")
    print("=" * 60)

    print("\nPurpose:")
    print("Displays time information for shared memory segments.\n")

    run_command(["ipcs", "-m", "-t"])

    pause()


# ------------------------------------------------------------
# 12. COMPLETE IPC INFORMATION
# ------------------------------------------------------------

def complete_ipcs():

    print("\n")
    print("=" * 60)
    print("                     IPCS")
    print("=" * 60)

    print("\nPurpose:")
    print("Displays System V IPC information.")
    print("This includes:")
    print("- Message queues")
    print("- Shared memory")
    print("- Semaphores\n")

    run_command(["ipcs"])

    pause()


# ------------------------------------------------------------
# 13. COMPLETE EXPERIMENT
# ------------------------------------------------------------

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
    print("PART A: COMMANDS FOR SENDING MESSAGES")
    print("=" * 70)

    # WHO

    print("\n1. WHO COMMAND")
    print("-" * 70)

    run_command(["who"])

    # TTY

    print("\n2. TTY COMMAND")
    print("-" * 70)

    run_command(["tty"])

    # MESG

    print("\n3. MESG COMMAND")
    print("-" * 70)

    run_command(["mesg"])

    # WALL

    print("\n4. WALL COMMAND")
    print("-" * 70)

    try:

        result = subprocess.run(
            ["wall"],
            input="Experiment No. 3: Hello from Python!\n",
            text=True,
            capture_output=True
        )

        if result.returncode == 0:
            print("Test wall message sent successfully.")

        else:
            print("Wall message could not be sent.")

    except Exception as error:

        print("Error:", error)

    # ========================================================
    # PART B
    # ========================================================

    print("\n")
    print("=" * 70)
    print("PART B: SHARED MEMORY")
    print("=" * 70)

    # IPCS -M

    print("\n5. IPCS -M")
    print("-" * 70)

    run_command(["ipcs", "-m"])

    # IPCS -M -P

    print("\n6. IPCS -M -P")
    print("-" * 70)

    run_command(["ipcs", "-m", "-p"])

    # IPCS -M -T

    print("\n7. IPCS -M -T")
    print("-" * 70)

    run_command(["ipcs", "-m", "-t"])

    # ========================================================

    print("\n")
    print("=" * 70)
    print("             EXPERIMENT NO. 3 COMPLETED")
    print("=" * 70)

    pause()


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

def main():

    while True:

        print("\n")
        print("=" * 70)
        print("                  OPERATING SYSTEMS LAB")
        print("                  EXPERIMENT NO. 3")
        print("=" * 70)

        print("\nPART A - MESSAGE COMMANDS")
        print("-" * 70)

        print("1.  who       - Display logged-in users")
        print("2.  tty       - Display current terminal")
        print("3.  cat       - Send message using terminal")
        print("4.  wall      - Send message to all users")
        print("5.  write     - Send message to particular user")
        print("6.  mesg      - Check message permission")
        print("7.  mesg y    - Enable messages")
        print("8.  mesg n    - Disable messages")

        print("\nPART B - SHARED MEMORY")
        print("-" * 70)

        print("9.  ipcs -m       - Display shared memory")
        print("10. ipcs -m -p    - Display process IDs")
        print("11. ipcs -m -t    - Display time information")
        print("12. ipcs          - Display complete IPC information")

        print("\n13. Run Complete Experiment")
        print("0.  Exit")

        print("=" * 70)

        choice = input("\nEnter your choice: ").strip()

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

            print("\nProgram terminated.")
            print("Thank you!")

            sys.exit(0)

        else:

            print("\nInvalid choice!")
            print("Please enter a number from 0 to 13.")


# ------------------------------------------------------------
# PROGRAM START
# ------------------------------------------------------------

if __name__ == "__main__":

    main()
