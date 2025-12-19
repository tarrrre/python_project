"""
Colab Work Timer
- Pomodoro-style work/break timer
- Browser notification + Colab audio
"""

import time
import numpy as np
from datetime import datetime
from IPython.display import display, HTML, Audio

# =========================
# 설정(Configuration)
# =========================
WORK_MINUTES = 25
BREAK_MINUTES = 5
CYCLES = 2
ENABLE_SOUND = True



# =========================
# 오디오(Audio Utilities)
# =========================
def _play_wave(wave, sr=44100):
    display(Audio(wave, rate=sr, autoplay=True))

def _beep(freq, duration):
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration))
    return np.sin(2 * np.pi * freq * t)

# =========================
# 사운드 패턴(Sound Patterns)
# =========================
def sound_work_end():
    wave = np.concatenate([
        _beep(880, 0.4) * np.exp(-2 * np.linspace(0, 0.4, int(44100 * 0.4)))
        for _ in range(6)
    ])
    _play_wave(wave)

def sound_break_end():
    wave = np.concatenate([
        _beep(1200, 0.3) *
        (np.sin(2 * np.pi * 4 * np.linspace(0, 0.3, int(44100 * 0.3))) > 0)
        for _ in range(8)
    ])
    _play_wave(wave)

def sound_all_done():
    melody = [(880, 0.3), (1320, 0.3), (1760, 0.4)]
    wave = np.concatenate([
        _beep(f, d)
        for _ in range(3)
        for f, d in melody
    ])
    _play_wave(wave)

def play_sound(kind):
    if not ENABLE_SOUND:
        return
    if kind == "work_end":
        sound_work_end()
    elif kind == "break_end":
        sound_break_end()
    elif kind == "all_done":
        sound_all_done()

# =========================
# 타이머 로직(Timer Logic)
# =========================
def run_timer(minutes, label):
    print(f"\n⏳ {label} started ({minutes} min)")
    time.sleep(minutes * 60)

    now = datetime.now().strftime("%H:%M")
    print(f"🔔 {label} finished - {now}")

    notify(f"{label} finished", f"{now} - move to next step")

    play_sound("work_end" if label == "Work" else "break_end")

def pomodoro(work, rest, cycles):
    print("🍅 Pomodoro Timer Started")

    for i in range(1, cycles + 1):
        print(f"\n▶ Cycle {i}/{cycles}")
        run_timer(work, "Work")
        run_timer(rest, "Break")

    print("\n🎉 All cycles completed")
    notify("Timer Completed", "All work cycles are done 🎉")
    play_sound("all_done")

# =========================
# 메인 실행부(Entry Point)
# =========================
if __name__ == "__main__":
    pomodoro(WORK_MINUTES, BREAK_MINUTES, CYCLES)
