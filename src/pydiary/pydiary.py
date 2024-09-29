import datetime
from PIL import Image, ImageTk
import cv2
import folium
import tkinter as tk
from tkinter import filedialog
import os
import gpxpy
import folium
import os
import shutil


class Entry:
    # Class variable to keep track of the last saved date
    last_saved_date = None

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")  # Only store the date (no time)

    def save(self, qmd_file="my_hiking_diary.qmd"):
        # Open the Quarto Markdown file in append mode
        with open(qmd_file, "a", encoding="utf-8") as f:
            # Check if the date needs to be written (i.e., if it's a new day)
            if Entry.last_saved_date != self.date:
                f.write(f"**Date**: {self.date}\n\n")
                Entry.last_saved_date = self.date  # Update the last saved date

            # Write the entry title and content
            f.write(f"# {self.title}\n\n")
            f.write(f"{self.content}\n\n")
        print(f"Entry '{self.title}' saved to {qmd_file}.")

    def display(self):
        print(f"Title: {self.title}")
        print(f"Date: {self.date}")
        print(f"Content:\n{self.content}")


class PictureEntry(Entry):
    def __init__(self, title, content, image_path, align="left"):
        super().__init__(title, content)
        self.image_path = image_path
        self.align = align  # 'left' or 'right'

    def save(self, qmd_file="my_hiking_diary.qmd"):
        super().save(qmd_file)

        # Ensure the image is copied to the same directory as the .qmd file
        qmd_dir = os.path.dirname(qmd_file)
        image_filename = os.path.basename(self.image_path)
        target_image_path = os.path.join(qmd_dir, image_filename)

        if not os.path.exists(target_image_path):
            # Copy the image to the same directory as the .qmd file
            shutil.copy(self.image_path, target_image_path)

        # Write the image and text in a float layout (text to the left or right of the image)
        with open(qmd_file, "a", encoding="utf-8") as f:
            f.write(
                f'<div style="display: flex; flex-direction: {"row-reverse" if self.align == "right" else "row"}; align-items: center;">\n'
            )
            f.write(f'<img src="{image_filename}" alt="{self.title}" style="max-width: 50%; height: auto; margin: 10px;">\n')
            f.write(f'<p style="max-width: 50%;">{self.content}</p>\n')
            f.write("</div>\n\n")

        print(f"PictureEntry '{self.title}' with image '{self.image_path}' saved to {qmd_file}.")


# Unterklasse für Video-Einträge
class VideoEntry(Entry):
    def __init__(self, title, content, video_path):
        super().__init__(title, content)
        self.video_path = video_path

    def save(self, qmd_file="my_hiking_diary.qmd"):
        super().save(qmd_file)
        # Append a video link (or placeholder) to the .qmd file
        with open(qmd_file, "a", encoding="utf-8") as f:
            f.write(f"[Watch Video]({self.video_path})\n\n")
        print(f"VideoEntry '{self.title}' with video '{self.video_path}' saved to {qmd_file}.")

    def play_video(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error opening video file {self.video_path}")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()


# Klasse für Karten (Geotagging)


class MapEntry(Entry):
    def __init__(self, title, content, gpx_file):
        super().__init__(title, content)
        self.gpx_file = gpx_file

    def parse_gpx(self):
        # Parse the GPX file and extract coordinates
        # Open the file in binary mode to check for BOM
        with open(self.gpx_file, "rb") as file:
            content = file.read()

        # Check for BOM (Byte Order Mark) and strip it
        if content.startswith(b"\xef\xbb\xbf"):
            content = content[3:]

        # Decode the content and parse it
        content = content.decode("utf-8")
        gpx = gpxpy.parse(content)

        coords = []
        for track in gpx.tracks:
            for segment in track.segments:
                coords.extend((point.latitude, point.longitude) for point in segment.points)
        return coords

    def create_map(self):
        coords = self.parse_gpx()

        if not coords:
            print("No coordinates found in the GPX file.")
            return None

        # Create the folium map centered on the first coordinate
        m = folium.Map(location=coords[0], zoom_start=12)

        # Add the GPX route to the map
        folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(m)

        return m  # Return the folium map object

    def save(self, qmd_file="my_hiking_diary.qmd"):
        super().save(qmd_file)
        if folium_map := self.create_map():
            # Get the HTML representation of the map
            map_html = folium_map._repr_html_()

            # Write the map HTML directly to the QMD file for inline embedding
            with open(qmd_file, "a", encoding="utf-8") as f:
                f.write(map_html)

        print(f"MapEntry '{self.title}' with GPX file '{self.gpx_file}' saved to {qmd_file}.")


# Klasse zur Verwaltung des Tagebuchs
class TravelDiary:
    def __init__(self, qmd_file="first_vacation.qmd"):
        self.entries = []
        self.qmd_file = qmd_file  # Specify the Quarto file to store entries

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.save(self.qmd_file)

    def show_entries(self):
        for entry in self.entries:
            entry.display()


# GUI für die Bildanzeige (optional)
class ImageViewer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Travel Diary - Image Viewer")
        self.label = tk.Label(self.window)
        self.label.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename()
        img = Image.open(file_path)
        img = img.resize((300, 300))  # Bildgröße anpassen
        img_tk = ImageTk.PhotoImage(img)
        self.label.config(image=img_tk)  # type: ignore
        self.label.image = img_tk  # type: ignore # Keep a reference to avoid garbage collection
        self.label.configure(image=img_tk)  # type: ignore
        self.image_reference = img_tk  # Keep a reference to avoid garbage collection

    def run(self):
        button = tk.Button(self.window, text="Open Image", command=self.open_image)
        button.pack()
        self.window.mainloop()


# Beispiel für die Verwendung der Klassen
if __name__ == "__main__":
    # Tagebuch erstellen
    diary = TravelDiary()

    # Text-Eintrag erstellen
    text_entry = Entry("Trip to Paris", "Visited the Eiffel Tower. It was amazing!")
    diary.add_entry(text_entry)

    # Bild-Eintrag erstellen
    picture_entry = PictureEntry("Eiffel Tower", "Beautiful day at the Eiffel Tower.", "eiffel_tower.jpg")
    diary.add_entry(picture_entry)
    picture_entry.display_image()  # type: ignore

    # Video-Eintrag erstellen
    video_entry = VideoEntry("Paris Video", "Short clip from the trip.", "paris_video.mp4")
    diary.add_entry(video_entry)
    video_entry.play_video()

    # Karten-Eintrag erstellen
    map_entry = MapEntry("Map of Eiffel Tower", "Location of the Eiffel Tower.", 48.8584, 2.2945, "Eiffel Tower")  # type: ignore
    diary.add_entry(map_entry)
    map_entry.create_map()

    # Alle Einträge anzeigen
    diary.show_entries()

    # Image Viewer starten (optional)
    # viewer = ImageViewer()
    # viewer.run()
