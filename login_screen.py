# =============================================================
# SHADOX — gui/login_screen.py
# The first screen users see when they launch the app.
# Provides College ID + Password login and a route to Register.
# =============================================================

import tkinter as tk
from tkinter import messagebox

# Import the login function from the auth module
from core.auth import login_user


def show_login_screen(root):
    """
    Builds and displays the login screen inside the given Tkinter root window.

    Args:
        root (tk.Tk): The main application window created in main.py
    """

    # ── Step 1: Configure the root window ─────────────────────
    root.title("SHADOX Login")
    root.geometry("400x350")
    root.resizable(False, False)

    # Clear any existing widgets (useful when navigating back from register)
    for widget in root.winfo_children():
        widget.destroy()
        # Remove old key bindings
        root.unbind("<Return>")

    # ── Step 2: App title label ───────────────────────────────
    title_label = tk.Label(
        root,
        text="SHADOX",
        font=("Helvetica", 28, "bold")
    )
    title_label.pack(pady=(30, 4))

    subtitle_label = tk.Label(
        root,
        text="Anonymous Interaction Platform",
        font=("Helvetica", 10)
    )
    subtitle_label.pack(pady=(0, 24))

    # ── Step 3: College ID field ──────────────────────────────
    tk.Label(root, text="College ID", font=("Helvetica", 11)).pack(anchor="w", padx=60)

    college_id_entry = tk.Entry(root, width=30, font=("Helvetica", 11))
    college_id_entry.pack(padx=60, pady=(2, 12))

    # ── Step 4: Password field ────────────────────────────────
    tk.Label(root, text="Password", font=("Helvetica", 11)).pack(anchor="w", padx=60)

    # show="*" hides the characters as the user types
    password_entry = tk.Entry(root, width=30, font=("Helvetica", 11), show="*")
    password_entry.pack(padx=60, pady=(2, 20))

    # ── Step 5: Button logic ──────────────────────────────────

    def handle_login():
        """
        Reads the input fields, calls login_user(), and shows
        a success or error message depending on the result.
        """
        college_id = college_id_entry.get()
        password   = password_entry.get()

        # Call the auth function
        result = login_user(college_id, password)

        if result["success"]:
            # Login succeeded — store user data and open chat screen
            user = result["user"]
            messagebox.showinfo("Welcome", result["message"])

            # Import here to avoid circular imports at the top of the file
            from gui.chat_screen import show_chat_screen
            show_chat_screen(root, user)

        else:
            # Login failed — show the error returned by auth.py
            messagebox.showerror("Login Failed", result["message"])

    def go_to_register():
        """
        Navigates to the registration screen.
        """
        from gui.register_screen import show_register_screen
        show_register_screen(root)

    # ── Step 6: Login and Register buttons ────────────────────
    login_btn = tk.Button(
        root,
        text="Login",
        width=20,
        font=("Helvetica", 11),
        command=handle_login
    )
    login_btn.pack(pady=(0, 8))

    register_btn = tk.Button(
        root,
        text="Register",
        width=20,
        font=("Helvetica", 11),
        command=go_to_register
    )
    register_btn.pack()

    # Allow pressing Enter to submit the login form
    root.bind("<Return>", lambda event: handle_login())