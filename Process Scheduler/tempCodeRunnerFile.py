import tkinter as tk
from src.gui import SchedulerGUI
#from tests.gui import SchedulerGUI

def main():
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.configure(bg='#03012d') 
    root.mainloop()


if __name__ == "__main__":
    main()
