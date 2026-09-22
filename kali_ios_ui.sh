#!/bin/bash
set -e

# ============================================================
# Kali Linux XFCE iOS/macOS-style UI Setup
# Designed for Kali Linux XFCE running in VMware.
#
# What this script does:
# 1. Backs up APT sources
# 2. Fixes the Kali repository configuration
# 3. Cleans APT lists and updates packages
# 4. Installs Plank + theme dependencies
# 5. Installs WhiteSur GTK theme
# 6. Installs WhiteSur icon theme
# 7. Configures XFCE to use the theme when available
# 8. Enables Plank at login
#
# Run:
#   chmod +x kali_ios_ui.sh
#   ./kali_ios_ui.sh
# ============================================================

set -u

if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as your normal kali user, NOT with sudo."
    exit 1
fi

echo
echo "=============================================="
echo " Kali XFCE iOS/macOS UI Setup"
echo "=============================================="
echo

if [ "${XDG_CURRENT_DESKTOP:-}" != "XFCE" ] && [ "${DESKTOP_SESSION:-}" != "xfce" ] && [ "${DESKTOP_SESSION:-}" != "lightdm-xsession" ]; then
    echo "WARNING: XFCE was not detected from the current session."
    echo "Your current desktop may not be XFCE."
    read -r -p "Continue anyway? [y/N]: " answer
    case "$answer" in
        y|Y) ;;
        *) echo "Cancelled."; exit 0 ;;
    esac
fi

echo "[1/8] Backing up APT configuration..."

BACKUP_DIR="$HOME/kali-apt-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

sudo cp -a /etc/apt/sources.list "$BACKUP_DIR/sources.list" 2>/dev/null || true
sudo cp -a /etc/apt/sources.list.d "$BACKUP_DIR/sources.list.d" 2>/dev/null || true

echo "APT backup saved to: $BACKUP_DIR"

echo
echo "[2/8] Configuring the official Kali rolling repository..."

# Disable old .list files that may contain stale/third-party Kali mirrors.
sudo mkdir -p /etc/apt/sources.list.d/disabled-by-kali-ios-ui

for f in /etc/apt/sources.list.d/*.list; do
    [ -e "$f" ] || continue

    if grep -qE '(^|[[:space:]])(mirrors\.esto\.network|http\.kali\.org|kali\.download|kali\.org)(/|[[:space:]])' "$f" 2>/dev/null; then
        sudo mv "$f" /etc/apt/sources.list.d/disabled-by-kali-ios-ui/
    fi
done

# Empty the legacy sources.list so there is no duplicate/stale Kali entry.
if [ -f /etc/apt/sources.list ]; then
    sudo cp /etc/apt/sources.list "$BACKUP_DIR/sources.list.original"
fi
printf '%s\n' '# Kali repository is configured in /etc/apt/sources.list.d/kali.sources' | sudo tee /etc/apt/sources.list >/dev/null

sudo tee /etc/apt/sources.list.d/kali.sources >/dev/null <<'EOF'
Types: deb
URIs: http://http.kali.org/kali/
Suites: kali-rolling
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/kali-archive-keyring.gpg
EOF

echo
echo "[3/8] Cleaning old APT package lists..."
sudo rm -rf /var/lib/apt/lists/*
sudo apt clean

echo
echo "[4/8] Updating Kali..."
if ! sudo apt update; then
    echo
    echo "APT update failed."
    echo "The problem is not related to the UI theme."
    echo "Check your Internet connection and try this script again."
    exit 1
fi

echo
echo "[5/8] Installing UI dependencies..."
sudo apt install -y \
    git \
    curl \
    wget \
    plank \
    sassc \
    libglib2.0-dev-bin \
    libxml2-utils \
    gtk2-engines-murrine \
    gnome-themes-extra \
    xfce4-goodies

echo
echo "[6/8] Installing WhiteSur GTK theme..."

THEME_DIR="$HOME/.local/share/kali-ios-ui"
mkdir -p "$THEME_DIR"

if [ -d "$THEME_DIR/WhiteSur-gtk-theme/.git" ]; then
    git -C "$THEME_DIR/WhiteSur-gtk-theme" pull --ff-only || true
else
    rm -rf "$THEME_DIR/WhiteSur-gtk-theme"
    git clone --depth=1 \
        https://github.com/vinceliuice/WhiteSur-gtk-theme.git \
        "$THEME_DIR/WhiteSur-gtk-theme"
fi

cd "$THEME_DIR/WhiteSur-gtk-theme"

# Install GTK theme, XFCE support and Plank theme.
./install.sh -c Light -c Dark --darker --round 2>/dev/null || ./install.sh

echo
echo "[7/8] Installing WhiteSur icon theme..."

if [ -d "$THEME_DIR/WhiteSur-icon-theme/.git" ]; then
    git -C "$THEME_DIR/WhiteSur-icon-theme" pull --ff-only || true
else
    rm -rf "$THEME_DIR/WhiteSur-icon-theme"
    git clone --depth=1 \
        https://github.com/vinceliuice/WhiteSur-icon-theme.git \
        "$THEME_DIR/WhiteSur-icon-theme"
fi

cd "$THEME_DIR/WhiteSur-icon-theme"
./install.sh

echo
echo "[8/8] Configuring XFCE + Plank..."

# Enable Plank on login.
AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"

cat > "$AUTOSTART_DIR/plank.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Plank
Comment=macOS/iOS-style application dock
Exec=plank
Terminal=false
OnlyShowIn=XFCE;
X-GNOME-Autostart-enabled=true
EOF

# Apply XFCE settings when the theme names exist.
xfconf-query -c xsettings -p /Net/ThemeName -s "WhiteSur-Dark" 2>/dev/null || true
xfconf-query -c xsettings -p /Net/IconThemeName -s "WhiteSur" 2>/dev/null || true
xfconf-query -c xfwm4 -p /general/theme -s "WhiteSur-Dark" 2>/dev/null || true

# Make Plank use the WhiteSur theme if installed.
mkdir -p "$HOME/.config/plank/dock1"
cat > "$HOME/.config/plank/dock1/settings" <<'EOF'
[PlankDockPreferences]
#icon-size=48
#hide-mode=1
#position=3
#zoom-enabled=true
#zoom-percent=120
EOF

echo
echo "=============================================="
echo " Installation completed!"
echo "=============================================="
echo
echo "Next steps:"
echo
echo "1. Log out of Kali."
echo "2. Log back in."
echo "3. Plank should start automatically."
echo
echo "If the theme does not appear immediately:"
echo "  Settings -> Appearance -> Style -> WhiteSur-Dark"
echo "  Settings -> Appearance -> Icons -> WhiteSur"
echo
echo "To start the dock manually:"
echo "  plank"
echo
echo "APT backup:"
echo "  $BACKUP_DIR"
echo
echo "Enjoy your iOS/macOS-style Kali desktop!"
