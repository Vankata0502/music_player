import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry("500x325")
        self.root.directory = ''


        try:
            self.root.iconbitmap(resource_path("assets/play_button.ico"))
        except Exception:
            pass

        pygame.mixer.init()

        self.songs = []
        self.current_song = ""
        self.paused = False

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.organise_menu = tk.Menu(self.menubar, tearoff=False)
        self.organise_menu.add_command(label='Select Folder', command=self.load_music)
        self.menubar.add_cascade(label='Organise', menu=self.organise_menu)

        self.song_list = tk.Listbox(self.root, bg="pink", fg="black", width=100, height=15)
        self.song_list.pack()

        self.play_btn_image = tk.PhotoImage(file=resource_path("assets/play50.png"))
        self.pause_btn_image = tk.PhotoImage(file=resource_path("assets/pause50.png"))
        self.next_btn_image = tk.PhotoImage(file=resource_path("assets/next50.png"))
        self.previous_btn_image = tk.PhotoImage(file=resource_path("assets/back50.png"))

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        self.play_btn = tk.Button(self.control_frame, image=self.play_btn_image, borderwidth=0, command=self.play_music)
        self.pause_btn = tk.Button(self.control_frame, image=self.pause_btn_image, borderwidth=0,
                                   command=self.pause_music)
        self.next_btn = tk.Button(self.control_frame, image=self.next_btn_image, borderwidth=0, command=self.next_music)
        self.previous_btn = tk.Button(self.control_frame, image=self.previous_btn_image, borderwidth=0,
                                      command=self.previous_music)

        # Подредба в мрежа (Grid)
        self.previous_btn.grid(row=0, column=0, padx=7, pady=10)
        self.play_btn.grid(row=0, column=1, padx=7, pady=10)
        self.pause_btn.grid(row=0, column=2, padx=7, pady=10)
        self.next_btn.grid(row=0, column=3, padx=7, pady=10)

    def load_music(self):
        self.root.directory = filedialog.askdirectory()
        if not self.root.directory:
            return

        self.songs.clear()
        self.song_list.delete(0, tk.END)

        for song in os.listdir(self.root.directory):
            name, ext = os.path.splitext(song)
            if ext.lower() == '.mp3':
                self.songs.append(song)

        for song in self.songs:
            self.song_list.insert("end", song)

        if self.songs:
            self.song_list.selection_set(0)
            self.current_song = self.songs[self.song_list.curselection()[0]]

    def play_music(self):

        if not self.songs:
            return

        try:
            selected_index = self.song_list.curselection()[0]
            self.current_song = self.songs[selected_index]
        except IndexError:
            pass

        if not self.paused:
            try:
                full_path = os.path.join(self.root.directory, self.current_song)
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load song: {e}")
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def next_music(self):
        if not self.songs:
            return

        try:
            current_index = self.songs.index(self.current_song)
            next_index = current_index + 1

            if next_index >= len(self.songs):
                next_index = 0

            self.song_list.selection_clear(0, tk.END)
            self.song_list.selection_set(next_index)
            self.current_song = self.songs[next_index]

            self.paused = False
            self.play_music()
        except (IndexError, ValueError):
            pass

    def previous_music(self):
        if not self.songs:
            return

        try:
            current_index = self.songs.index(self.current_song)
            prev_index = current_index - 1

            if prev_index < 0:
                prev_index = len(self.songs) - 1

            self.song_list.selection_clear(0, tk.END)
            self.song_list.selection_set(prev_index)
            self.current_song = self.songs[prev_index]

            self.paused = False
            self.play_music()
        except (IndexError, ValueError):
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()