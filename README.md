# ClaTime
A simple, Python based pomodoro timer / productivity tool. Perfect for hard workers that want to increase productivity and relieve stress.

ClaTime is a command-line Pomodoro timer application designed to enhance productivity through structured work-break cycles. Created by Joshua M Clatney (Clats97), this tool implements the Pomodoro Technique, a time management method that uses timed intervals of focused work followed by breaks.

**Features**

**Structured Time Management: Implements the classic Pomodoro technique with:**

- 30-minute work sessions
- 5-minute short breaks
- 20-minute long breaks after four work cycles

**Visual Feedback: ASCII art displays for different session types:**

- Work sessions
- Break sessions
- Long break sessions

**Comprehensive Logging: Automatic session tracking with detailed logs including:**

- Session start and end times
- Duration of work and break periods
- Total work cycles completed
- Summary statistics

**Technical Details**

**Core Components**

1. **Logging System**
- Logs are saved to `clatime_log.txt`
- Includes timestamp, event type, and duration information
- Session starts and ends
- Work periods
- Break periods
- Summary statistics

2. **Timer Functions**
-`countdown()`: Core timing mechanism that:
- Displays real-time countdown
- Tracks session duration
- Updates global statistics
- Handles user interruptions


 3. **Session Management**
- Implements full Pomodoro cycles:
- 4 work/break cycles followed by a long break
- Maintains session statistics
- Handles graceful interruption

4. **User Interface**
- Clean command-line interface with:
- ASCII art headers
- Real-time countdown display
- Session type indicators
- Simple Enter key controls

**Key Variables**
- `total_work_time`: Tracks cumulative work duration
- `total_break_time`: Tracks cumulative break duration
- `work_cycles_completed`: Counts finished work sessions
- `stop_script`: Controls program termination

**Usage**

**Starting the Application**

1. Run the script
2. Press Enter to begin the Pomodoro timer
3. Press Enter again at any time to stop the session

**Session Flow**

1. Work Session (30 minutes)
2. Short Break (5 minutes)
3. Repeat steps 1-2 four times
4. Long Break (20 minutes)
5. Cycle repeats until user exits

**Logging**

- All sessions are automatically logged
- Log file (`clatime_log.txt`) includes:
- Timestamp for each event
- Session durations
- End-of-session summary

**Requirements**

- Python 3.x
- Standard library modules:
- `time`
- `threading`
- `logging`
- `datetime`

**Implementation Notes**

**Threading**

- Uses a separate thread to monitor for user input
- Allows for clean program termination
- Prevents blocking during countdown

**Error Handling**

- Graceful session termination
- Proper cleanup of resources
- Complete session logging even on early exit

**Session Statistics**

- Tracks multiple metrics:
- Number of completed work cycles
- Total work time
- Total break time
- Session duration

**Author**

Joshua M Clatney (Clats97)
Ethical Pentesting Enthusiast

Released under the Apache 2.0 License. This project is open source. Modify it, improve it, share it, use it, or whatever!

*Copyright 2025 Joshua M Clatney (Clats97)*

