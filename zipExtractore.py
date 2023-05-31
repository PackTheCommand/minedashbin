import tkinter as tk
from tkinter import font

root = tk.Tk()
text_widget = tk.Text(root)
text_widget.pack()

# Create a custom font with a wavy underline
custom_font = font.Font(underline=True)
custom_font.configure(family="Arial", size=12, weight="normal",slant="italic")

# Apply the custom font to the text widget
text_widget.configure(font=custom_font)

# Insert some text
text_widget.insert(tk.END, "This is some wavy underlined text.")

root.mainloop()