import tkinter as t

def readOut():
    with open("output.txt", "r") as f:
        outText.config(text=f.read())
    window.after(500, readOut)

window = t.Tk()
window.title("Leap Output")
output = t.Text(window, wrap = "word", width = 40, height = 10)
output.pack(pady=10)

outText = t.Label(output, text = "Hang on...")
outText.grid(row = 1, column = 1)

    
readOut()
window.mainloop()
