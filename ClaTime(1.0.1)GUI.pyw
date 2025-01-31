import tkinter as tk
import time
import threading
import logging
from datetime import datetime

stop_script = False

# Global tracking variables
total_work_time = 0.0
total_break_time = 0.0
work_cycles_completed = 0

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        filename='clatime_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("========== New ClaTime Session Started ==========")

def log_event(event_type, duration=None, message=None):
    """Log various events during the Pomodoro session."""
    if event_type == "work_start":
        logging.info("Work session started")
    elif event_type == "work_complete":
        logging.info(f"Work session completed - Duration: {duration:.2f} minutes")
    elif event_type == "break_start":
        logging.info("Break session started")
    elif event_type == "break_complete":
        logging.info(f"Break session completed - Duration: {duration:.2f} minutes")
    elif event_type == "long_break_start":
        logging.info("Long break session started")
    elif event_type == "session_end":
        logging.info("Session ended by user")
    elif event_type == "custom":
        logging.info(message)

def log_results():
    """Write summary to a log file after user stops the script."""
    global total_work_time, total_break_time, work_cycles_completed
    total_work_minutes = total_work_time / 60.0
    total_break_minutes = total_break_time / 60.0

    logging.info("======= Session Summary =======")
    logging.info(f"Work cycles completed: {work_cycles_completed}")
    logging.info(f"Total work time (minutes): {total_work_minutes:.2f}")
    logging.info(f"Total break time (minutes): {total_break_minutes:.2f}")
    logging.info("=============================")

def pomodoro_cycle(ui_update_callback):
    """
    Conducts the Pomodoro cycles in a loop:
      - 4 cycles of (30 min work, 5 min break)
      - Then a 20 min long break
    ui_update_callback is a function to update the GUI label text.
    """
    global stop_script, total_work_time, total_break_time, work_cycles_completed

    # Repeat the cycles until user stops
    while not stop_script:
        for _ in range(4):
            if stop_script:
                break

            # Work session
            log_event("work_start")
            run_countdown(30 * 60, "Working", ui_update_callback, "work")

            if stop_script:
                break

            # Short break
            log_event("break_start")
            run_countdown(5 * 60, "Short Break", ui_update_callback, "break")

        if stop_script:
            break

        # Long break
        log_event("long_break_start")
        run_countdown(20 * 60, "Long Break", ui_update_callback, "long_break")

    log_results()
    log_event("session_end")
    ui_update_callback("Session stopped. Summary logged.")

def run_countdown(duration, phase_label, ui_update_callback, session_type):
    """
    Counts down from 'duration' seconds. Updates the UI every second.
    phase_label is a string to indicate whether it's a work or break session.
    ui_update_callback is used to update the GUI label.
    """
    global stop_script, total_work_time, total_break_time, work_cycles_completed

    start_time = time.time()
    seconds_remaining = duration

    while seconds_remaining >= 0 and not stop_script:
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60
        ui_text = f"{phase_label}: {minutes:02d}:{seconds:02d}"
        ui_update_callback(ui_text)
        time.sleep(1)
        seconds_remaining -= 1

    end_time = time.time()
    elapsed = end_time - start_time
    elapsed_minutes = elapsed / 60.0

    if session_type == 'work':
        if not stop_script:
            work_cycles_completed += 1
        total_work_time += elapsed
        log_event("work_complete", elapsed_minutes)
    elif session_type == 'long_break':
        total_break_time += elapsed
        log_event("break_complete", elapsed_minutes, "Long break completed")
    else:
        total_break_time += elapsed
        log_event("break_complete", elapsed_minutes)

class PomodoroGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ClaTime Productivity Tool")
        self.master.geometry("400x200")
        self.master.resizable(False, False)

        # A modern, minimalistic style
        self.master.configure(bg="#F0F0F0")

        self.timer_label = tk.Label(
            self.master,
            text="Welcome to ClaTime!",
            font=("Helvetica", 14, "bold"),
            fg="#333333",
            bg="#F0F0F0"
        )
        self.timer_label.pack(pady=20)

        button_frame = tk.Frame(self.master, bg="#F0F0F0")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            command=self.start_timer
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            font=("Helvetica", 12),
            bg="#F44336",
            fg="white",
            padx=20,
            pady=5,
            command=self.stop_timer
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Track the thread so we can ensure we don't start multiple sessions
        self.timer_thread = None

    def start_timer(self):
        global stop_script
        if self.timer_thread is not None and self.timer_thread.is_alive():
            # Already running
            return

        stop_script = False
        self.timer_label.config(text="Preparing Pomodoro cycles...")

        def run_pomodoro():
            pomodoro_cycle(self.update_timer_label)

        self.timer_thread = threading.Thread(target=run_pomodoro, daemon=True)
        self.timer_thread.start()

    def stop_timer(self):
        global stop_script
        stop_script = True

    def update_timer_label(self, new_text):
        self.timer_label.config(text=new_text)

def main():
    setup_logging()
    log_event("custom", message="ClaTime application started (GUI)")

    root = tk.Tk()
    app = PomodoroGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()