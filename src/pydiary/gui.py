# src/pydiary/gui.py

import tkinter as tk
from tkinter import messagebox, filedialog
from pydiary.pydiary import Entry, PictureEntry, VideoEntry, MapEntry
import os


class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Diary")

        # Initialize variables
        self.image_path = None
        self.video_path = None
        self.lat = None
        self.lon = None
        self.location_name = None

        # Title Label and Entry
        self.title_label = tk.Label(root, text="Title:")
        self.title_label.pack(pady=5)
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack(pady=5)

        # Content Label and Text Area
        self.content_label = tk.Label(root, text="Content:")
        self.content_label.pack(pady=5)
        self.content_text = tk.Text(root, height=10, width=50)
        self.content_text.pack(pady=5)

        # Buttons Frame
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        # Add Picture Button
        self.add_picture_button = tk.Button(self.buttons_frame, text="Add Picture", command=self.add_picture)
        self.add_picture_button.grid(row=0, column=0, padx=5)

        # Add Video Button
        self.add_video_button = tk.Button(self.buttons_frame, text="Add Video", command=self.add_video)
        self.add_video_button.grid(row=0, column=1, padx=5)

        # Add Map Data Button
        self.add_map_button = tk.Button(self.buttons_frame, text="Add Map Data", command=self.add_map_data)
        self.add_map_button.grid(row=0, column=2, padx=5)

        # Save Button
        self.save_button = tk.Button(root, text="Save Entry", command=self.save_entry)
        self.save_button.pack(pady=20)

    def add_picture(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(title="Select Picture", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Picture Selected", f"Picture selected: {os.path.basename(file_path)}")

    def add_video(self):
        # Open file dialog to select a video
        file_path = filedialog.askopenfilename(title="Select Video", filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_path:
            self.video_path = file_path
            messagebox.showinfo("Video Selected", f"Video selected: {os.path.basename(file_path)}")

    def add_map_data(self):
        # Create a new window to input map data
        map_window = tk.Toplevel(self.root)
        map_window.title("Add Map Data")

        # Latitude Entry
        lat_label = tk.Label(map_window, text="Latitude:")
        lat_label.pack(pady=5)
        lat_entry = tk.Entry(map_window, width=30)
        lat_entry.pack(pady=5)

        # Longitude Entry
        lon_label = tk.Label(map_window, text="Longitude:")
        lon_label.pack(pady=5)
        lon_entry = tk.Entry(map_window, width=30)
        lon_entry.pack(pady=5)

        # Location Name Entry
        loc_label = tk.Label(map_window, text="Location Name:")
        loc_label.pack(pady=5)
        loc_entry = tk.Entry(map_window, width=30)
        loc_entry.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(
            map_window, text="Add Map Data", command=lambda: self.save_map_data(map_window, lat_entry, lon_entry, loc_entry)
        )
        submit_button.pack(pady=10)

    def save_map_data(self, map_window, lat_entry, lon_entry, loc_entry):
        try:
            self.lat = float(lat_entry.get())
            self.lon = float(lon_entry.get())
            self.location_name = loc_entry.get()

            if not self.location_name:
                messagebox.showerror("Error", "Location name is required.")
                return

            messagebox.showinfo("Map Data Added", f"Map data for {self.location_name} added.")
            map_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid latitude or longitude. Please enter valid numbers.")

    def save_entry(self):
        # Get the values from the GUI fields
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()

        # Validation
        if not title or not content:
            messagebox.showerror("Error", "Both title and content are required!")

    # Main GUI loop function


def run_gui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
