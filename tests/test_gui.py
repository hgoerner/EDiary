import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from pydiary.gui import DiaryApp

class TestDiaryApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = DiaryApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('pydiary.gui.filedialog.askopenfilename')
    @patch('pydiary.gui.messagebox.showinfo')
    def test_add_picture(self, mock_showinfo, mock_askopenfilename):
        mock_askopenfilename.return_value = "test_image.png"
        self.app.add_picture()
        self.assertEqual(self.app.image_path, "test_image.png")
        mock_showinfo.assert_called_with("Picture Selected", "Picture selected: test_image.png")

    @patch('pydiary.gui.filedialog.askopenfilename')
    @patch('pydiary.gui.messagebox.showinfo')
    def test_add_video(self, mock_showinfo, mock_askopenfilename):
        mock_askopenfilename.return_value = "test_video.mp4"
        self.app.add_video()
        self.assertEqual(self.app.video_path, "test_video.mp4")
        mock_showinfo.assert_called_with("Video Selected", "Video selected: test_video.mp4")

    @patch('pydiary.gui.filedialog.askopenfilename')
    @patch('pydiary.gui.messagebox.showinfo')
    def test_add_gpx_data(self, mock_showinfo, mock_askopenfilename):
        mock_askopenfilename.return_value = "test_data.gpx"
        self.app.add_gpx_data()
        self.assertEqual(self.app.gpx_file, "test_data.gpx")
        mock_showinfo.assert_called_with("GPX File Selected", "GPX file selected: test_data.gpx")

    @patch('pydiary.gui.messagebox.showerror')
    def test_save_entry_without_title_or_content(self, mock_showerror):
        self.app.title_entry.insert(0, "")
        self.app.content_text.insert("1.0", "")
        self.app.save_entry()
        mock_showerror.assert_called_with("Error", "Both title and content are required!")

    @patch('pydiary.gui.messagebox.showinfo')
    @patch('pydiary.gui.Entry.save')
    @patch('pydiary.gui.has_header', return_value=True)
    def test_save_entry_with_title_and_content(self, mock_has_header, mock_save, mock_showinfo):
        self.app.title_entry.insert(0, "Test Title")
        self.app.content_text.insert("1.0", "Test Content")
        self.app.save_entry()
        mock_save.assert_called_once()
        mock_showinfo.assert_called_with("Success", "Entry 'Test Title' saved successfully!")

    @patch('pydiary.gui.messagebox.showerror')
    def test_delete_entry_no_selection(self, mock_showerror):
        self.app.entry_selection.set("")
        self.app.delete_entry()
        mock_showerror.assert_called_with("Error", "No entry selected!")

    @patch('pydiary.gui.messagebox.showinfo')
    @patch('pydiary.gui.open', new_callable=unittest.mock.mock_open, read_data="# Test Entry\nContent") # type: ignore
    def test_delete_entry(self, mock_open, mock_showinfo):
        self.app.entry_selection.set("Test Entry")
        self.app.delete_entry()
        mock_showinfo.assert_called_with("Success", "Entry 'Test Entry' deleted successfully!")

    @patch('pydiary.gui.messagebox.showerror')
    def test_edit_entry_no_selection(self, mock_showerror):
        self.app.entry_selection.set("")
        self.app.edit_entry()
        mock_showerror.assert_called_with("Error", "No entry selected!")

    @patch('pydiary.gui.open', new_callable=unittest.mock.mock_open, read_data="# Test Entry\nContent") # type: ignore
    def test_edit_entry(self, mock_open):
        self.app.entry_selection.set("Test Entry")
        self.app.edit_entry()
        self.assertEqual(self.app.title_entry.get(), "Test Entry")
        self.assertEqual(self.app.content_text.get("1.0", tk.END).strip(), "Content")

if __name__ == '__main__':
    unittest.main()