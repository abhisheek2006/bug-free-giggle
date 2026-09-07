cd() {
    if [[ "$1" == "hp" ]]; then
        read -s -p "Password: " password
        echo

        if [[ "$password" == "terror" ]]; then
            builtin cd "$HOME/secret"
        else
            echo "Access denied."
            return 1
        fi
    else
        builtin cd "$@"
    fi
}
