import tkinter as tk
from tkinter import messagebox
from PIL import Image

import pyperclip
from cryptography.fernet import Fernet
import string
import random
import os
# create a key for encryption/decryption
key = Fernet.generate_key()
fernet = Fernet(key)

# create a tkinter window
root = tk.Tk()
root.geometry("600x400")

# create a frame for the sidebar
sidebar_frame = tk.Frame(root, bg="#333")

# create a label for the sidebar title
sidebar_title = tk.Label(sidebar_frame, text="M-Pass", font=("Arial", 18), fg="#fff", bg="#333", padx=10, pady=10)
sidebar_title.pack(side="top", fill="x")

# create a button for adding a new password
def add_password():
    # create a frame for the add password form
    add_password_frame = tk.Frame(root)

    # create labels and entry fields for the add password form
    tk.Label(add_password_frame, text="Website:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    website_entry = tk.Entry(add_password_frame, font=("Arial", 12), width=30)
    website_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_password_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    username_entry = tk.Entry(add_password_frame, font=("Arial", 12), width=30)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_password_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
    password_entry = tk.Entry(add_password_frame, font=("Arial", 12), width=30, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    # create a function for saving the password
    def save_password():
        # encrypt the password using the Blowfish algorithm
        encrypted_password = fernet.encrypt(password_entry.get().encode())

        # save the password to a hidden file
        with open(".m_pass", "a") as f:
            f.write(f"{website_entry.get()}|{username_entry.get()}|{encrypted_password.decode()}@\\n")

        # show a success message
        messagebox.showinfo("Success", "Password saved successfully!")

        # destroy the add password form frame
        add_password_frame.destroy()

    # create a button for saving the password
    save_button = tk.Button(add_password_frame, text="Save", font=("Arial", 12), command=save_password)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # show the add password form frame
    add_password_frame.pack()

# create a button for retrieving a password
def retrieve_password():
    # create a frame for the retrieve password form
    retrieve_password_frame = tk.Frame(root)

    # create a label and entry field for the website
    tk.Label(retrieve_password_frame, text="Website:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    website_entry = tk.Entry(retrieve_password_frame, font=("Arial", 12), width=30)
    website_entry.grid(row=0, column=1, padx=5, pady=5)

    # create a function for retrieving the password
    def get_password():
        # read the hidden file and get the corresponding line for the given website
        with open(".m_pass", "r") as f:
            lines = f.readlines()
            for line in lines:
                website, username, encrypted_password = line.strip().split("|")
                if website == website_entry.get():
                    # decrypt the password using the Blowfish algorithm
                    decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
                    # show the password in a message box
                    messagebox.showinfo("Password", f"Username: {username}\nPassword: {decrypted_password}")
                    return

        # show an error message if no password is found for the given website
        messagebox.showerror("Error", "No password found for the given website.")

    # create a button for retrieving the password
    get_button = tk.Button(retrieve_password_frame, text="Get Password", font=("Arial", 12), command=get_password)
    get_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # show the retrieve password form frame
    retrieve_password_frame.pack()

#create a function for checking the strength of a password
#create a function for checking the strength of a password
# define a list of common words to be avoided in passwords
common_words = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "monkey", "dragon", "football", "iloveyou", "abc123"]
# create a function for checking the strength of a password
def check_strength(password):
    # calculate the password strength based on length, complexity, and avoidance of common words
    length_bonus = min(len(password) / 12, 1.0)
    complexity_bonus = sum([1 for c in password if c.islower()]) * sum([1 for c in password if c.isupper()]) * sum([1 for c in password if c.isdigit()])
    common_words_penalty = sum([1 for word in common_words if word in password.lower()])
    strength = length_bonus * complexity_bonus * (1 - (common_words_penalty / 10))

    return strength


#create a function for generating a new password
def generate_password():
    # define the password length and character sets to use
    password_length = 16
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digit_chars = string.digits
    punctuation_chars = string.punctuation.replace("|", "").replace("\\", "").replace("/","")  # exclude some characters that may cause issues
    # generate the password by randomly selecting characters from the character sets
    password = "".join([random.choice(lowercase_chars + uppercase_chars + digit_chars + punctuation_chars) for i in range(password_length)])
    # check the strength of the generated password
    strength = check_strength(password)
    # show the password in a message box along with its strength
    pyperclip.copy(password)
    messagebox.showinfo("New Password", f"Your new password is:\n{password}\n\nPassword Strength: {strength:.2f}%")


# #create a frame for the main content
# content_frame = tk.Frame(root)
# #create a button for adding a new password
# add_password_button = tk.Button(sidebar_frame, text="Add Password", font=("Arial", 12), command=add_password)
# add_password_button.pack(side="top", fill="x", padx=10, pady=10)
# calculate the password strength
# create a function for checking the strength of a password
def calculate_strength(password):
    # calculate the password strength based on length, complexity, and avoidance of common words
    length_bonus = min(len(password) / 12, 1.0)
    complexity_bonus = sum([1 for c in password if c.islower()]) * sum([1 for c in password if c.isupper()]) * sum([1 for c in password if c.isdigit()]) / 1000
    common_word_penalty = 0
    for word in common_words:
        if word in password.lower():
            common_word_penalty += 1
    common_word_penalty = min(common_word_penalty, 2)
    score = length_bonus * complexity_bonus * (1 - common_word_penalty / 10)
    # return a score between 0 and 100
    return round(score * 10)

def log_show():
    try:
        img_path = os.path.abspath("unauthorized_access.jpg")
        img = Image.open(img_path)
        img.show()
    except:
        messagebox.showerror("Error", "Could not open unauthorized_access.jpg")



# create a button for quitting the application
def quit_app():
    root.destroy()

# create a button for clearing the password file
def clear_passwords():
    result = messagebox.askyesno("Confirm", "Are you sure you want to clear all passwords?")
    if result:
        with open(".m_pass", "w") as f:
            f.write("")
        messagebox.showinfo("Success", "Passwords cleared successfully.")

# create a button for displaying the help message
def show_help():
    help_message = "M-Pass is a simple password manager.\n\nTo add a new password, click the 'Add Password' button and enter the website, username, and password.\n\nTo retrieve a password, click the 'Retrieve Password' button and enter the website.\n\nTo check the strength of a password, click the 'Check Strength' button while adding a new password.\n\nTo clear all passwords, click the 'Clear Passwords' button."
    messagebox.showinfo("Help", help_message)

# create buttons for the sidebar
add_password_button = tk.Button(sidebar_frame, text="Add Password", font=("Arial", 12), command=add_password)
add_password_button.pack(side="top", fill="x", padx=10, pady=10)

add_password_button = tk.Button(sidebar_frame, text="Generate Password", font=("Arial", 12), command=generate_password)
add_password_button.pack(side="top", fill="x", padx=10, pady=10)

retrieve_password_button = tk.Button(sidebar_frame, text="Retrieve Password", font=("Arial", 12), command=retrieve_password)
retrieve_password_button.pack(side="top", fill="x", padx=10, pady=10)

clear_passwords_button = tk.Button(sidebar_frame, text="Clear Passwords", font=("Arial", 12), command=clear_passwords)
clear_passwords_button.pack(side="top", fill="x", padx=10, pady=10)

help_button = tk.Button(sidebar_frame, text="Help", font=("Arial", 12), command=show_help)
help_button.pack(side="top", fill="x", padx=10, pady=10)

quit_button = tk.Button(sidebar_frame, text="Quit", font=("Arial", 12), command=quit_app)
quit_button.pack(side="bottom", fill="x", padx=10, pady=10)

log_show = tk.Button(sidebar_frame, text="Log", font=("Arial", 12), command=log_show)
log_show.pack(side="bottom", fill="x", padx=10, pady=10)

# pack the sidebar frame
sidebar_frame.pack(side="left", fill="y")

# start the tkinter event loop
root.mainloop()
