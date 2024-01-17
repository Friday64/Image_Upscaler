import os
import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog, messagebox

def upscale_image_with_tensorflow(input_path, output_path, output_name, scale_factor):
    # Load the TensorFlow model
    model = tf.saved_model.load("C:/Users/Matthew/Desktop/FSRCNN_Tensorflow-master/models")

    # Read the image using OpenCV
    image = cv2.imread(input_path)
    if image is None:
        messagebox.showerror("Error", "Image not found.")
        return

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Normalize and expand image dimensions
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # Use the model to upscale the image
    upscaled_image = model(image)

    # Convert back to BGR and scale back pixel values
    upscaled_image = upscaled_image.numpy().squeeze() * 255
    upscaled_image = upscaled_image.astype(np.uint8)
    upscaled_image = cv2.cvtColor(upscaled_image, cv2.COLOR_RGB2BGR)

    # Extract the extension from the input file
    _, ext = os.path.splitext(input_path)
    if not ext:
        messagebox.showerror("Error", "Invalid file extension.")
        return

    # Construct the full output path with the same extension as the input image
    full_output_path = os.path.join(output_path, f"{output_name}{ext}")

    # Save the upscaled image
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

# Scale Factor Field
tk.Label(root, text="Scale Factor:").grid(row=3, column=0, sticky=tk.W)
scale_factor_entry = tk.Entry(root, width=10)
scale_factor_entry.grid(row=3, column=1, sticky=tk.W)

# Upscale Button
upscale_button = tk.Button(root, text="Upscale Image", command=lambda: upscale_image_with_tensorflow(
    input_entry.get(), output_entry.get(), output_name_entry.get(), int(scale_factor_entry.get())))
upscale_button.grid(row=4, column=1, sticky=tk.W)

root.mainloop()
