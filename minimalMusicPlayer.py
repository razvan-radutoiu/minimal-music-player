import random
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
import os
from pygame import mixer

songs_list = []
song_labels = []
current_song_index = 0
song_duration = 0
global dur_start


def select_folder():
    folder_path = filedialog.askdirectory()
    load_music(folder_path)


def load_music(folder_path):
    mixer.init()
    global songs_list, current_song_index
    songs_list.clear()
    current_song_index = 0

    for filename, index in zip(
        os.listdir(folder_path), range(len(os.listdir(folder_path)))
    ):
        if (
            filename.endswith(".mp3")
            or filename.endswith(".ogg")
            or filename.endswith(".wav")
        ):
            song_name = filename
            song_path = os.path.join(folder_path, filename)
            mixer.music.load(song_path)
            songs_list.append(song_path)

            song_label = ctk.CTkLabel(song_listbox, text=song_name, cursor="hand2")
            song_label.pack(anchor=ctk.CENTER)
            song_label.bind("<Button-1>", lambda event, path=song_path: play_song(path))
            song_label.bind(
                "<Button-1>", lambda event, path=song_path: update_song(path)
            )
            song_label.bind(
                "<Enter>",
                lambda event, label=song_label: label.configure(fg_color="teal"),
            )
            song_label.bind(
                "<Leave>",
                lambda event, label=song_label: label.configure(
                    fg_color="transparent", underline=False
                ),
            )
            song_labels.append(song_label)


def play_music():
    mixer.music.play()


def play_song(song):
    mixer.music.load(song)
    global song_duration
    song_obj = mixer.Sound(song)
    song_duration = song_obj.get_length()
    mixer.music.play()
    song_progress()


pause = False


def pause_music():
    global pause
    if pause == False:
        mixer.music.pause()
        pause = True
    else:
        mixer.music.unpause()
        pause = False


def update_song(song_path):
    song_name = os.path.basename(song_path)
    current_song_label.configure(text=f"Currently Playing: {song_name}")


def update_volume(value):
    volume = int(value) / 100.0
    mixer.music.set_volume(volume)
    volume_label.configure(text=f"Volume: {int(volume * 100)}%")


def play_next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs_list)
    next_song = songs_list[current_song_index]
    play_song(next_song)


def play_prev_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs_list)
    prev_song = songs_list[current_song_index]
    play_song(prev_song)


def song_progress():
    current_position = mixer.music.get_pos() / 1000
    progress = (current_position / song_duration) * 100
    progressbar["value"] = progress

    # Calculate current position in minutes and seconds
    minutes = int(current_position // 60)
    seconds = int(current_position % 60)
    current_position_text = f"{minutes:02d}:{seconds:02d}"

    # Update the timestamp labels
    current_position_label.configure(text=current_position_text)
    total_duration_label.configure(text=format_duration(song_duration))

    root.after(500, song_progress)


def format_duration(duration):
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    return f"{minutes:02d}:{seconds:02d}"


# ------------------------- GUI

root = ctk.CTk()
root.geometry("1000x800")
root.title("Finally a good Music Player:||")

title_label = ctk.CTkLabel(
    root,
    text="Finally a good Music Player™",
    font=ctk.CTkFont(size=30, weight="bold"),
)
title_label.pack(padx=10, pady=(40, 20))

select_folder_button = ctk.CTkButton(
    root, text="♫ Add music +", width=500, command=select_folder
)
select_folder_button.pack(pady=20)

# play_music_button = ctk.CTkButton(root, text="Play", width=200, command=play_music)
# play_music_button.pack(pady=10)

pause_music_button = ctk.CTkButton(
    root, text="▶ Play/Pause", width=200, command=pause_music
)
pause_music_button.pack(pady=5)

song_listbox = ctk.CTkScrollableFrame(master=root, width=600, height=450)
song_listbox.pack(fill=ctk.NONE, expand=True)

current_song_label = ctk.CTkLabel(root, text="Currently Playing: None")
current_song_label.pack(pady=0)

volume_label = ctk.CTkLabel(root, text="Volume: 50%")
volume_label.pack(pady=0)

volume_slider = ctk.CTkSlider(root, from_=0, to=100, command=update_volume)
volume_slider.set(50)  # Initial volume value (50%)
volume_slider.pack(pady=3)

progressbar = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
progressbar.pack(pady=5)

current_position_label = ctk.CTkLabel(root, text="00:00")
current_position_label.pack(side=tk.LEFT, padx=(650, 70))

total_duration_label = ctk.CTkLabel(root, text="00:00")
total_duration_label.pack(side=tk.RIGHT, padx=(20, 650))

root.bind("<Right>", lambda event: play_next_song())
root.bind("<Left>", lambda event: play_prev_song())

root.mainloop()
