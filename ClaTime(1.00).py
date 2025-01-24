import time
import threading
import logging
from datetime import datetime

stop_script = False

# Logging info
total_work_time = 0.0
total_break_time = 0.0
work_cycles_completed = 0

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        filename='clatime_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Add a separator line when starting a new session
    logging.info("========== New ClaTime Session Started ==========")

def log_event(event_type, duration=None, message=None):
    """Log various events during the Pomodoro session"""
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

def wait_for_enter():
    global stop_script
    input()
    stop_script = True
    log_event("session_end")

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

def countdown(total_seconds, label, session_type):
    """
    Counts down from total_seconds. 
    session_type should be 'work' or 'break' or 'long_break' for logging purposes.
    """
    global stop_script, total_work_time, total_break_time, work_cycles_completed

    start_time = time.time()
    
    if session_type == 'work':
        log_event("work_start")
    elif session_type == 'long_break':
        log_event("long_break_start")
    else:
        log_event("break_start")

    for remaining in range(total_seconds, -1, -1):
        if stop_script:
            break
        minutes = remaining // 60
        seconds = remaining % 60
        print(f"\r{label} {minutes:02d}:{seconds:02d}", end="", flush=True)

        if remaining > 0:
            time.sleep(1)
    print()

    end_time = time.time()
    elapsed = end_time - start_time
    elapsed_minutes = elapsed / 60.0

    if session_type == 'work':
        if not stop_script:
            work_cycles_completed += 1
        total_work_time += elapsed
        log_event("work_complete", elapsed_minutes)
    else:
        total_break_time += elapsed
        if session_type == 'long_break':
            log_event("break_complete", elapsed_minutes, "Long break completed")
        else:
            log_event("break_complete", elapsed_minutes)

def main():
    # Set up logging first
    setup_logging()

    print("\033[1;31m██████╗    ██╗          █████╗     ████████╗    ██╗    ███╗   ███╗    ███████╗")
    print("██╔════╝    ██║         ██╔══██╗    ╚══██╔══╝    ██║    ████╗ ████║    ██╔════╝")
    print("██║         ██║         ███████║       ██║       ██║    ██╔████╔██║    █████╗")
    print("██║         ██║         ██╔══██║       ██║       ██║    ██║╚██╔╝██║    ██╔══╝")
    print("╚██████╗    ███████╗    ██║  ██║       ██║       ██║    ██║ ╚═╝ ██║    ███████╗")
    print(" ╚═════╝    ╚══════╝    ╚═╝  ╚═╝       ╚═╝       ╚═╝    ╚═╝     ╚═╝    ╚══════╝\033[0m")
    print("\033[1;34mC   L   A   T   I   M   E      P   R   O   D   U   C   T   I   V   I   T   Y       T   O   O   L\033[0m   \033[1;31m(Version 1.00)\033[0m")
    author = "🛡️ By Joshua M Clatney (Clats97) - Ethical Pentesting Enthusiast 🛡️"
    print(author + "\n[Pomodoro Timer]\nStrategic Pauses, Sustained Success\n")

    log_event("custom", message="ClaTime application started")
    input("Press Enter to start the Pomodoro timer. Press Enter again at any time to stop.\n")

    listener = threading.Thread(target=wait_for_enter, daemon=True)
    listener.start()

    WORK_TEXT = r"""
 __          __   ____    _____    _  __  _ 
 \ \        / /  / __ \  |  __ \  | |/ / | |
  \ \  /\  / /  | |  | | | |__) | | ' /  | |
   \ \/  \/ /   | |  | | |  _  /  |  <   | |
    \  /\  /    | |__| | | | \ \  | . \  |_|
     \/  \/      \____/  |_|  \_\ |_|\_\ (_)

"""

    BREAK_TEXT = r"""
 ____    _____    ______              _  __  _ 
 |  _ \  |  __ \  |  ____|     /\     | |/ / | |
 | |_) | | |__) | | |__       /  \    | ' /  | |
 |  _ <  |  _  /  |  __|     / /\ \   |  <   | |
 | |_) | | | \ \  | |____   / ____ \  | . \  |_|
 |____/  |_|  \_\ |______| /_/    \_\ |_|\_\ (_
                                                                                                            
"""

    LONG_BREAK_TEXT = r"""
  _         ____    _   _    _____         ____    _____    ______              _  __  _ 
 | |       / __ \  | \ | |  / ____|       |  _ \  |  __ \  |  ____|     /\     | |/ / | |
 | |      | |  | | |  \| | | |  __        | |_) | | |__) | | |__       /  \    | ' /  | |
 | |      | |  | | | . ` | | | |_ |       |  _ <  |  _  /  |  __|     / /\ \   |  <   | |
 | |____  | |__| | | |\  | | |__| |       | |_) | | | \ \  | |____   / ____ \  | . \  |_|
 |______|  \____/  |_| \_|  \_____|       |____/  |_|  \_\ |______| /_/    \_\ |_|\_\ (_)
"""

    # Continuous loop until user stops
    while not stop_script:
        # Each "round" has 4 work/break cycles, then 1 long break
        for _ in range(4):
            if stop_script:
                break

            #Work time
            print(WORK_TEXT)
            countdown(30 * 60, "Time remaining:", "work")  # 30 minutes

            if stop_script:
                break

            #Regular break
            print(BREAK_TEXT)
            countdown(5 * 60, "Break Time remaining:", "break")  # 5 minutes

        if stop_script:
            break

        #Long break
        print(LONG_BREAK_TEXT)
        countdown(20 * 60, "Long Break Time remaining:", "long_break")  # 20 minutes

    # After user exits, log is created
    log_results()

if __name__ == "__main__":
    main()