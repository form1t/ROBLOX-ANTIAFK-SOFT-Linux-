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


### 📥 How to Download & Run

1. **Download the app:**
   Go to the right-side panel and click on **[Releases](../../releases)** (or look for **Roblox AFK Tool v1.0.0**), then download the **`roblox-afk`** file.

2. **Make it executable:**
   Since Linux blocks downloaded binaries by default, you need to give it permission to run:
   * **Option A (Mouse):** Right-click the downloaded `roblox-afk` file ➔ **Properties** ➔ **Permissions** ➔ Change owner access to **"Read and execute"** (or check "Allow executing file as program").
   * **Option B (Terminal):** Open a terminal in the folder with the file and run:
     ```bash
     chmod +x roblox-afk
     ```

3. **Launch:**
   Double-click the file (or run `./roblox-afk` in the terminal) to launch the app!

---

### 🛠 Required Dependencies
Make sure you have installed the required tool for your system via terminal before running:

* **For X11:**
  ```bash
  sudo apt install xdotool
