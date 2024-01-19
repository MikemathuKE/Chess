import tkinter as tk
from Chess import Chess

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x500")
    Chess(root)
    root.mainloop()