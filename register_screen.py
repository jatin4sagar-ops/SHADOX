# =============================================================
# SHADOX — gui/register_screen.py
# Registration screen where new students create an account.
# After successful registration, the user is sent back to login.
# =============================================================

import tkinter as tk
from tkinter import messagebox

# Import the registration function from the auth module
from core.auth import register_user


def show_register_screen(root):
    """
    Builds and displays the registration screen inside the given
    Tkinter root window.

    Args:
        root (tk.Tk): The main application window created in main.py
    """

    # ── Step 1: Configure the root window ─────────────────────
    root.title("SHADOX Register")
    root.geometry("400x380")
    root.resizable(False, False)

    # Clear any existing widgets from the previous screen
    for widget in root.winfo_children():
        widget.destroy()

    # ── Step 2: Title labels ───────────────────────────────────
    title_label = tk.Label(
        root,
        text="SHADOX",
        font=("Helvetica", 28, "bold")
    )
    title_label.pack(pady=(30, 4))

    subtitle_label = tk.Label(
        root,
        text="Create your anonymous account",
        font=("Helvetica", 10)
    )
    subtitle_label.pack(pady=(0, 24))

    # ── Step 3: College ID field ───────────────────────────────
    tk.Label(root, text="College ID", font=("Helvetica", 11)).pack(anchor="w", padx=60)

    college_id_entry = tk.Entry(root, width=30, font=("Helvetica", 11))
    college_id_entry.pack(padx=60, pady=(2, 12))

    # ── Step 4: Password field ─────────────────────────────────
    tk.Label(root, text="Password", font=("Helvetica", 11)).pack(anchor="w", padx=60)

    # show="*" masks the characters as the user types
    password_entry = tk.Entry(root, width=30, font=("Helvetica", 11), show="*")
    password_entry.pack(padx=60, pady=(2, 20))

    # ── Step 5: Button logic ───────────────────────────────────

    def handle_register():
        """
        Reads the input fields, calls register_user(), and shows
        a success or error message depending on the result.
        On success, navigates back to the login screen.
        """
        college_id = college_id_entry.get()
        password   = password_entry.get()

        # Call the auth function
        result = register_user(college_id, password)

        if result["success"]:
            # Registration succeeded — inform the user of their codename
            messagebox.showinfo("Registration Successful", result["message"])

            # Navigate back to the login screen
            go_to_login()

        else:
            # Registration failed — show the error returned by auth.py
            messagebox.showerror("Registration Failed", result["message"])

    def go_to_login():
        """
        Navigates back to the login screen.
        Imported here to avoid circular imports at the top of the file.
        """
        from gui.login_screen import show_login_screen
        show_login_screen(root)

    # ── Step 6: Register and Back buttons ─────────────────────
    register_btn = tk.Button(
        root,
        text="Register",
        width=20,
        font=("Helvetica", 11),
        command=handle_register
    )
    register_btn.pack(pady=(0, 8))

    back_btn = tk.Button(
        root,
        text="Back to Login",
        width=20,
        font=("Helvetica", 11),
        command=go_to_login
    )
    back_btn.pack()

    # Allow pressing Enter to submit the registration form
    root.bind("<Return>", lambda event: handle_register())