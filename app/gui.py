import cv2
import dlib
import os
import tkinter as tk
from tkinter import filedialog, Toplevel, Label, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
from app.utils import detect_faces_and_save

def open_image(panel, canvas, frame, status_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        # Clear the frame before adding new content
        for widget in frame.winfo_children():
            widget.destroy()

        # Fixed width and height for the image frame
        FRAME_WIDTH = 840
        FRAME_HEIGHT = 560

        # Load and process the image
        image, face_count, match_count = detect_faces_and_save(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Resize the image to fit within the fixed frame dimensions
        image.thumbnail((FRAME_WIDTH, FRAME_HEIGHT))
        image = ImageTk.PhotoImage(image)

        status_label.config(text=f"Successfully detected {face_count} faces.")
        status_label.pack(pady=10)

        # Create and pack the image label
        label = tk.Label(frame, image=image, bg="#f0f0f0", width=FRAME_WIDTH, height=FRAME_HEIGHT)
        label.image = image  # Keep a reference to avoid garbage collection
        label.pack()

        # Display the number of matched faces if applicable
        if match_count > 0:
            match_label = tk.Label(frame, text=f"{match_count} face(s) data available.", bg="#f0f0f0", font=("Arial", 12))
            match_label.pack(pady=10)

        # Update the scroll region to accommodate the new content
        canvas.configure(scrollregion=canvas.bbox("all"))

# The rest of the code remains unchanged


def show_full_image(image_path, image_id):
    """Display the full image and its ID in a new window."""
    full_image_window = Toplevel()
    full_image_window.title("Full Image")

    image = Image.open(image_path)
    image = ImageTk.PhotoImage(image)

    label = Label(full_image_window, image=image)
    label.image = image  # Keep a reference to avoid garbage collection
    label.pack(padx=10, pady=10)

    label_id = Label(full_image_window, text=image_id, font=("Arial", 12), bg="#f0f0f0")
    label_id.pack(pady=10)

def show_data():
    """Create a scrollable window to display all detected face images."""
    output_folder = 'output'
    if not os.path.exists(output_folder):
        return

    data_window = Toplevel()
    data_window.title("Detected Faces")
    data_window.configure(bg="#303030")
    

    canvas = Canvas(data_window, bg="#f0f0f0")
    scroll_y = Scrollbar(data_window, orient="vertical", command=canvas.yview)
    scroll_x = Scrollbar(data_window, orient="horizontal", command=canvas.xview)
    
    frame = Frame(canvas, bg="#f0f0f0")
    row = 0
    col = 0

    for filename in os.listdir(output_folder):
        if filename.endswith('.jpg'):
            file_path = os.path.join(output_folder, filename)
            image = Image.open(file_path)
            image.thumbnail((100, 100))
            image = ImageTk.PhotoImage(image)

            label = Label(frame, image=image, bg="#f0f0f0", cursor="hand2")
            label.image = image  # Keep a reference to avoid garbage collection
            label.grid(row=row, column=col, padx=5, pady=5)
            label.bind("<Button-1>", lambda e, p=file_path, i=filename: show_full_image(p, i))

            col += 1
            if col > 4:
                col = 0
                row += 1

    frame.update_idletasks()
    canvas.create_window(0, 0, anchor='nw', window=frame)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'), 
                     yscrollcommand=scroll_y.set,
                     xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    scroll_x.pack(fill='x', side='bottom')

def start_app():
    """Initialize and start the main application window."""
    root = tk.Tk()
    root.title("Face Detection App")
    root.configure(bg="#303030")


    # Set the application window to full screen
    # Set the application window to full screen size with minimize, maximize, and close options
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # adjusted_height = screen_height - 50
    # root.geometry(f"{screen_width}x{adjusted_height}")
    # Set the application window to start maximized
    root.state('zoomed')  # This works for Windows
    # Set the window size to 400x600 when !maximize
    root.geometry("720x480")


    
    top_frame = Frame(root, bg="#303030")
    top_frame.pack(side="top", fill="x", padx=10, pady=10)

    btn_open = tk.Button(top_frame, text="Open Image", command=lambda: open_image(panel, canvas, frame, status_label), 
                         bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    btn_open.pack(side="left", padx=10)

    btn_data = tk.Button(top_frame, text="Data", command=show_data, 
                         bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    btn_data.pack(side="left", padx=10)

    canvas = Canvas(root, bg="#f0f0f0")
    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_x = Scrollbar(root, orient="horizontal", command=canvas.xview)

    frame = Frame(canvas, bg="#f0f0f0")
    panel = tk.Label(frame, bg="#f0f0f0")

    canvas.create_window((0, 0), window=frame, anchor='nw')
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True, side='left', padx=10, pady=10)
    scroll_y.pack(fill='y', side='right')
    scroll_x.pack(fill='x', side='bottom')

    status_label = tk.Label(root, text="", bg="#303030", fg="white", font=("Arial", 12))
    status_label.pack(pady=10)

    # Create a frame for the exit button at the bottom
    bottom_frame = Frame(root, bg="#303030")
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10, anchor='se')

    # Add the Exit button
    btn_exit = tk.Button(bottom_frame, text="Exit", command=root.quit,
                         bg="#FF0000", fg="white", font=("Arial", 12, "bold"))
    btn_exit.pack(side="right", padx=10)

    root.mainloop()
