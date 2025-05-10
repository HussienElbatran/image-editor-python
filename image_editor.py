
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab

# Define global variables
WIDTH = 750
HEIGHT = 560
file_path = ""
pen_size = 3
pen_color = "black"
is_flipped = False
rotation_angle = 0

# Create main window
root = tk.Tk()
root.title("Image Editor")
root.geometry("750x600+300+110")
root.resizable(0, 0)

# Try to set an icon if available
try:
    icon = tk.PhotoImage(file='icon.png')
    root.iconphoto(False, icon)
except:
    pass  # Icon not found, continue without it

# The left frame to contain buttons and controls
left_frame = tk.Frame(root, width=200, height=600, bg="#f0f0f0")
left_frame.pack(side="left", fill="y")

# The right canvas for displaying the image
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.pack()

# Label
filter_label = tk.Label(left_frame, text="Select Filter:", bg="#f0f0f0", font=("Arial", 10, "bold"))
filter_label.pack(padx=10, pady=10)

# A list of filters
image_filters = ["Contour", "Black and White", "Blur", "Detail", "Emboss", "Edge Enhance", "Sharpen", "Smooth"]

# Combobox for the filters
filter_combobox = ttk.Combobox(left_frame, values=image_filters, width=15)
filter_combobox.pack(padx=10, pady=5)

# Function to open the image file
def open_image():
    global file_path, image, photo_image
    file_path = filedialog.askopenfilename(title="Open Image File", 
                                          filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        # Reset rotation and flip state when opening a new image
        global rotation_angle, is_flipped
        rotation_angle = 0
        is_flipped = False
        
        # Open and resize the image
        image = Image.open(file_path)
        # Calculate the aspect ratio to fit in canvas
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        
        # Adjust dimensions to maintain aspect ratio while fitting in canvas
        if aspect_ratio > WIDTH / HEIGHT:
            new_width = WIDTH
            new_height = int(WIDTH / aspect_ratio)
        else:
            new_height = HEIGHT
            new_width = int(HEIGHT * aspect_ratio)
        
        # Resize the image while maintaining aspect ratio
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to Tkinter PhotoImage and display
        photo_image = ImageTk.PhotoImage(image)
        
        # Clear canvas before creating a new image
        canvas.delete("all")
        canvas.create_image(WIDTH // 2, HEIGHT // 2, anchor="center", image=photo_image)

# Function for flipping the image
def flip_image():
    try:
        global image, photo_image, is_flipped
        
        if not is_flipped:
            # Open the image and flip it left and right
            image = Image.open(file_path).transpose(Image.FLIP_LEFT_RIGHT)
            is_flipped = True
        else:
            # Reset the image to its original state
            image = Image.open(file_path)
            is_flipped = False
        
        # Resize the image to fit the canvas
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        
        if aspect_ratio > WIDTH / HEIGHT:
            new_width = WIDTH
            new_height = int(WIDTH / aspect_ratio)
        else:
            new_height = HEIGHT
            new_width = int(HEIGHT * aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply rotation if needed
        if rotation_angle != 0:
            image = image.rotate(rotation_angle)
        
        # Convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.create_image(WIDTH // 2, HEIGHT // 2, anchor="center", image=photo_image)
    except:
        showerror(title='Flip Image Error', message='Please select an image to flip!')

# Function for rotating the image
def rotate_image():
    try:
        global image, photo_image, rotation_angle
        
        # Open the image
        image = Image.open(file_path)
        
        # Apply flip if needed
        if is_flipped:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Rotate the image
        rotation_angle = (rotation_angle + 90) % 360
        
        # Resize the image to fit the canvas
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        
        if aspect_ratio > WIDTH / HEIGHT:
            new_width = WIDTH
            new_height = int(WIDTH / aspect_ratio)
        else:
            new_height = HEIGHT
            new_width = int(HEIGHT * aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply rotation
        rotated_image = image.rotate(rotation_angle)
        
        # Convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(rotated_image)
        canvas.delete("all")
        canvas.create_image(WIDTH // 2, HEIGHT // 2, anchor="center", image=photo_image)
    except:
        showerror(title='Rotate Image Error', message='Please select an image to rotate!')

# Function for applying filters to the opened image file
def apply_filter(filter_name):
    global image, photo_image
    try:
        # Open the original image
        original_image = Image.open(file_path)
        
        # Apply flip if needed
        if is_flipped:
            original_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Resize the image to fit the canvas
        img_width, img_height = original_image.size
        aspect_ratio = img_width / img_height
        
        if aspect_ratio > WIDTH / HEIGHT:
            new_width = WIDTH
            new_height = int(WIDTH / aspect_ratio)
        else:
            new_height = HEIGHT
            new_width = int(HEIGHT * aspect_ratio)
        
        original_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply rotation if needed
        if rotation_angle != 0:
            original_image = original_image.rotate(rotation_angle)
        
        # Apply the selected filter
        if filter_name == "Black and White":
            filtered_image = ImageOps.grayscale(original_image)
        elif filter_name == "Blur":
            filtered_image = original_image.filter(ImageFilter.BLUR)
        elif filter_name == "Contour":
            filtered_image = original_image.filter(ImageFilter.CONTOUR)
        elif filter_name == "Detail":
            filtered_image = original_image.filter(ImageFilter.DETAIL)
        elif filter_name == "Emboss":
            filtered_image = original_image.filter(ImageFilter.EMBOSS)
        elif filter_name == "Edge Enhance":
            filtered_image = original_image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_name == "Sharpen":
            filtered_image = original_image.filter(ImageFilter.SHARPEN)
        elif filter_name == "Smooth":
            filtered_image = original_image.filter(ImageFilter.SMOOTH)
        else:
            filtered_image = original_image
        
        # Update the global image
        image = filtered_image
        
        # Convert the PIL image to a Tkinter PhotoImage and display it on the canvas
        photo_image = ImageTk.PhotoImage(filtered_image)
        canvas.delete("all")
        canvas.create_image(WIDTH // 2, HEIGHT // 2, anchor="center", image=photo_image)
        
    except:
        showerror(title='Filter Error', message='Please select an image first!')

# Function for drawing lines on the opened image
def draw(event):
    global file_path
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")

# Function for changing the pen color
def change_color():
    global pen_color
    color = colorchooser.askcolor(title="Select Pen Color")
    if color[1]:  # If a color was selected (not canceled)
        pen_color = color[1]

# Function for erasing lines on the opened image
def erase_lines():
    global file_path
    if file_path:
        canvas.delete("oval")

# Function for changing pen size
def change_pen_size(size):
    global pen_size
    pen_size = size

# Function for saving the image
def save_image():
    global file_path
    if file_path:
        # Get the save location from user
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"),
                                                          ("JPEG files", "*.jpg;*.jpeg"),
                                                          ("All files", "*.*")])
        if save_path:
            if askyesno(title='Save Image', message='Do you want to save this image?'):
                # Get the canvas boundaries
                x = root.winfo_rootx() + canvas.winfo_x()
                y = root.winfo_rooty() + canvas.winfo_y()
                x1 = x + canvas.winfo_width()
                y1 = y + canvas.winfo_height()
                
                # Grab the image from the canvas
                try:
                    # Using ImageGrab to capture the canvas (works on Windows/macOS)
                    image = ImageGrab.grab(bbox=(x, y, x1, y1))
                    image.save(save_path)
                except Exception as e:
                    showerror(title='Save Error', message=f'Error saving image: {str(e)}')
    else:
        showerror(title='Save Error', message='Please open an image first!')

# Create a frame for pen size options
pen_size_frame = tk.Frame(left_frame, bg="#f0f0f0")
pen_size_frame.pack(padx=10, pady=10)

# Label for pen size
pen_size_label = tk.Label(pen_size_frame, text="Pen Size:", bg="#f0f0f0", font=("Arial", 10, "bold"))
pen_size_label.grid(row=0, column=0, columnspan=3, pady=5)

# Buttons for different pen sizes
small_pen_btn = tk.Button(pen_size_frame, text="Small", command=lambda: change_pen_size(2), 
                          width=5, bg="#e0e0e0", relief=tk.RAISED)
small_pen_btn.grid(row=1, column=0, padx=2)

medium_pen_btn = tk.Button(pen_size_frame, text="Medium", command=lambda: change_pen_size(5), 
                           width=5, bg="#e0e0e0", relief=tk.RAISED)
medium_pen_btn.grid(row=1, column=1, padx=2)

large_pen_btn = tk.Button(pen_size_frame, text="Large", command=lambda: change_pen_size(10), 
                          width=5, bg="#e0e0e0", relief=tk.RAISED)
large_pen_btn.grid(row=1, column=2, padx=2)

# Create buttons with descriptive text instead of icons
open_btn = tk.Button(left_frame, text="Open Image", command=open_image, 
                     bg="#4CAF50", fg="white", width=15, height=2)
open_btn.pack(pady=5)

flip_btn = tk.Button(left_frame, text="Flip Image", command=flip_image, 
                     bg="#2196F3", fg="white", width=15, height=2)
flip_btn.pack(pady=5)

rotate_btn = tk.Button(left_frame, text="Rotate Image", command=rotate_image, 
                       bg="#FFC107", fg="white", width=15, height=2)
rotate_btn.pack(pady=5)

color_btn = tk.Button(left_frame, text="Change Color", command=change_color, 
                      bg="#9C27B0", fg="white", width=15, height=2)
color_btn.pack(pady=5)

erase_btn = tk.Button(left_frame, text="Erase Drawing", command=erase_lines, 
                      bg="#F44336", fg="white", width=15, height=2)
erase_btn.pack(pady=5)

save_btn = tk.Button(left_frame, text="Save Image", command=save_image, 
                     bg="#607D8B", fg="white", width=15, height=2)
save_btn.pack(pady=5)

# Bind the filter selection to the apply_filter function
filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))

# Bind canvas to mouse drag for drawing
canvas.bind("<B1-Motion>", draw)

# Start the main loop
root.mainloop()