import tkinter as tk

root = tk.Tk()
root.geometry("800x450")
root.title("How should i change border color")
tk.Label(root, text="How should i change border color", width=50, height=4, bg="White", highlightthickness=4, highlightbackground="#37d3ff").place(x=10, y=10)
tk.Button(root, text="Button", width=5, height=1, bg="White", highlightbackground="#37d3ff").place(x=100, y=100)


root.mainloop()