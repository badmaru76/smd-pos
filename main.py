import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter import filedialog as fd
from PIL import Image, ImageTk,ImageDraw
import interface as intf

import cv2

first_click = 0
current_value = 0
x_dim = 0
y_dim = 0
frame = None

imgtk = None
img_orig = None
img_draw = None


def image_cord(event):
    global first_click
    if first_click == 0:
        canvas.create_rectangle(event.x -2, event.y -2, event.x+2, event.y+2,
                                outline="#fb0", fill="#fb0")
        intf.set_origin(event.x, event.y)
    elif first_click == 1:
        canvas.create_rectangle(event.x - 2, event.y - 2, event.x + 2, event.y + 2,
                                outline="#0bf", fill="#0bf")
        intf.set_scale(intf.x_dim, intf.y_dim, event.x, event.y)
    elif first_click > 2:
        x_pos_mm, y_pos_mm, pos_rot = intf.get_position(event.x, event.y, 0)
        print("X mm:", x_pos_mm)
        print("Y mm:", y_pos_mm)
        #update_table(x_pos_mm, y_pos_mm)
    first_click += 1
    print("X:", event.x)
    print("Y:", event.y)


def overlay(self):
    im = Image.new("RGBA", (100, 100), (255, 255, 0, 255))
    draw = ImageDraw.Draw(im)
    draw.ellipse((10, 10, 90, 90), fill=(0, 0, 0, 0))
    return im


def combine(img_orig, img_pos):
    return Image.alpha_composite(img_orig, img_pos)


def select_file():
    global img_orig, img_draw, imgtk
    filetypes = (('image files', '*.png *.jpg'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Open an Image', initialdir='/home/badmaru/Documenti', filetypes=filetypes)
    #showinfo(title='Selected Image', filename)
    #cv2image = cv2.imread(filename)
    #img = Image.fromarray(cv2image)
    print("select file fired")
    #img_label = ttk.Label(frame)
    #img_label.grid(column=1, row=1, sticky=tk.W)
    # Convert image to PhotoImage
    img = Image.open(filename)
    imgtk = ImageTk.PhotoImage(image=img)
    #img_label.imgtk = imgtk
    #img_label.configure(image=imgtk)
    canvas.config(width=img.size[0], height=img.size[1])
    canvas.create_image(0, 0, image=imgtk, anchor='nw')


def slider_changed(event):
    print(event)#slider.get())


def double_click_table(event):
    curItem = event.widget.focus()
    treeview = event.widget
    row_data = event.widget.item(curItem)['values']
    #print(row_data[0])
    img_x, img_y, img_rot = intf.calc_position(float(row_data[2]), float(row_data[3]), float(row_data[4]))
    canvas.create_rectangle(int(img_x-2), int(img_y-2),int(img_x +2), int(img_y+2), outline="#bf0", fill="#bf0")



def create_table(frame, df):
    PP_table = ttk.Treeview(frame)

    PP_table['columns'] = ('Articolo', 'Referenza', 'X', 'Y', 'rot')

    PP_table.column("#0", width=0, stretch='NO')
    PP_table.column("Articolo", anchor='n', width=80)
    PP_table.column("Referenza", anchor='n', width=80)
    PP_table.column("X", anchor='n', width=80)
    PP_table.column("Y", anchor='n', width=80)
    PP_table.column("rot", anchor='n', width=80)
    PP_table.heading("#0", text="", anchor='n')
    PP_table.heading("Articolo", text="Articolo", anchor='n')
    PP_table.heading("Referenza", text="Referenza", anchor='n')
    PP_table.heading("X", text="X", anchor='n')
    PP_table.heading("Y", text="Y", anchor='n')
    PP_table.heading("rot", text="rot", anchor='n')

    for (idx, row) in df.iterrows():
        #print(row.ItemCode, row.Ref, row.X, row.Y, row.Rot)
        PP_table.insert(parent='', index='end', iid=idx, text='',
                        values=(row.ItemCode, row.Ref, row.X, row.Y, row.Rot)
                        )

    PP_table.grid(column=1, row=3, sticky=tk.W)
    PP_table.bind("<Double-1>", double_click_table)


def update_table(x,y):
    PP_table = ttk.Treeview(frame)
    selected_item = PP_table.selection()
    PP_table.item(1,'#3', values=(str(x)))


def create_input_frame(container):
    global frame
    frame = ttk.Frame(container)

    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)

    # Find what
    ttk.Label(frame, text='Find what:').grid(column=0, row=0, sticky=tk.W)
    keyword = ttk.Entry(frame, width=20)
    keyword.focus()
    keyword.grid(column=0, row=0, sticky=tk.W)

    # Replace with:
    #ttk.Label(frame, text='Replace with:').grid(column=0, row=1, sticky=tk.W)
    #replacement = ttk.Entry(frame, width=30)
    #replacement.grid(column=1, row=1, sticky=tk.W)

    # Match Case checkbox
    #match_case = tk.StringVar()
    #match_case_check = ttk.Checkbutton(frame, text='Match case', variable=match_case, command=lambda: print(match_case.get()))
    #match_case_check.grid(column=0, row=2, sticky=tk.W)

    # Wrap Around checkbox
    #wrap_around = tk.StringVar()
    #wrap_around_check = ttk.Checkbutton(
    #    frame,
    #    variable=wrap_around,
    #    text='Wrap around',
    #    command=lambda: print(wrap_around.get()))
    #wrap_around_check.grid(column=0, row=3, sticky=tk.W)

    #  slider
    slider = ttk.Scale(
        frame,
        from_=0,
        to=100,
        orient='horizontal',  # vertical
        command=slider_changed,
        variable=current_value
    )
    slider.grid(column=0, row=3, sticky=tk.W)

    img_label = ttk.Label(frame)
    img_label.grid(column=1, row=3, sticky=tk.W)
    img_label.bind("<Button-1>", image_cord)

    #dialog box File (Image select)
    openfile_button = ttk.Button(frame, text='Open a File')#, command=select_file)#download_clicked)#
    openfile_button.bind("<Button-1>", select_file)
    openfile_button.grid(column=0, row=1, sticky=tk.W)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)
    return frame


def create_button_frame(container):
    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)

    ttk.Button(frame, text='Find Next',command=lambda: showwarning(
        title='Warning',
        message='This is a warning message.')).grid(column=0, row=0)
    ttk.Button(frame, text='Replace').grid(column=0, row=1)
    ttk.Button(frame, text='Replace All').grid(column=0, row=2)
    ttk.Button(frame, text='Cancel').grid(column=1, row=2)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=3)

    return frame




# root window
root = tk.Tk()
root.title('Pick & Place Viewer ')
root.geometry('600x500')
root.resizable(True, True)

#root.iconbitmap('./assets/pythontutorial.ico')

# windows only (remove the minimize/maximize button)
#root.attributes('-fullscreen', True)

# layout on the root window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)

# slider current value
current_value = tk.DoubleVar()


frame = ttk.Frame(root)


# grid layout for the input frame
frame.columnconfigure(0, weight=1)
frame.columnconfigure(0, weight=3)

# Find what
ttk.Label(frame, text='Find what:').grid(column=0, row=0, sticky=tk.W)
keyword = ttk.Entry(frame, width=20)
keyword.focus()
keyword.grid(column=0, row=0, sticky=tk.W)


# grid layout for the input frame
frame.columnconfigure(0, weight=1)
frame.columnconfigure(0, weight=3)


img_label = ttk.Label(frame)
img_label.grid(column=1, row=3, sticky=tk.W)



# Create the canvas, size in pixels.
canvas = tk.Canvas(width=800, height=200, bg='white')
# Pack the canvas into the Frame.
canvas.grid(column=0, row=3, sticky=tk.W)
canvas.bind("<Button-1>", image_cord)  #<Motion>






#dialog box File (Image select)
openfile_button = ttk.Button(frame, text='Open a File', command=select_file)#download_clicked)#
#openfile_button.bind("<Button-1>", select_file)
openfile_button.grid(column=0, row=1, sticky=tk.W)


frame.grid(column=0, row=0)

smd_df = intf.load_datafile('/home/badmaru/Documenti/ABAS_MD_BMS_SE9B.xlsx')
create_table(frame, smd_df)
root.mainloop()






