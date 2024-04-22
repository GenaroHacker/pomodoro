import time
import datetime
from playsound import playsound
from tqdm import tqdm

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None
        self.running = False
        self.progress = None

    def start(self, desc):
        self.start_time = time.time()
        self.running = True
        self.progress = tqdm(total=self.duration, bar_format='{desc}: {percentage:3.0f}%|{bar}| {elapsed}<{remaining}', desc=desc, colour='blue' if 'Focus' in desc else 'magenta')

    def update_progress(self):
        elapsed_time = time.time() - self.start_time
        self.progress.n = min(int(elapsed_time), self.duration)
        self.progress.refresh()

    def stop_progress(self):
        self.progress.n = self.duration
        self.progress.refresh()
        self.progress.close()

    def is_finished(self):
        return time.time() - self.start_time >= self.duration

class PomodoroManager:
    def __init__(self, focus_duration=1500, short_break=300, long_break=600):
        self.focus_duration = focus_duration
        self.short_break = short_break
        self.long_break = long_break
        self.current_round = 0  # Counting focus periods
        self.timer = Timer(self.focus_duration)
        self.notifier = Notifier()
        self.state = 'focus'  # Possible states: 'focus', 'short_break', 'long_break'

    def run(self):
        self.notifier.notify("Pomodoro session started.", sound="session_start.wav")
        while self.current_round <= 5:
            if self.state == 'focus':
                self.timer.start("Focus Period")
                self.current_round += 1
            elif self.state == 'short_break':
                self.timer.start("Short Break")
            elif self.state == 'long_break':
                self.timer.start("Long Break")

            while not self.timer.is_finished():
                self.timer.update_progress()
                time.sleep(1)

            self.timer.stop_progress()
            self.change_state()

    def change_state(self):
        if self.current_round < 4 and self.state == 'focus':
            self.state = 'short_break'
            self.timer = Timer(self.short_break)
            self.notifier.notify("Starting short break.", sound="break_start.wav")
        elif self.current_round == 4 and self.state == 'focus':
            self.state = 'long_break'
            self.timer = Timer(self.long_break)
            self.notifier.notify("Starting long break.", sound="long_break_start.wav")
        elif self.current_round == 5 and self.state == 'focus':
            self.notifier.notify("Pomodoro session completed.", sound="session_end.wav")
            exit()  # End the program after the last focus session
        else:
            self.state = 'focus'
            self.timer = Timer(self.focus_duration)
            self.notifier.notify("Starting focus period.", sound="focus_start.wav")

class Notifier:
    def notify(self, message, sound=None):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}")
        if sound:
            playsound(sound)

if __name__ == "__main__":
    manager = PomodoroManager()
    manager.run()

