from tkinter import *

from src.gui.ShowUserGUI import ShowUserGUI

# Lanzamos interfaz gráfica.
root = Tk()
ShowUserGUI.show_chooser(root)
root.mainloop()
