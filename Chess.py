class Chess:
    def __init__(self, window):
        self.window = window
        self.window.title("Chess")
        self.window.geometry("900x900")
        self.window.resizable(False, False)
        self.window.configure(bg="#FFFFFF")