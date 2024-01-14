import cv2
import os 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def upscale_image(input_path, output_path, output_name, new_width, new_height):
    image = cv2.imread(input_path)
    if image is None:
        messagebox.showerror("Error", "Image not found.")
        return

    # Extract the extension from the input file
    _, ext = os.path.splitext(input_path)
    if not ext:
        messagebox.showerror("Error", "Invalid file extension.")
        return

    # Construct the full output path with the same extension as the input image
    full_output_path = os.path.join(output_path, f"{output_name}{ext}")

    upscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(full_output_path, upscaled_image)
    messagebox.showinfo("Success", f"Image upscaled and saved to {full_output_path}")
def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, foldername)

root = tk.Tk()
root.title("Image Upscaler")

# Input File Selection
tk.Label(root, text="Input Image:").grid(row=0, column=0, sticky=tk.W)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(input_entry)).grid(row=0, column=2)

# Output Folder Selection
tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky=tk.W)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(output_entry)).grid(row=1, column=2)

# Output Image Name
tk.Label(root, text="Output Image Name:").grid(row=2, column=0, sticky=tk.W)
output_name_entry = tk.Entry(root, width=50)
output_name_entry.grid(row=2, column=1)

# Resolution Fields
tk.Label(root, text="Width:").grid(row=3, column=0, sticky=tk.W)
width_entry = tk.Entry(root, width=10)
width_entry.grid(row=3, column=1, sticky=tk.W)

tk.Label(root, text="Height:").grid(row=4, column=0, sticky=tk.W)
height_entry = tk.Entry(root, width=10)
height_entry.grid(row=4, column=1, sticky=tk.W)

# Upscale Button
upscale_button = tk.Button(root, text="Upscale Image", command=lambda: upscale_image(
    input_entry.get(), output_entry.get(), output_name_entry.get(), int(width_entry.get()), int(height_entry.get())))
upscale_button.grid(row=5, column=1, sticky=tk.W)

root.mainloop()
