import openai
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

