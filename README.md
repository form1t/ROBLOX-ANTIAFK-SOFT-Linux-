### First Release: Roblox AFK Tool v1.0.0 🚀

This is the first stable release of the auto-jump tool for Roblox on Linux.

**Features included:**
- Auto-pressing the Spacebar to prevent AFK kicks.
- Customizable intervals and jump limits.
- Built-in ±20% random jitter to simulate human behavior.
- Support for both X11 and Wayland sessions.
- Start/Stop via the `F6` hotkey.

**How to use:**
1. Download the `roblox-afk` file below.
2. Make it executable (`Right-click -> Properties -> Allow executing file as program`).
3. Double-click to run.

*Note: Make sure you have installed `xdotool` (for X11) or `ydotool` (for Wayland) via terminal before running.*

**For X11 (Ubuntu, Linux Mint, Pop!_OS, Debian):**
```bash
sudo apt update
sudo apt install xdotool

