import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pydiary.pydiary import Entry, PictureEntry, VideoEntry, MapEntry
import os
from pydiary.utils import has_header, add_qmd_header


class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Diary")

        # Initialize variables
        self.entries = []  # Store entries
        self.image_path = None
        self.video_path = None
        self.gpx_file = None
        self.image_alignment = tk.StringVar(value="left")  # Default value is left
        self.qmd_file = "first_diary.qmd"

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

        # Add GPX Map Data Button
        self.add_map_button = tk.Button(self.buttons_frame, text="Add GPX Map", command=self.add_gpx_data)
        self.add_map_button.grid(row=0, column=2, padx=5)

        # Alignment Selection (Radio Buttons for Left/Right)
        self.align_label = tk.Label(root, text="Image Alignment:")
        self.align_label.pack(pady=5)

        # Radio buttons for alignment (left or right)
        self.left_align_radio = tk.Radiobutton(root, text="Left", variable=self.image_alignment, value="left")
        self.left_align_radio.pack(pady=5, anchor="w")
        self.right_align_radio = tk.Radiobutton(root, text="Right", variable=self.image_alignment, value="right")
        self.right_align_radio.pack(pady=5, anchor="w")

        # Save Button
        self.save_button = tk.Button(root, text="Save Entry", command=self.save_entry)
        self.save_button.pack(pady=20)

        # Dropdown for selecting an entry
        self.entry_selection_label = tk.Label(root, text="Select an Entry:")
        self.entry_selection_label.pack(pady=5)

        self.entry_selection = ttk.Combobox(root, values=self.get_entry_titles())
        self.entry_selection.pack(pady=5)

        # Edit and Delete Buttons
        self.edit_button = tk.Button(root, text="Edit Entry", command=self.edit_entry)
        self.edit_button.pack(pady=5)
        self.delete_button = tk.Button(root, text="Delete Entry", command=self.delete_entry)
        self.delete_button.pack(pady=5)

    def add_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
        )
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Picture Selected", f"Picture selected: {os.path.basename(file_path)}")

    def add_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")],
        )
        if file_path:
            self.video_path = file_path
            messagebox.showinfo("Video Selected", f"Video selected: {os.path.basename(file_path)}")

    def add_gpx_data(self):
        file_path = filedialog.askopenfilename(
            title="Select GPX File",
            filetypes=[("GPX Files", "*.gpx")],
        )
        if file_path:
            self.gpx_file = file_path
            messagebox.showinfo("GPX File Selected", f"GPX file selected: {os.path.basename(file_path)}")

    def get_entry_titles(self):
        # Read entries from the QMD file and return a list of entry titles
        if os.path.exists(self.qmd_file):
            titles = []
            with open(self.qmd_file, "r") as f:
                for line in f:
                    if line.startswith("# "):  # Assuming each entry starts with '# Title'
                        titles.append(line.strip()[2:])  # Strip off the '# ' part
            return titles
        return []

    def save_entry(self):
        # Get the values from the GUI fields
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        alignment = self.image_alignment.get()

        if not title or not content:
            messagebox.showerror("Error", "Both title and content are required!")
            return

        # Check if the QMD file exists and add the header if it's missing
        if not os.path.exists(self.qmd_file) or not has_header(self.qmd_file):
            add_qmd_header(self.qmd_file)

        entry = None
        if self.image_path:
            entry = PictureEntry(title, content, self.image_path, align=alignment)
        elif self.video_path:
            entry = VideoEntry(title, content, self.video_path)
        elif self.gpx_file:
            entry = MapEntry(title, content, self.gpx_file)
        else:
            entry = Entry(title, content)

        entry.save(self.qmd_file)

        # Update the dropdown with new entry
        self.entry_selection["values"] = self.get_entry_titles()

        # Clear fields
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.image_path = None
        self.video_path = None
        self.gpx_file = None

        messagebox.showinfo("Success", f"Entry '{title}' saved successfully!")

    def delete_entry(self):
        selected_entry = self.entry_selection.get()
        if not selected_entry:
            messagebox.showerror("Error", "No entry selected!")
            return

        # Read and rewrite QMD file without the selected entry
        new_content = []
        with open(self.qmd_file, "r", encoding="utf-8") as f:
            skip = False
            for line in f:
                if line.startswith(f"# {selected_entry}"):
                    skip = True
                elif skip and line.startswith("# "):
                    skip = False
                if not skip:
                    new_content.append(line)

        with open(self.qmd_file, "w") as f:
            f.writelines(new_content)

        # Update the dropdown
        self.entry_selection["values"] = self.get_entry_titles()

        messagebox.showinfo("Success", f"Entry '{selected_entry}' deleted successfully!")

    def edit_entry(self):
        selected_entry = self.entry_selection.get()
        if not selected_entry:
            messagebox.showerror("Error", "No entry selected!")
            return

        # Load the selected entry's content into the GUI fields for editing
        entry_found = False
        with open(self.qmd_file, "r", encoding="utf-8") as f:
            content = []
            for line in f:
                if line.startswith(f"# {selected_entry}"):
                    entry_found = True
                    continue
                elif entry_found and line.startswith("# "):
                    break
                if entry_found:
                    content.append(line)

        if entry_found:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, selected_entry)

            self.content_text.delete("1.0", tk.END)
            self.content_text.insert("1.0", "".join(content))
        else:
            messagebox.showerror("Error", f"Entry '{selected_entry}' not found!")

    # Main GUI


def run_gui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
