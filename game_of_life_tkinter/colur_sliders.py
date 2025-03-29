import tkinter as tk
from tkinter import ttk

window = tk.Tk()
main_frame = tk.Frame(master=window)


def tup2hex(t1,t2,t3):
	return f'#{t1:02x}{t2:02x}{t3:02x}'


def hex2tup(s):
	return int(s[1:3],base=16),int(s[3:5],base=16),int(s[5:7],base=16)


def new_selected(selection):
	colour_scale_red.set(hex2tup(dropbox_options[selection].cget('bg'))[0])
	colour_scale_green.set(hex2tup(dropbox_options[selection].cget('bg'))[1])
	colour_scale_blue.set(hex2tup(dropbox_options[selection].cget('bg'))[2])


def change_colour(event, colour, selection):
	if colour == 'red':
		_, t2, t3 = hex2tup(dropbox_options[selection].cget('bg'))
		dropbox_options[selection].config(bg=tup2hex(int(event), t2, t3))
	if colour == 'green':
		t1, _, t3 = hex2tup(dropbox_options[selection].cget('bg'))
		dropbox_options[selection].config(bg=tup2hex(t1, int(event), t3))
	if colour == 'blue':
		t1, t2, _ = hex2tup(dropbox_options[selection].cget('bg'))
		dropbox_options[selection].config(bg=tup2hex(t1, t2, int(event)))



colour_changes = ttk.Combobox(master=main_frame, state='readonly', values=['frame1', 'frame2', 'frame3'])
colour_changes.grid(row=6, column=1)
colour_changes.bind('<<ComboboxSelected>>', lambda selection:new_selected(selection=colour_changes.get()))

colour_scale_red = tk.Scale(master=main_frame, from_=0, to=255, orient='horizontal',
							command=lambda event:change_colour(event=event, colour='red', selection=colour_changes.get()))
colour_scale_red.grid(row=3, column=1)

colour_scale_green = tk.Scale(master=main_frame, from_=0, to=255, orient='horizontal',
							  command=lambda event:change_colour(event=event, colour='green', selection=colour_changes.get()))
colour_scale_green.grid(row=4, column=1)

colour_scale_blue = tk.Scale(master=main_frame, from_=0, to=255, orient='horizontal',
							 command=lambda event:change_colour(event=event, colour='blue', selection=colour_changes.get()))
colour_scale_blue.grid(row=5, column=1)


frame1 = tk.Frame(master=main_frame, width=50, height=50, bg='#ff0000')
frame2 = tk.Frame(master=main_frame, width=50, height=50, bg='#0000ff')
frame3 = tk.Frame(master=main_frame, width=50, height=50, bg='#000000')

frame1.grid(row=1, column=1)
frame2.grid(row=1, column=2)
frame3.grid(row=1, column=3)

dropbox_options = {'frame1': frame1, 'frame2': frame2, 'frame3': frame3}

main_frame.pack()
window.mainloop()