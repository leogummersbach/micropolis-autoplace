from image_array import *
import os
import copy
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from module_connections import *
from PIL import ImageGrab


width = 100
draw_scale = 128
max_x = int(1600/draw_scale)
max_y = int(1000/draw_scale)
high_prio = []
low_prio = []
globalImageArray = None


window = Tk()
window.title("Micropolis Autoplace")

max_inits = IntVar()
max_inits.set(100)

#FRAME menu
menuframe = Frame(window, width = width)
menuframe.pack(side=LEFT)

#FRAME canvas
canvas = Canvas(window, width=max_x*draw_scale, height=max_y*draw_scale, background="lightgray")
canvas.pack(side=LEFT)

def drawGrid(x, y, useCustoms=False, consumeCustoms=True, verbose=False):
    global img, globalImageArray, state
    percent = int(max_inits.get()/100)
    places = x*y
    left_allowed = len(high_prio) - places
    bestResult = None
    bestScore = x*y
    if(left_allowed < 0):
        left_allowed = 0
    for i in range(max_inits.get()):
        if(i % percent == 0):
            if verbose: print(f"{int(i/percent)} %")
            state.set(f"{int(i/percent)} %")
            statelabel.update()
        imagearray = ImageArray()
        for h in high_prio:
            sl = Module_connections()
            datapath = h[:-4] + ".json"
            sl.load(datapath)
            imagearray.addHighPriority(h, sl.streetLocations)

        success = imagearray.init_array(x, y, mindCustoms=useCustoms, consumeCustoms=consumeCustoms, verbose=False)

        if(consumeCustoms):
            if(len(imagearray.highPriority) < bestScore):
                #new best score
                bestScore = len(imagearray.highPriority)
                bestResult = copy.deepcopy(imagearray.dict)
        else:
            if(imagearray.countDefaults() < bestScore):
                #new best score
                bestScore = imagearray.countDefaults()
                bestResult = copy.deepcopy(imagearray.dict)

        if(success and (((not consumeCustoms) and imagearray.countDefaults() == 0) or len(imagearray.highPriority) <= left_allowed or i == max_inits.get()-1)):
            if verbose: print(f"Final initialization after {i + 1} attempts. {len(imagearray.highPriority)} high priority modules left, {left_allowed} were allowed.")
            if(i == max_inits.get()-1):
                imagearray.dict = bestResult
            state.set(f"Final initialization after {i+1} attempts.\n{bestScore} high priority modules left,\n{left_allowed} were allowed.")
            break
    globalImageArray = imagearray
    imagelist = imagearray.toImageList(size=draw_scale)
    img = imagelist.getImageTkList()
    coords = imagelist.getCoordList()
    for i in range(len(img)):
        canvas.create_image(coords[i][0], coords[i][1], image=img[i], anchor="nw")

def redrawGrid(newsize):
    global draw_scale, img, globalImageArray, max_x, max_y, xscale, yscale
    if(globalImageArray != None):
        draw_scale = int(newsize)
        max_x = int(1600/draw_scale)
        max_y = int(1000/draw_scale)
        xscale.config(to=max_x)
        yscale.config(to=max_y)
        canvas.config(width=max_x*draw_scale, height=max_y*draw_scale)
        imagearray = globalImageArray
        imagelist = imagearray.toImageList(size=draw_scale)
        img = imagelist.getImageTkList()
        coords = imagelist.getCoordList()
        for i in range(len(img)):
            canvas.create_image(coords[i][0], coords[i][1], image=img[i], anchor="nw")

def insertCustomframe_lb(element):
    for i in range(customframe_lb.size()):
        lookat = customframe_lb.get(i)
        if(lookat.split("x ", maxsplit=1)[1] == element):
            lookat = lookat.split("x", maxsplit=1)
            currentCount = int(lookat[0])
            newentry = str(currentCount+1) + "x" + "".join(lookat[1:])
            customframe_lb.delete(i)
            customframe_lb.insert(i, newentry)
            return
    customframe_lb.insert("end", "1x " + element)

def removeCustomframe_lb(index):
    lookat = customframe_lb.get(index).split("x", maxsplit=1)
    currentCount = int(lookat[0])
    if(currentCount == 1):
        customframe_lb.delete(index)
    else:
        newentry = str(currentCount-1) + "x" + "".join(lookat[1:])
        customframe_lb.delete(index)
        customframe_lb.insert(index, newentry)
        return

def selectCustom(evt):
    if(len(selectableframe_lb.curselection()) == 0):
        return
    name = selectableframe_lb.get(selectableframe_lb.curselection()[0])
    high_prio.append("custom_modules/"+name+".png")
    #customframe_lb.insert("end", name)
    insertCustomframe_lb(name)
    customexplanation_update()

def selectAll():
    selectable_customs = os.listdir("custom_modules")
    selectable_customs = filter(lambda x: x.endswith(".png"), selectable_customs)
    for selectable_custom in selectable_customs:
        name = selectable_custom[:-4]
        high_prio.append("custom_modules/"+selectable_custom)
        insertCustomframe_lb(name)
    customexplanation_update()

def deselectSelectedCustom(verbose=False):
    if(len(customframe_lb.curselection()) == 0):
        return
    clicked_index = customframe_lb.curselection()[0]
    clicked = customframe_lb.get(clicked_index).split("x ", maxsplit=1)[1]
    removeCustomframe_lb(clicked_index)
    #customframe_lb.delete(clicked_index)
    customframe_preview_canvas.delete("all")
    customframe_preview_canvas.create_text(5, 2, text="Preview", anchor="nw")
    if verbose: print(high_prio, clicked)
    for t in high_prio:
        if (t == "custom_modules/"+clicked+".png"):
            high_prio.remove(t)
            if verbose: print("removed: " + str(t))
            break
    customexplanation_update()

def clearHighPrio():
    global high_prio
    high_prio = []
    customexplanation_update()
    customframe_lb.delete(0, "end")
    customframe_preview_canvas.delete("all")
    customframe_preview_canvas.create_text(5, 2, text="Preview", anchor="nw")

def customframe_lb_click(evt):
    if(len(customframe_lb.curselection()) == 0):
        return
    global img
    clicked = customframe_lb.get(customframe_lb.curselection()[0]).split("x ", maxsplit=1)[1]
    img = ImageTk.PhotoImage(Image.open("custom_modules/"+clicked+".png").resize((100,100)))
    customframe_preview_canvas.create_image(0, 0, image=img, anchor="nw")
    #load connections from json (if none, default is used) (for preview)
    name = clicked
    drawConnectionsPreview(name)

def drawConnectionsPreview(name):
    path = "custom_modules/"+name+".json"
    connections = Module_connections()
    connections.load(path)
    connections_preview.delete("all")
    if(connections.getStreetLocation(0)):
        connections_preview.create_rectangle(20, 10, 30, 20, fill="black")
    if(connections.getStreetLocation(1)):
        connections_preview.create_rectangle(10, 0, 20, 10, fill="black")
    if(connections.getStreetLocation(2)):
        connections_preview.create_rectangle(0, 10, 10, 20, fill="black")
    if(connections.getStreetLocation(3)):
        connections_preview.create_rectangle(10, 20, 20, 30, fill="black")
    if(connections.getStreetLocation(0, getCorner=True)):
        connections_preview.create_rectangle(20, 0, 30, 10, fill="black")
    if(connections.getStreetLocation(1, getCorner=True)):
        connections_preview.create_rectangle(0, 0, 10, 10, fill="black")
    if(connections.getStreetLocation(2, getCorner=True)):
        connections_preview.create_rectangle(0, 20, 10, 30, fill="black")
    if(connections.getStreetLocation(3, getCorner=True)):
        connections_preview.create_rectangle(20, 20, 30, 30, fill="black")

def showConnections():
    if(len(customframe_lb.curselection()) == 0):
        return
    global imgConnections
    clicked = (customframe_lb.get(customframe_lb.curselection()[0])).split("x ", maxsplit=1)[1]
    connectionsWindow = Toplevel(window)
    connectionsWindow.title("Connections")
    connectionsWindow.geometry("1000x1000")
    #load connections from json (if none, default is used)
    path = "custom_modules/"+clicked+".json"
    connections = Module_connections()
    connections.load(path)
    #initVars
    street_right = BooleanVar()
    street_top = BooleanVar()
    street_left = BooleanVar()
    street_bottom = BooleanVar()
    corner_right = BooleanVar()
    corner_top = BooleanVar()
    corner_left = BooleanVar()
    corner_bottom = BooleanVar()
    custom_right = StringVar()
    custom_top = StringVar()
    custom_left = StringVar()
    custom_bottom = StringVar()
    key_right = StringVar()
    key_top = StringVar()
    key_left = StringVar()
    key_bottom = StringVar()
    custom_right_important = BooleanVar()
    custom_top_important = BooleanVar()
    custom_left_important = BooleanVar()
    custom_bottom_important = BooleanVar()
    #setVars
    street_right.set(connections.getStreetLocation(0))
    street_top.set(connections.getStreetLocation(1))
    street_left.set(connections.getStreetLocation(2))
    street_bottom.set(connections.getStreetLocation(3))
    corner_right.set(connections.getStreetLocation(0, getCorner=True))
    corner_top.set(connections.getStreetLocation(1, getCorner=True))
    corner_left.set(connections.getStreetLocation(2, getCorner=True))
    corner_bottom.set(connections.getStreetLocation(3, getCorner=True))
    custom_right.set(connections.streetLocations.custom[0])
    custom_top.set(connections.streetLocations.custom[1])
    custom_left.set(connections.streetLocations.custom[2])
    custom_bottom.set(connections.streetLocations.custom[3])
    key_right.set(connections.streetLocations.getKey(0))
    key_top.set(connections.streetLocations.getKey(1))
    key_left.set(connections.streetLocations.getKey(2))
    key_bottom.set(connections.streetLocations.getKey(3))
    custom_right_important.set(connections.streetLocations.getCustomImportant(0))
    custom_top_important.set(connections.streetLocations.getCustomImportant(1))
    custom_left_important.set(connections.streetLocations.getCustomImportant(2))
    custom_bottom_important.set(connections.streetLocations.getCustomImportant(3))


    def exit_connectionsWindow():
        if(len(custom_right.get()) != 16 or len(custom_top.get()) != 16 or len(custom_left.get()) != 16 or len(custom_bottom.get()) != 16):
            status["text"] = "A custom entry has not the lenght 16!"
            rightlabel["text"] = str(len(custom_right.get()))
            toplabel["text"] = str(len(custom_top.get()))
            leftlabel["text"] = str(len(custom_left.get()))
            bottomlabel["text"] = str(len(custom_bottom.get()))
        else:
            connections.setStreetLocation(0, street_right.get())
            connections.setStreetLocation(1, street_top.get())
            connections.setStreetLocation(2, street_left.get())
            connections.setStreetLocation(3, street_bottom.get())
            connections.setStreetLocation(0, corner_right.get(), setCorner=True)
            connections.setStreetLocation(1, corner_top.get(), setCorner=True)
            connections.setStreetLocation(2, corner_left.get(), setCorner=True)
            connections.setStreetLocation(3, corner_bottom.get(), setCorner=True)
            connections.streetLocations.custom[0] = custom_right.get()
            connections.streetLocations.custom[1] = custom_top.get()
            connections.streetLocations.custom[2] = custom_left.get()
            connections.streetLocations.custom[3] = custom_bottom.get()
            connections.streetLocations.setKey(0, key_right.get())
            connections.streetLocations.setKey(1, key_top.get())
            connections.streetLocations.setKey(2, key_left.get())
            connections.streetLocations.setKey(3, key_bottom.get())
            connections.streetLocations.setCustomImportant(0, custom_right_important.get())
            connections.streetLocations.setCustomImportant(1, custom_top_important.get())
            connections.streetLocations.setCustomImportant(2, custom_left_important.get())
            connections.streetLocations.setCustomImportant(3, custom_bottom_important.get())
            connections.safe(path)
            drawConnectionsPreview(clicked)
            connectionsWindow.destroy()

    #checkbuttons
    Checkbutton(connectionsWindow, variable=street_right).grid(column=4, row=2)
    Checkbutton(connectionsWindow, variable=street_top).grid(column=2, row=0)
    Checkbutton(connectionsWindow, variable=street_left).grid(column=0, row=2)
    Checkbutton(connectionsWindow, variable=street_bottom).grid(column=2, row=4)
    Checkbutton(connectionsWindow, variable=corner_right).grid(column=4, row=0)
    Checkbutton(connectionsWindow, variable=corner_top).grid(column=0, row=0)
    Checkbutton(connectionsWindow, variable=corner_left).grid(column=0, row=4)
    Checkbutton(connectionsWindow, variable=corner_bottom).grid(column=4, row=4)
    #frames for customs and keys
    f_right = Frame(connectionsWindow)
    f_right.grid(column=3, row=2)
    f_top = Frame(connectionsWindow)
    f_top.grid(column=2, row=1)
    f_left = Frame(connectionsWindow)
    f_left.grid(column=1, row=2)
    f_bottom = Frame(connectionsWindow)
    f_bottom.grid(column=2, row=3)
    #entries
    Entry(f_right, textvariable=custom_right).pack()
    Label(f_right, text="Custom Connections").pack()
    Checkbutton(f_right, variable=custom_right_important, text="Important").pack()
    ttk.Separator(f_right, orient="horizontal").pack(fill="x")
    Entry(f_right, textvariable=key_right).pack()
    Label(f_right, text="Key").pack()
    Entry(f_top, textvariable=custom_top).pack()
    Label(f_top, text="Custom Connections").pack()
    Checkbutton(f_top, variable=custom_top_important, text="Important").pack()
    ttk.Separator(f_top, orient="horizontal").pack(fill="x")
    Entry(f_top, textvariable=key_top).pack()
    Label(f_top, text="Key").pack()
    Entry(f_left, textvariable=custom_left).pack()
    Label(f_left, text="Custom Connections").pack()
    Checkbutton(f_left, variable=custom_left_important, text="Important").pack()
    ttk.Separator(f_left, orient="horizontal").pack(fill="x")
    Entry(f_left, textvariable=key_left).pack()
    Label(f_left, text="Key").pack()
    Entry(f_bottom, textvariable=custom_bottom).pack()
    Label(f_bottom, text="Custom Connections").pack()
    Checkbutton(f_bottom, variable=custom_bottom_important, text="Important").pack()
    ttk.Separator(f_bottom, orient="horizontal").pack(fill="x")
    Entry(f_bottom, textvariable=key_bottom).pack()
    Label(f_bottom, text="Key").pack()
    #lengthlabels
    rightlabel = Label(f_right, text=len(custom_right.get()))
    rightlabel.pack()
    toplabel = Label(f_top, text=len(custom_top.get()))
    toplabel.pack()
    leftlabel = Label(f_left, text=len(custom_left.get()))
    leftlabel.pack()
    bottomlabel = Label(f_bottom, text=len(custom_bottom.get()))
    bottomlabel.pack()
    #cofirm button
    Button(connectionsWindow, text="Confirm", command=exit_connectionsWindow).grid(row=5, column=0)
    status = Label(connectionsWindow, text="", fg="red")
    status.grid(row=5, column=2)
    #pic
    preview_canvas = Canvas(connectionsWindow, width=512, height=512)
    preview_canvas.grid(column=2, row=2)
    imgConnections = ImageTk.PhotoImage(Image.open("custom_modules/"+clicked+".png").resize((512,512)))
    preview_canvas.create_image(0, 0, image=imgConnections, anchor="nw")
    connectionsWindow.mainloop()

def exportCanvas():
    dir = "export"
    unique_name = 0
    alreadyExported = os.listdir(dir)
    while(True):
        if(not str(unique_name)+".png" in alreadyExported):
            break
        unique_name += 1
    x=window.winfo_rootx()+canvas.winfo_x()
    y=window.winfo_rooty()+canvas.winfo_y()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(dir + "/" + str(unique_name) + ".png")


#FRAME
#selected customs list preview
#mainframe for that
customframe_preview = Frame(menuframe)
customframe_preview.pack()
#canvas
customframe_preview_canvas = Canvas(customframe_preview, width=width, height=width, highlightbackground="black", highlightthickness=2)
customframe_preview_canvas.pack(side=RIGHT)
customframe_preview_canvas.create_text(5, 2, text="Preview", anchor="nw")
#buttons
customframe_buttons = Frame(customframe_preview)
customframe_buttons.pack(side=LEFT)
#remove
img_cancel = ImageTk.PhotoImage(Image.open("icons/cancel.png").resize((30,30)))
customframe_preview_remove = Button(customframe_buttons, image=img_cancel, command=deselectSelectedCustom)
customframe_preview_remove.pack()
#show connections
img_show_connections = ImageTk.PhotoImage(Image.open("icons/streets.png").resize((30,30)))
customframe_preview_show_connections = Button(customframe_buttons, image=img_show_connections, command=showConnections)
customframe_preview_show_connections.pack()
#connections_preview
connections_preview = Canvas(customframe_buttons, height=30, width=30, background="lightgray")
connections_preview.pack()

#FRAME
#selected customs list
customframe = Frame(menuframe)
customframe.pack()
customframe_removeAll = Button(customframe, text="Clear", command=clearHighPrio)
customframe_removeAll.grid(column=0, row=0, sticky=(N,W,E,S))
customframe_lb = Listbox(customframe, height=10, selectmode=SINGLE)
customframe_lb.grid(column=0, row=1, sticky=(N,W,E,S))
customframe_scrollbar = Scrollbar(customframe, orient=VERTICAL, command=customframe_lb.yview)
customframe_scrollbar.grid(column=1, row=1, sticky=(N,S))
customframe_lb['yscrollcommand'] = customframe_scrollbar.set

customframe_lb.bind('<<ListboxSelect>>', customframe_lb_click)

customexplanation = StringVar()

#scale vars
x = IntVar()
y = IntVar()
x.set(1)
y.set(1)

def customexplanation_update():
    global customexplanation
    l = len(high_prio)
    xv = x.get()
    yv = y.get()
    if(xv*yv == 1):
        if(l == 1):
            customexplanation.set(f"{l} custom module selected.\nGrid will generate {xv * yv} module.")
        else:
            customexplanation.set(f"{l} custom modules selected.\nGrid will generate {xv * yv} module.")
    else:
        if(l == 1):
            customexplanation.set(f"{l} custom module selected.\nGrid will generate {xv * yv} modules.")
        else:
            customexplanation.set(f"{l} custom modules selected.\nGrid will generate {xv * yv} modules.")


#scales
xscale = Scale(menuframe, orient="horizontal", from_=1, to=max_x, variable=x, command=lambda x: customexplanation_update())
xscale.pack()
xlabel = Label(menuframe, text="Width")
xlabel.pack()

yscale = Scale(menuframe, orient="horizontal", from_=1, to=max_y, variable=y, command=lambda x: customexplanation_update())
yscale.pack()
ylabel = Label(menuframe, text="Height")
ylabel.pack()



customexplanation_update()
Label(customframe, textvariable=customexplanation).grid(column=0, row=2, sticky=(N,W,E,S))

#generate button
useCustoms = BooleanVar()
consumeCustoms = BooleanVar()
consumeCustoms.set(True)
activateButton = Button(menuframe, text="Generate", command=lambda: drawGrid(x.get(), y.get(), useCustoms.get(), consumeCustoms.get()))
activateButton.pack()
state = StringVar()
statelabel = Label(menuframe, textvariable=state)
statelabel.pack()
Scale(menuframe, orient="horizontal", from_=100, to=10000, resolution=100, variable=max_inits).pack()
Label(menuframe, text="Maximum attempts").pack()
Button(menuframe, text="Export image", command=exportCanvas).pack()
useCustomsCheckbutton = Checkbutton(menuframe, variable=useCustoms, text="Use Custom Connections")
useCustomsCheckbutton.pack()
Checkbutton(menuframe, variable=consumeCustoms, text="Consume Custom Modules").pack()
size_scale = Scale(menuframe, orient="horizontal", from_=32, to=512, resolution=16, command=lambda s: redrawGrid(s))
size_scale.pack()
size_scale.set(draw_scale)

"""
#FRAME
#selectable customs list preview
#mainframe for that
selectable_preview = Frame(menuframe)
selectable_preview.pack()
#canvas
selectable_preview_canvas = Canvas(selectable_preview, width=width, height=width, highlightbackground="black", highlightthickness=2)
selectable_preview_canvas.pack(side=RIGHT)
selectable_preview_canvas.create_text(5, 2, text="Preview", anchor="nw")
#buttons
selectable_buttons = Frame(selectable_preview)
selectable_buttons.pack(side=LEFT)
#add
img_add = ImageTk.PhotoImage(Image.open("icons/add.png").resize((30,30)))
selectable_add = Button(selectable_buttons, image=img_cancel, command=deselectSelectedCustom)
selectable_add.pack()
"""



selectable_customs = os.listdir("custom_modules")
selectable_customs = filter(lambda x: x.endswith(".png"), selectable_customs)

#FRAME
#selected customs list
selectableframe = Frame(menuframe)
selectableframe.pack()
selectableframe_addAll = Button(selectableframe, text=f"Add all once ({len(list(selectable_customs))})", command=selectAll)
selectableframe_addAll.grid(column=0, row=0, sticky=(N,W,E,S))
selectableframe_lb = Listbox(selectableframe, height=10, selectmode=SINGLE)
selectableframe_lb.grid(column=0, row=1, sticky=(N,W,E,S))
selectableframe_scrollbar = Scrollbar(selectableframe, orient=VERTICAL, command=selectableframe_lb.yview)
selectableframe_scrollbar.grid(column=1, row=1, sticky=(N,S))
selectableframe_lb['yscrollcommand'] = selectableframe_scrollbar.set

selectableframe_lb.bind('<<ListboxSelect>>', selectCustom)


#custom module list
selectable_customs = os.listdir("custom_modules")
selectable_customs = filter(lambda x: x.endswith(".png"), selectable_customs)
for selectable_custom in selectable_customs:
    selectableframe_lb.insert("end", selectable_custom[:-4])

#unselected_imagelist.append(ImageTk.PhotoImage(Image.open("custom_modules/"+custom).resize((30,30))))

#Button(frame, image=unselected_imagelist[i], command=lambda c=custom: selectCustom(c)).pack(side=LEFT)



window.geometry(str(width+max_x*128) + "x" + str(max_y*128))
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))
window.mainloop()
