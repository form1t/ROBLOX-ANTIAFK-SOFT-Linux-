import os
import random
import shutil
import subprocess
import time
import tkinter as tk

SESSION = os.environ.get("XDG_SESSION_TYPE", "").lower()


BG = "#040904"
PANEL = "#0a130b"
GREEN = "#39ff6a"
DIM = "#1b7a36"
AMBER = "#ffb000"
RED = "#ff4d4d"

def mono(size, bold=False):
    return ("DejaVu Sans Mono", size, "bold" if bold else "normal")


TR = {
    "ru": {
        "sys_load": "система загружена",
        "err_no_tool": "ОШИБКА: нет xdotool/ydotool",
        "install_hint": "sudo apt install xdotool",
        "engine": "движок:",
        "session": "сессия:",
        "warn_wayland": "ВНИМАНИЕ: Wayland! нужен ydotool",
        "interval": "ИНТЕРВАЛ",
        "jumps": "ПРЫЖКОВ",
        "inf_jumps": "(0 = прыгать бесконечно)",
        "jitter": "случайный разброс ±20%",
        "focus": "переключаться на окно Roblox (xdotool)",
        "start_btn": "▶  СТАРТ",
        "stop_btn": "■  СТОП",
        "hint": "F6 — старт/стоп  |  после СТАРТ переключись в игру (5с)",
        "err_no_keys": "ОШИБКА: нечем нажимать клавиши",
        "start_in": "старт через {0}с — кликни в игру!",
        "stopped": "остановлено. прыжков: {0}",
        "done_log": "ГОТОВО! прыжков: {0}",
        "err_press": "ОШИБКА нажатия: {0}",
        "check_sudo": "запущен ли sudo ydotoold ?",
        "jump_n": "прыжок #{0}",
        "win_not_found": "окно Roblox не найдено",
        "idle": "ОЖИДАНИЕ",
        "countdown": "СТАРТ ЧЕРЕЗ",
        "running": "РАБОТАЕТ",
        "done": "ГОТОВО",
        "next": "СЛЕДУЮЩИЙ :",
        "jumps_lbl": "ПРЫЖКОВ  :"
    },
    "en": {
        "sys_load": "system loaded",
        "err_no_tool": "ERROR: missing xdotool/ydotool",
        "install_hint": "sudo apt install xdotool",
        "engine": "engine:",
        "session": "session:",
        "warn_wayland": "WARNING: Wayland! ydotool is required",
        "interval": "INTERVAL",
        "jumps": "JUMPS",
        "inf_jumps": "(0 = jump infinitely)",
        "jitter": "random jitter ±20%",
        "focus": "auto-focus Roblox window (xdotool)",
        "start_btn": "▶  START",
        "stop_btn": "■  STOP",
        "hint": "F6 — start/stop  |  after START switch to game (5s)",
        "err_no_keys": "ERROR: no keyboard backend",
        "start_in": "starting in {0}s — click the game!",
        "stopped": "stopped. jumps: {0}",
        "done_log": "DONE! jumps: {0}",
        "err_press": "PRESS ERROR: {0}",
        "check_sudo": "is sudo ydotoold running?",
        "jump_n": "jump #{0}",
        "win_not_found": "Roblox window not found",
        "idle": "STANDBY",
        "countdown": "STARTING IN",
        "running": "RUNNING",
        "done": "DONE",
        "next": "NEXT JUMP :",
        "jumps_lbl": "JUMPS    :"
    }
}



def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        return r.returncode == 0, (r.stderr or r.stdout).strip()
    except Exception as e:
        return False, str(e)


class Backend:
    def __init__(self):
        self.name = None
        order = ["ydotool", "xdotool", "pynput"] if SESSION == "wayland" \
            else ["xdotool", "ydotool", "pynput"]
        for n in order:
            if n == "xdotool" and shutil.which("xdotool"):
                self.name = n
                self._d = ["xdotool", "keydown", "space"]
                self._u = ["xdotool", "keyup", "space"]
                return
            if n == "ydotool" and shutil.which("ydotool"):
                self.name = n
                self._d = ["ydotool", "key", "57:1"]
                self._u = ["ydotool", "key", "57:0"]
                return
            if n == "pynput":
                try:
                    from pynput.keyboard import Controller, Key
                    self.kb, self.Key, self.name = Controller(), Key, n
                    return
                except Exception:
                    pass

    def _do(self, cmd, down):
        if self.name == "pynput":
            try:
                (self.kb.press if down else self.kb.release)(self.Key.space)
                return True, ""
            except Exception as e:
                return False, str(e)
        return run(cmd)

    def down(self):
        return self._do(getattr(self, "_d", None), True)

    def up(self):
        return self._do(getattr(self, "_u", None), False)


def focus_roblox():
    ok, out = run(["xdotool", "search", "--name", "Roblox"])
    wid = out.split("\n")[0] if ok and out else ""
    if wid:
        run(["xdotool", "windowactivate", wid])
        return True
    return False



class RetroButton(tk.Label):
    def __init__(self, parent, text, command, fg=GREEN, size=14):
        super().__init__(parent, text=text, fg=fg, bg=BG, font=mono(size, True),
                         bd=2, relief="solid", cursor="hand2", pady=8)
        self.cmd, self.base_fg = command, fg
        self.bind("<Button-1>", lambda e: self.cmd())
        self.bind("<Enter>", lambda e: self.config(bg=self.base_fg, fg=BG))
        self.bind("<Leave>", lambda e: self.config(bg=BG, fg=self.base_fg))

    def set(self, text, fg):
        self.base_fg = fg
        self.config(text=text, fg=fg, bg=BG)


class Stepper(tk.Frame):
    def __init__(self, parent, title, value, lo, hi, fmt, steps=(-10, -1, 1, 10)):
        super().__init__(parent, bg=PANEL)
        self.value, self.lo, self.hi, self.fmt = value, lo, hi, fmt
        self.lbl_title = tk.Label(self, text=title, bg=PANEL, fg=GREEN, font=mono(10),
                                  width=10, anchor="w")
        self.lbl_title.pack(side="left")
        
        for s in steps[:2]:
            self._btn(s)
        self.lbl = tk.Label(self, text=fmt(value), bg=BG, fg=AMBER, font=mono(13, True),
                            width=6, bd=1, relief="solid")
        self.lbl.pack(side="left", padx=5)
        for s in steps[2:]:
            self._btn(s)
        for w in (self.lbl,):
            w.bind("<Button-4>", lambda e: self.add(1))
            w.bind("<Button-5>", lambda e: self.add(-1))

    def _btn(self, s):
        b = tk.Label(self, text=f"{s:+d}", bg=PANEL, fg=GREEN, font=mono(10, True),
                     width=4, bd=1, relief="solid", cursor="hand2")
        b.pack(side="left", padx=1)
        b.bind("<Button-1>", lambda e: self.add(s))
        b.bind("<Enter>", lambda e: b.config(bg=GREEN, fg=BG))
        b.bind("<Leave>", lambda e: b.config(bg=PANEL, fg=GREEN))

    def add(self, d):
        self.value = max(self.lo, min(self.hi, self.value + d))
        self.lbl.config(text=self.fmt(self.value))


class Toggle(tk.Label):
    def __init__(self, parent, text, value):
        super().__init__(parent, bg=PANEL, fg=GREEN, font=mono(10), anchor="w",
                         cursor="hand2")
        self.value, self.txt = value, text
        self.bind("<Button-1>", self.flip)
        self.render()

    def render(self):
        self.config(text=("[X] " if self.value else "[ ] ") + self.txt)

    def flip(self, _=None):
        self.value = not self.value
        self.render()



COUNTDOWN = 5.0

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ROBLOX AFK // RETRO")
        self.geometry("480x720")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.lang = "ru"            # Исходный язык
        self.be = Backend()
        self.mode = "idle"          # idle / countdown / running / done
        self.jumps = 0
        self.next_ts = 0.0
        self.span = 1.0
        self.release_ts = None
        self.finish_after_release = False
        self.global_flag = False
        self.tick_n = 0

        self._build()
        self._global_hotkey()
        self.bind("<F6>", lambda e: self.toggle())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.add_log(self.tr("sys_load"))
        if not self.be.name:
            self.add_log(self.tr("err_no_tool"))
            self.add_log(self.tr("install_hint"))
        else:
            self.add_log(f"{self.tr('engine')} {self.be.name}, {self.tr('session')} {SESSION or '?'}")
            if SESSION == "wayland" and self.be.name != "ydotool":
                self.add_log(self.tr("warn_wayland"))
        self.after(50, self.tick)

    def tr(self, key):
        """Возвращает строку для текущего языка"""
        return TR[self.lang].get(key, key)

    def toggle_language(self, event=None):
        self.lang = "en" if self.lang == "ru" else "ru"
        self.lang_btn.config(text="RU [EN]" if self.lang == "en" else "[RU] EN")
        self.update_ui_texts()

    def update_ui_texts(self):
        """Обновляет статические тексты в интерфейсе при смене языка"""
        self.st_interval.lbl_title.config(text=self.tr("interval"))
        self.st_jumps.lbl_title.config(text=self.tr("jumps"))
        self.lbl_inf_jumps.config(text=self.tr("inf_jumps"))
        
        self.t_jitter.txt = self.tr("jitter")
        self.t_jitter.render()
        
        self.t_focus.txt = self.tr("focus")
        self.t_focus.render()
        
        if self.mode == "idle" or self.mode == "done":
            self.btn.set(self.tr("start_btn"), GREEN)
        else:
            self.btn.set(self.tr("stop_btn"), RED)
            
        self.lbl_hint.config(text=self.tr("hint"))

    def _global_hotkey(self):
        try:
            from pynput import keyboard
            def on_press(key):
                if key == keyboard.Key.f6:
                    self.global_flag = True
            self._lst = keyboard.Listener(on_press=on_press)
            self._lst.daemon = True
            self._lst.start()
        except Exception:
            pass

    
    def _build(self):
        
        self.lang_btn = tk.Label(self, text="[RU] EN", bg=BG, fg=DIM, font=mono(10, True), cursor="hand2")
        self.lang_btn.place(relx=1.0, x=-10, y=10, anchor="ne")
        self.lang_btn.bind("<Button-1>", self.toggle_language)

        tk.Label(self, text="╔═══════════════════════╗", bg=BG, fg=DIM,
                 font=mono(12)).pack(pady=(14, 0))
        tk.Label(self, text="║  R O B L O X   A F K  ║", bg=BG, fg=GREEN,
                 font=mono(14, True)).pack()
        tk.Label(self, text="╚═══════════════════════╝", bg=BG, fg=DIM,
                 font=mono(12)).pack()

        
        self.W, self.H = 440, 190
        self.cv = tk.Canvas(self, width=self.W, height=self.H, bg=BG,
                            highlightthickness=2, highlightbackground=DIM)
        self.cv.pack(pady=(10, 8))
        for y in range(0, self.H, 3):
            self.cv.create_line(0, y, self.W, y, fill="#07140a")

        
        card = tk.Frame(self, bg=PANEL, highlightthickness=1, highlightbackground=DIM)
        card.pack(padx=20, fill="x")
        inner = tk.Frame(card, bg=PANEL)
        inner.pack(padx=12, pady=10, fill="x")

        self.st_interval = Stepper(inner, self.tr("interval"), 30, 1, 3600,
                                   lambda v: f"{v}s")
        self.st_interval.pack(fill="x", pady=3)
        
        self.st_jumps = Stepper(inner, self.tr("jumps"), 0, 0, 9999,
                                lambda v: "∞" if v == 0 else str(v),
                                steps=(-10, -1, 1, 10))
        self.st_jumps.pack(fill="x", pady=3)
        
        self.lbl_inf_jumps = tk.Label(inner, text=self.tr("inf_jumps"), bg=PANEL, fg=DIM,
                                      font=mono(8), anchor="w")
        self.lbl_inf_jumps.pack(fill="x", padx=2)

        self.t_jitter = Toggle(inner, self.tr("jitter"), True)
        self.t_jitter.pack(fill="x", pady=(6, 0))
        self.t_focus = Toggle(inner, self.tr("focus"), False)
        self.t_focus.pack(fill="x")

        
        self.btn = RetroButton(self, self.tr("start_btn"), self.toggle)
        self.btn.pack(padx=20, pady=10, fill="x")

        
        self.log_box = tk.Text(self, height=7, bg=PANEL, fg=GREEN, font=mono(9),
                               bd=0, highlightthickness=1, highlightbackground=DIM,
                               state="disabled", takefocus=0, wrap="word")
        self.log_box.pack(padx=20, fill="x")

        self.lbl_hint = tk.Label(self, text=self.tr("hint"), bg=BG, fg=DIM, font=mono(8))
        self.lbl_hint.pack(pady=6)

    def add_log(self, msg):
        b = self.log_box
        b.config(state="normal")
        b.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        b.see("end")
        b.config(state="disabled")

    
    def toggle(self):
        if self.mode == "idle" or self.mode == "done":
            self.start()
        else:
            self.stop()

    def start(self):
        if not self.be.name:
            self.add_log(self.tr("err_no_keys"))
            return
        self.jumps = 0
        self.finish_after_release = False
        self.mode = "countdown"
        self.span = COUNTDOWN
        self.next_ts = time.time() + COUNTDOWN
        self.btn.set(self.tr("stop_btn"), RED)
        self.add_log(self.tr("start_in").format(int(COUNTDOWN)))

    def stop(self):
        if self.release_ts is not None:
            self.be.up()
            self.release_ts = None
        self.mode = "idle"
        self.btn.set(self.tr("start_btn"), GREEN)
        self.add_log(self.tr("stopped").format(self.jumps))

    def finish(self):
        self.mode = "done"
        self.btn.set(self.tr("start_btn"), GREEN)
        self.add_log(self.tr("done_log").format(self.jumps))

    def schedule_next(self):
        base = float(self.st_interval.value)
        if self.t_jitter.value:
            base *= random.uniform(0.8, 1.2)
        self.span = max(0.5, base)
        self.next_ts = time.time() + self.span

    def do_jump(self):
        if self.t_focus.value and self.be.name == "xdotool":
            if focus_roblox():
                time.sleep(0.25)
            else:
                self.add_log(self.tr("win_not_found"))
        ok, err = self.be.down()
        if not ok:
            self.add_log(self.tr("err_press").format(err[:60] or '...'))
            if self.be.name == "ydotool":
                self.add_log(self.tr("check_sudo"))
        self.jumps += 1
        self.release_ts = time.time() + 0.12
        self.add_log(self.tr("jump_n").format(self.jumps))
        
        target = self.st_jumps.value
        if target and self.jumps >= target:
            self.finish_after_release = True
            self.next_ts = float("inf")
        else:
            self.schedule_next()

    def on_close(self):
        if self.release_ts is not None:
            self.be.up()
        self.destroy()

    def tick(self):
        now = time.time()
        self.tick_n += 1

        if self.global_flag:
            self.global_flag = False
            self.toggle()

        if self.release_ts is not None and now >= self.release_ts:
            self.be.up()
            self.release_ts = None
            if self.finish_after_release:
                self.finish_after_release = False
                self.finish()

        if self.mode == "countdown" and now >= self.next_ts:
            self.mode = "running"
            self.do_jump()
        elif self.mode == "running" and now >= self.next_ts:
            self.do_jump()

        self.draw(now)
        self.after(50, self.tick)

    
    def draw(self, now):
        c = self.cv
        c.delete("dyn")
        blink = (self.tick_n // 10) % 2 == 0
        cur = "█" if blink else " "

        c.create_text(14, 18, anchor="w", text="> ROBLOX_AFK.EXE", fill=DIM,
                      font=mono(10), tags="dyn")

        status = {
            "idle": (self.tr("idle"), AMBER), 
            "countdown": (self.tr("countdown"), AMBER),
            "running": (self.tr("running"), GREEN), 
            "done": (self.tr("done"), GREEN)
        }[self.mode]
        
        left = max(0.0, self.next_ts - now) if self.next_ts != float("inf") else 0.0
        txt = status[0]
        if self.mode == "countdown":
            txt += f" {left:.0f}"
        c.create_text(self.W // 2, 62, text=txt + cur, fill=status[1],
                      font=mono(22, True), tags="dyn")

        target = self.st_jumps.value
        c.create_text(14, 108, anchor="w", fill=GREEN, font=mono(12), tags="dyn",
                      text=f"{self.tr('jumps_lbl')} {self.jumps}/{'∞' if target == 0 else target}")
        
        nxt = f"{left:4.0f}s" if self.mode in ("running", "countdown") else "  --"
        c.create_text(14, 132, anchor="w", fill=GREEN, font=mono(12), tags="dyn",
                      text=f"{self.tr('next')} {nxt}")

        if self.mode in ("running", "countdown"):
            frac = 1 - min(1.0, left / max(0.1, self.span))
        else:
            frac = 1.0 if self.mode == "done" else 0.0
        n = int(frac * 30)
        c.create_text(14, 166, anchor="w", fill=GREEN if self.mode != "idle" else DIM,
                      font=mono(11), tags="dyn",
                      text="[" + "█" * n + "░" * (30 - n) + "]")

        if self.release_ts is not None:
            c.create_text(self.W - 14, 108, anchor="e", text="^ JUMP ^",
                          fill=AMBER, font=mono(12, True), tags="dyn")

if __name__ == "__main__":
    App().mainloop()
