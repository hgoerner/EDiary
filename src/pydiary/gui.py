import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from dotenv import load_dotenv
from pydiary.pydiary import Entry, MapEntry, PictureEntry, VideoEntry
from pydiary.utils import add_qmd_header, has_header

# Load environment variables from .env file
load_dotenv()


class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Diary")
        # Load environment variables from .env file
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        print(self.api_key)

        if self.api_key is None:
            raise ValueError(
                "API key not found! Make sure it's set as an environment variable with -setx OPENWEATHERMAP_API_KEY ~your_actual_api_key~"
            )

        self.city_name = None

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

        # Add Weather Button
        self.add_weather_button = tk.Button(self.buttons_frame, text="Fetch Weather", command=self.add_weather)
        self.add_weather_button.grid(row=0, column=3, padx=5)

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

    def get_weather(self, city_name):
        """Fetch weather data including temperature, description, and icon URL."""
        try:
            # Fetch weather data
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            weather_data = response.json()

            if response.status_code != 200:
                return f"Error: {weather_data['message']}" if weather_data.get("message") else "Weather data could not be fetched."

            # Extract temperature, description, and icon code
            temp = weather_data["main"]["temp"]
            desc = weather_data["weather"][0]["description"].capitalize()
            icon_code = weather_data["weather"][0]["icon"]

            # Construct the icon URL
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

            # Format the weather information
            weather_info = f"Weather in {city_name}: {temp}°C, {desc}\n"
            weather_info += f"![Weather Icon]({icon_url})"  # Markdown format for embedding images

            return weather_info

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"

    def add_weather(self):
        """Prompt the user to enter a city name, then fetch weather data."""
        if city_name := simpledialog.askstring("City Name", "Enter the name of the city:"):
            # Fetch weather data and the icon image
            weather_info = self.get_weather(city_name)

            # Insert the weather info into the text box (only the text)
            self.content_text.insert(tk.END, f"\n\n{weather_info}\n")

            messagebox.showinfo("Weather Added", f"Weather data for {city_name} added.")
        else:
            messagebox.showerror("Error", "City name is required.")

    def add_picture(self):
        if file_path := filedialog.askopenfilename(
            title="Select Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],
        ):
            self.image_path = file_path
            messagebox.showinfo("Picture Selected", f"Picture selected: {os.path.basename(file_path)}")

    def add_video(self):
        if file_path := filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")],
        ):
            self.video_path = file_path
            messagebox.showinfo("Video Selected", f"Video selected: {os.path.basename(file_path)}")

    def add_gpx_data(self):
        if file_path := filedialog.askopenfilename(
            title="Select GPX File",
            filetypes=[("GPX Files", "*.gpx")],
        ):
            self.gpx_file = file_path
            messagebox.showinfo("GPX File Selected", f"GPX file selected: {os.path.basename(file_path)}")

    def get_entry_titles(self):
        # Read entries from the QMD file and return a list of entry titles
        if os.path.exists(self.qmd_file):
            titles = []
            with open(self.qmd_file, "r", encoding="utf-8") as f:
                titles.extend(line.strip()[2:] for line in f if line.startswith("# "))
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

        with open(self.qmd_file, "w", encoding="utf-8") as f:
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


def run_gui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
