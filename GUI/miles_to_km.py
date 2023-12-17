from tkinter import *

window = Tk()
window.title('Mile to Km Converter')
window.minsize(width=200, height=100)
window.config(padx=20, pady=20)

def calculate():
    miles = entry.get()
    if miles is not None:
        km = float(miles) * 1.6
        label_result.config(text=f'{km}')

entry = Entry(width=10)
label_1 = Label(text='Miles')
label_2 = Label(text='is equal to')
label_result = Label(text='0', width=10)
label_3 = Label(text='Km')
button = Button(text='Calculate', command=calculate)

entry.grid(row=0,column=1)
label_1.grid(row=0,column=2)
label_2.grid(row=1,column=0)
label_result.grid(row=1,column=1)
label_3.grid(row=1,column=2)
button.grid(row=2,column=1)

window.mainloop()