import tkinter
import websocket
from config import ws_url

root = tkinter.Tk(screenName='Lingleo Widget')

# root.overrideredirect(1)
frame = tkinter.Frame(root, width=300, height=250)
frame.bind('<Button -1>')
frame.pack()
button = tkinter.Button(frame, command=root.withdraw)
button.pack()
root.mainloop()
