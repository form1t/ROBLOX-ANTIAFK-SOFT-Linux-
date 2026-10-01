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

### 🚀 How to Run

1. **Download the app:** Go to the **Releases** section on the right side of the page and download the **`roblox-afk`** file[cite: 4, 5].
2. **Make it executable:** 
   * Right-click the downloaded file ➔ **Properties** ➔ **Permissions**[cite: 5].
   * Look down, find the owner permissions, and change "Read and write" to **"Read and execute"** (allow executing file as program)[cite: 5].
3. **Launch:** Double-click the file to run it!

⚠️ **Troubleshooting (If double-clicking doesn't work):**
If the app still won't open or your system doesn't know what to do with it, you can easily launch it via the terminal in 2 seconds:
1. Open your terminal in the folder where the file is located.
2. Type this command and press Enter:
   ```bash
   chmod +x roblox-afk
   ./roblox-afk



*Note: Make sure you have installed `xdotool` (for X11) or `ydotool` (for Wayland) via terminal before running.*

**For X11 (Ubuntu, Linux Mint, Pop!_OS, Debian):**
```bash
sudo apt update
sudo apt install xdotool

