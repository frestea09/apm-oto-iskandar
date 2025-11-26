"""Entry point for patient search and BPJS automation UI."""
import tkinter as tk

from app.ui import PatientApp


def main():
    root = tk.Tk()
    app = PatientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
