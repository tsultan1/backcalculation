from tkinter import *


class CommonButtons:

    def create_back_button(parent):
        back_button = Button(parent, text='Back', fg='brown')
        back_button.config(height=2, width=10)
        back_button.pack()
        back_button.place(relx=0.1, rely=0.9, anchor=CENTER)
        return back_button

    def create_next_button(parent):
        next_button = Button(parent, text='Next', fg='brown')
        next_button.config(height=2, width=10)
        next_button.pack()
        next_button.place(relx=0.9, rely=0.9, anchor=CENTER)
        return next_button




