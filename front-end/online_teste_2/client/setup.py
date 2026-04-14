import threading, json, os
import numpy as np, tkinter as tk
from tkinter import font

DIR = os.path.dirname(os.path.realpath(__file__))

root = tk.Tk()
root.resizable(False,False)
root.title('Setup')

ansi = font.nametofont('ansi',root)
ansi.config(size=10)

def add_placeholder(widget:tk.Event,text:str):
    widget.insert(0,text)
    widget.config(fg='gray',show='')
    def focus_in(event:tk.Event,text=text):
        self = event.widget
        if self.get() == text and self['fg']=='gray':
            self.config(fg='black',show='')
            self.delete(0,tk.END)
    def focus_out(event:tk.Event,text=text):
        self = event.widget
        if self.get() == '':
            self.insert(0,text)
            self.config(fg='gray',show='')
    widget.bind('<FocusOut>',focus_out)
    widget.bind('<FocusIn>' ,focus_in )

#def init():
#    os.system(f'{DIR}\\client.py {name} {address} {port}')


labl_frame = tk.Frame(root,width= 60,height=100,bg='red'  )
entr_frame = tk.Frame(root,width=200,height=100,bg='green')
bttn_frame = tk.Frame(root,width=260,height= 50,bg='blue' )

labl_frame.grid_propagate(False)
entr_frame.grid_propagate(False)
bttn_frame.pack_propagate(False)

labl_frame.grid(row=0,column=0)
entr_frame.grid(row=0,column=1)
bttn_frame.grid(row=1,columnspan=2)

name_label = tk.Label(labl_frame,font=ansi,text='Name:')
name_entry = tk.Entry(entr_frame,font=ansi)

addr_label = tk.Label(labl_frame,font=ansi,text='Address:')
addr_ipntr = tk.Entry(entr_frame,font=ansi)
addr_pontr = tk.Entry(entr_frame,font=ansi)

add_placeholder(name_entry,'username')
add_placeholder(addr_ipntr,'ip address')
add_placeholder(addr_pontr,'port')

name_label.grid(row=0,padx=[2,0],pady=[20,0],sticky='w')
addr_label.grid(row=1,padx=[2,0],pady=[10,0],sticky='w')

name_entry.grid(row=0,padx=[10,0],pady=[20,0])
addr_ipntr.grid(row=1,padx=[10,0],pady=[10,0])
addr_pontr.grid(row=2,padx=[10,0])


entr_buttn = tk.Button(root)

tk.mainloop()