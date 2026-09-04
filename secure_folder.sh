#!/bin/bash

FOLDER="$HOME/.private_folder"
MAX_ATTEMPTS=3

# Create folder if it doesn't exist
if [ ! -d "$FOLDER" ]; then
    mkdir -p "$FOLDER"
    chmod 700 "$FOLDER"
fi

echo "================================"
echo "       PRIVATE FOLDER"
echo "================================"

attempt=1

while [ $attempt -le $MAX_ATTEMPTS ]; do
    read -rsp "Enter password: " PASSWORD
    echo

    # Change this password
    if [ "$PASSWORD" = "MyPassword123" ]; then
        echo "Access granted."

        chmod 700 "$FOLDER"
        cd "$FOLDER"

        echo
        echo "Private folder: $FOLDER"
        echo "You are now inside the folder."
        echo "Type 'exit' when finished."

        bash

        exit 0
    else
        echo "Wrong password. Attempt $attempt/$MAX_ATTEMPTS"
        attempt=$((attempt + 1))
    fi
done

echo
echo "Maximum attempts reached."
echo "Deleting the private folder..."

rm -rf "$FOLDER"

echo "Private folder deleted."
