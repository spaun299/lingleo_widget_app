import tkinter

root = tkinter.Tk(screenName='Lingleo Widget')


def test(event):
    print('Clicked Left button')


frame = tkinter.Frame(root, width=300, height=250)
frame.bind('<Button-1>', test)
frame.pack()


root.mainloop()
