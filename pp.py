#!/usr/bin/env python3
import json
import os
import sys

JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "linux_os_12_experiments.json")

def load_experiments():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found: {JSON_FILE}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)

def show_experiment(data, number):
    exp = data.get(str(number))
    if not exp:
        print("Experiment not found.")
        return

    print("\n" + "=" * 70)
    print(f"EXPERIMENT {number}: {exp['title']}")
    print("=" * 70)
    print(exp.get("answer", ""))

    if exp.get("code"):
        print("\n--- PYTHON PROGRAM ---")
        print(exp["code"])

    print("=" * 70)

def main():
    data = load_experiments()

    while True:
        print("\nLinux / Operating Systems Experiments")
        print("-------------------------------------")
        print("1-12 : Show an experiment")
        print("a    : Show all experiment titles")
        print("q    : Quit")

        choice = input("\nEnter experiment number: ").strip().lower()

        if choice == "q":
            print("Exiting...")
            break

        if choice == "a":
            for number, exp in data.items():
                print(f"{number}. {exp['title']}")
            continue

        if choice.isdigit() and 1 <= int(choice) <= 12:
            show_experiment(data, int(choice))
        else:
            print("Invalid choice. Enter a number from 1 to 12, 'a', or 'q'.")

if __name__ == "__main__":
    main()

