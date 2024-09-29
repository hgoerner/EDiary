import datetime
from PIL import Image, ImageTk
import cv2
import folium
import tkinter as tk
from tkinter import filedialog
import csv


# Basis-Klasse für Einträge
class Entry:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        filename = f"{self.title}_{self.timestamp}.txt"
        with open(filename, "w") as file:
            file.write(f"Title: {self.title}\n")
            file.write(f"Date: {self.timestamp}\n")
            file.write(f"Content:\n{self.content}\n")
        print(f"Entry '{self.title}' saved successfully.")

    def display(self):
        print(f"Title: {self.title}")
        print(f"Date: {self.timestamp}")
        print(f"Content:\n{self.content}")


# Unterklasse für Bild-Einträge
class PictureEntry(Entry):
    def __init__(self, title, content, image_path):
        super().__init__(title, content)
        self.image_path = image_path

    def display_image(self):
        try:
            img = Image.open(self.image_path)
            img.show()
            print(f"Image '{self.image_path}' displayed.")
        except FileNotFoundError:
            print("Image not found.")

    def save(self):
        super().save()
        print(f"PictureEntry '{self.title}' with image '{self.image_path}' saved.")


# Unterklasse für Video-Einträge
class VideoEntry(Entry):
    def __init__(self, title, content, video_path):
        super().__init__(title, content)
        self.video_path = video_path

    def play_video(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"Error opening video file {self.video_path}")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow("Video", frame)
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def save(self):
        super().save()
        print(f"VideoEntry '{self.title}' with video '{self.video_path}' saved.")


# Klasse für Karten (Geotagging)
class MapEntry(Entry):
    def __init__(self, title, content, lat, lon, location_name):
        super().__init__(title, content)
        self.lat = lat
        self.lon = lon
        self.location_name = location_name

    def create_map(self):
        m = folium.Map(location=[self.lat, self.lon], zoom_start=12)
        folium.Marker([self.lat, self.lon], popup=self.location_name).add_to(m)
        m.save(f"{self.location_name}_map.html")
        print(f"Map for {self.location_name} saved as {self.location_name}_map.html.")

    def save(self):
        super().save()
        print(f"MapEntry '{self.title}' with location '{self.location_name}' saved.")


# Klasse zur Verwaltung des Tagebuchs
class TravelDiary:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.save()

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
        self.label.config(image=img_tk)
        self.label.image = img_tk

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
    picture_entry.display_image()

    # Video-Eintrag erstellen
    video_entry = VideoEntry("Paris Video", "Short clip from the trip.", "paris_video.mp4")
    diary.add_entry(video_entry)
    video_entry.play_video()

    # Karten-Eintrag erstellen
    map_entry = MapEntry("Map of Eiffel Tower", "Location of the Eiffel Tower.", 48.8584, 2.2945, "Eiffel Tower")
    diary.add_entry(map_entry)
    map_entry.create_map()

    # Alle Einträge anzeigen
    diary.show_entries()

    # Image Viewer starten (optional)
    # viewer = ImageViewer()
    # viewer.run()
