import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

def upscale_image(input_path, output_path, target_resolution):
    try:
        image = Image.open(input_path)
        image = image.resize(target_resolution, Image.ANTIALIAS)
        image.save(output_path)
        result_label.config(text=f"Image upscaled and saved as '{output_path}'")
    except FileNotFoundError:
        result_label.config(text="Input file not found.")
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")

def browse_input_file():
    file_path = filedialog.askopenfilename()
    input_path_entry.delete(0, tk.END)
    input_path_entry.insert(0, file_path)

def browse_output_directory():
    output_directory = filedialog.askdirectory()
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, output_directory)

def upscale_button_clicked():
    input_path = input_path_entry.get()
    output_directory = output_path_entry.get()
    output_name = output_name_entry.get()
    try:
        width = int(target_width_entry.get())
        height = int(target_height_entry.get())
        target_resolution = (width, height)
        if not output_name:
            result_label.config(text="Please enter a valid output name.")
            return
        output_path = f"{output_directory}/{output_name}"
        upscale_image(input_path, output_path, target_resolution)
        # Clear input fields
        input_path_entry.delete(0, tk.END)
        output_name_entry.delete(0, tk.END)
        result_label.after(5000, clear_result)  # Clear result message after 5 seconds
    except ValueError:
        result_label.config(text="Invalid target resolution!")

def clear_result():
    result_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Image Upscaler")

# Create and pack GUI elements
input_label = tk.Label(root, text="Input Image:")
input_label.pack()
input_path_entry = tk.Entry(root, width=40)
input_path_entry.pack()
browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.pack()

output_label = tk.Label(root, text="Output Directory:")
output_label.pack()
output_path_entry = tk.Entry(root, width=40)
output_path_entry.pack()
browse_output_button = tk.Button(root, text="Browse", command=browse_output_directory)
browse_output_button.pack()

output_name_label = tk.Label(root, text="Output Image Name:")
output_name_label.pack()
output_name_entry = tk.Entry(root, width=40)
output_name_entry.pack()

resolution_label = tk.Label(root, text="Output Resolution:")
resolution_label.pack()
target_width_entry = tk.Entry(root, width=10)
target_width_entry.pack(side=tk.LEFT)
x_label = tk.Label(root, text="x")
x_label.pack(side=tk.LEFT)
target_height_entry = tk.Entry(root, width=10)
target_height_entry.pack(side=tk.LEFT)

upscale_button = tk.Button(root, text="Upscale Image", command=upscale_button_clicked)
upscale_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Start the GUI main loop
root.mainloop()
