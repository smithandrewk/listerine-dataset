import matplotlib.pyplot as plt
import numpy as np
import torch
import time
import subprocess

# Load the data
X, y, bouts = torch.load('5_vectored/0/5.pt')  # 100 Hz 44k samples
X = X[::5]  # Downsample to 20 Hz
duration = len(X) / 20  # Duration in seconds

# Create time array for 20 Hz data
t = np.linspace(0, duration, len(X))

# Define the event times
event_time_in_video = 87.5  # Event time in the video (in seconds)
event_time_in_time_series = 71  # Event time in the time series (in seconds)

# Calculate the offset
time_offset = event_time_in_video - event_time_in_time_series

# Define the cropping parameters
crop_width = 1500  # Width of the cropped video
crop_height = 400  # Height of the cropped video
crop_x = 0  # X position of the crop
crop_y = 0  # Y position of the crop

# Create the plot
fig, ax = plt.subplots()

# Plot the time series data
ax.plot(t, X)
line, = ax.plot([], [], 'r-', lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
ax.set_ylim([-20, 20])

# Set x-axis ticks to every 2 seconds
ax.xaxis.set_major_locator(plt.MultipleLocator(2))

# Function to update the plot
def update_plot(current_time):
    line.set_data([current_time, current_time], [X.min(), X.max()])
    time_text.set_text(f'Time: {current_time:.2f}s')
    ax.set_xlim([current_time-20, current_time+20])
    plt.draw()

# Start mplayer subprocess with cropping
video_path = 'cohort_2_meeting_0.mp4'
mplayer_process = subprocess.Popen([
    'mplayer', '-slave', '-quiet', '-osdlevel', '3', 
    '-vf', f'crop={crop_width}:{crop_height}:{crop_x}:{crop_y}', video_path
], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Function to get current playback time from mplayer
def get_current_time():
    mplayer_process.stdin.write('get_time_pos\n')
    mplayer_process.stdin.flush()
    while True:
        line = mplayer_process.stdout.readline()
        if line.startswith('ANS_TIME_POSITION'):
            return float(line.split('=')[1].strip())

# Function to send a command to mplayer
def send_command(command):
    print(f"Sending command: {command}")
    mplayer_process.stdin.write(f'{command}\n')
    mplayer_process.stdin.flush()

# Function to handle key press events
def on_key_press(event):
    if event.key == ' ':
        send_command('pause')
        print('Toggled pause/play')

# Connect the key press event handler
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Synchronize plot with video
try:
    while True:
        current_time = get_current_time()
        if current_time is not None:
            adjusted_time = current_time - time_offset
            if adjusted_time >= 0:
                update_plot(adjusted_time)
            else:
                update_plot(0)
        plt.pause(0.05)  # Adjust as needed to match your frame rate
except KeyboardInterrupt:
    pass
finally:
    send_command('quit')
    mplayer_process.terminate()

plt.show()
