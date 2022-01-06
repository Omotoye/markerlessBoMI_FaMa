import tkinter

# Getting the screen resolution of the Computer


def get_display_size():
    screen = tkinter.Tk()
    screen.update_idletasks()
    screen.attributes("-fullscreen", True)
    screen.state("iconic")
    height = screen.winfo_screenheight()
    width = screen.winfo_screenwidth()
    screen.destroy()
    return width, height
