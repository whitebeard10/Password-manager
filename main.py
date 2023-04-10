import tkinter as tk
import os
from tkinter import messagebox
import cv2

# Create a new Tkinter window
window = tk.Tk()
window.title("M-Pass Login")
window.geometry("400x300")
window.minsize(800, 600)
window.maxsize(1200, 900)

# Set a custom background color for the window
window.config(bg="#cce6ff")

# Create a label for the title
title_label = tk.Label(text="Welcome to M-Pass", font=("Arial", 24), fg="#333333", bg="#F0F0F0")
title_label.pack(pady=20)

# Create a frame for the username and password fields
input_frame = tk.Frame(window, bg="#F0F0F0")
input_frame.pack()

# Create a label and entry box for the username
username_label = tk.Label(input_frame, text="Username:", font=("Arial", 14), fg="#333333", bg="#F0F0F0")
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
username_entry = tk.Entry(input_frame, font=("Arial", 14))
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a label and entry box for the master password
password_label = tk.Label(input_frame, text="Master Password:", font=("Arial", 14), fg="#333333", bg="#F0F0F0")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password_entry = tk.Entry(input_frame, show="*", font=("Arial", 14))
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Set variables to keep track of the number of login attempts and whether a photo has been taken
login_attempts = 0
photo_taken = False


# Create a button to log in
def login():
    # Declare the global variables for login attempts and photo taken
    global login_attempts, photo_taken

    # Check if the username and password are valid
    if username_entry.get() == "sudo" and password_entry.get() == "1YjrI135#":
        # Display a message box
        messagebox.showinfo("Login", "Login successful!")

        # Reset the login attempts counter and photo taken flag
        login_attempts = 0
        photo_taken = False

        # Open the landing page using the os module
        os.system('python home.py')

        # Close the current window
        window.destroy()
    else:
        # Increment the login attempts counter
        login_attempts += 1

        # Display an error message if the password is incorrect
        messagebox.showerror("Error", "Invalid username or password")

        # Check if the user has entered the correct password
        if password_entry.get() == "1YjrI135#":
            # Check if the user has entered the wrong password more than once
            if login_attempts >= 2:
                # Show a warning message about unauthorized access attempts
                response = messagebox.askokcancel("Warning",
                                                  "Unauthorized access attempt detected! Do you want to view the login attempts log?")
                if response == 1:
                    # Open the login attempts log using the os module
                    os.system('python log.py')

        # Check if the user has entered the wrong password more than twice
        if login_attempts >= 3:
            # Take a photo using the webcam
            if not photo_taken:
                # Create a VideoCapture object
                cap = cv2.VideoCapture(0)

                # Check if the webcam is available
                if not cap.isOpened():
                    messagebox.showerror("Error", "Webcam is not available!")
                else:
                    # Capture a photo
                    ret, frame = cap.read()
                    if ret:
                        # Save the photo as a JPEG file
                        cv2.imwrite("unauthorized_access.jpg", frame)

                        # Display a message box
                        messagebox.showwarning("Warning", "Unauthorized access attempt detected! A photo has been taken and saved.")

                        # Set the photo_taken flag to True
                        photo_taken = True

                    # Release the webcam
                    cap.release()

            if username_entry.get() == "sudo" and password_entry.get() == "1YjrI135#":
                response = messagebox.askokcancel("Warning",
                                                  "Unauthorized access attempt detected! Do you want to view the login attempts log?")
                if response == 1:
                    # Open the login attempts log using the os module
                    os.system('python log.py')

login_button = tk.Button(window, text="Log In", command=login, font=("Arial", 14), bg="#333333", fg="#F0F0F0")
login_button.pack(pady=10)

# Create a button to sign up
def signup():
    # Display a message box with instructions for signing up
    messagebox.showinfo("Sign Up", "To sign up, please contact the administrator.")

signup_button = tk.Button(window, text="Sign Up", command=signup, font=("Arial", 14), bg="#333333", fg="#F0F0F0")
signup_button.pack()

# Start the Tkinter event loop
window.mainloop()



