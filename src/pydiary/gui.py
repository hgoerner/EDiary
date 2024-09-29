# src/pydiary/gui.py

import tkinter as tk
from tkinter import messagebox
from pydiary.pydiary import Entry


class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Diary")

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

        # Save Button
        self.save_button = tk.Button(root, text="Save Entry", command=self.save_entry)
        self.save_button.pack(pady=20)

    def save_entry(self):
        # Get the values from the GUI fields
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END)

        # Validation
        if not title or not content.strip():
            messagebox.showerror("Error", "Both title and content are required!")
            return

        # Create an Entry instance and save it
        entry = Entry(title, content)
        try:
            file_path = entry.save()  # Save the entry to the diary_entries directory
            messagebox.showinfo("Success", f"Entry saved to {file_path}")
            # Clear the fields after saving
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry: {str(e)}")


# Main GUI loop function
def run_gui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
