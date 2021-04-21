from tkinter import *
import os
import tkinter.filedialog
import tkinter.messagebox
from tkinter import messagebox
from difflib import SequenceMatcher
from tkinter import filedialog
import pyttsx3
import time
from tkinter.font import Font, families
from tkinter import font
from PIL import Image
import cv2 as cv


#all codes goes here

#splash screen
splash_screen=Tk()
app_width = 430
app_height = 430

screen_width = splash_screen.winfo_screenwidth()
screen_height = splash_screen.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)

splash_screen.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
#splash_screen.geometry("430x430")
splash_screen.overrideredirect(True)
splashfile=PhotoImage(file="splash.png")
splashFrame=Label(splash_screen,width=400,height=400,image=splashfile)
splashFrame.place(x=0,y=0,relwidth=1,relheight=1)


def mainWindow():
    splash_screen.destroy()
    root = Tk()
    root.iconbitmap('icon.ico')

    PROGRAM_NAME = "TextEditor"
    root.title(PROGRAM_NAME)
    file_name = None
    _width = 1200
    _height = 600

    root_width = root.winfo_screenwidth()
    root_height = root.winfo_screenheight()

    x = (root_width / 2) - (_width / 2)
    y = (root_height / 2) - (_height / 2)

    root.geometry(f'{_width}x{_height}+{int(x)}+{int(y)}')
    #root.geometry('800x400')
    #FILE MENU
    def new_file(event=None):
        root.title("Untitled")
        global file_name
        file_name = None
        content_text.delete(1.0, END)
        on_content_changed()

    def open_file(event=None):
        input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("HTML", "*.html"),("CSS", "*.css"),("JavaScript", "*.js")])
        if input_file_name:
            global file_name
            file_name = input_file_name
            root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
            content_text.delete(1.0, END)
            with open(file_name) as _file:
                content_text.insert(1.0, _file.read())

        on_content_changed()

    def write_to_file(file_name):
        try:
            content = content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass


    def save_as(event=None):
        input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("HTML", "*.html"),("CSS", "*.css"),("JavaScript", "*.js")])
        if input_file_name:
            global file_name
            file_name = input_file_name
            write_to_file(file_name)
            root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        return "break"


    def save(event=None):
        global file_name
        if not file_name:
            save_as()
        else:
            write_to_file(file_name)
        return "break"

    # Compare files
    def compare_files():
        file1 = filedialog.askopenfilename(initialdir="C:/gui/", title="Choose File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

        text_file1 = open(file1, 'r')

        file1_data = text_file1.read()
        file2_data = content_text.get(1.0,END)
        similarity = SequenceMatcher(None, file1_data, file2_data).ratio()
        messagebox.showinfo("Plagiarism", f"The contents are {similarity * 100:.3f}% common.")

    #EDIT MENU
    def cut():
        content_text.event_generate("<<Cut>>")
        on_content_changed()
        return "break"
    def copy():
        content_text.event_generate("<<Copy>>")
        on_content_changed()
        return "break"
    def paste():
        content_text.event_generate("<<Paste>>")
        on_content_changed()
        return "break"

    def undo():
        content_text.event_generate("<<Undo>>")
        on_content_changed()
        return "break"

    def redo(event=None):
        content_text.event_generate("<<Redo>>")
        on_content_changed()
        return "break"

    def selectall(event=None):
        content_text.tag_add('sel','1.0','end')
        return "break"


    def find_text(event=None):
        search_toplevel = Toplevel(root)
        search_toplevel.title('Find Text')
        search_toplevel.transient(root)
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        ignore_case_value = IntVar()
        Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
        Button(search_toplevel, text="Find All", underline=0,
               command=lambda: search_output(
                   search_entry_widget.get(), ignore_case_value.get(),
                   content_text, search_toplevel, search_entry_widget)
               ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

        def close_search_window():
            content_text.tag_remove('match', '1.0', END)
            search_toplevel.destroy()
        search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
        return "break"

    def search_output(needle,if_ignore_case, content_text, search_toplevel, search_box):
        content_text.tag_remove('match','1.0', END)
        matches_found=0
        if needle:
            start_pos = '1.0'
            while True:
                start_pos = content_text.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
                if not start_pos:
                    break

                end_pos = '{} + {}c'. format(start_pos, len(needle))
                content_text.tag_add('match', start_pos, end_pos)
                matches_found +=1
                start_pos = end_pos
            content_text.tag_config('match', background='yellow', foreground='blue')
        search_box.focus_set()
        search_toplevel.title('{} matches found'.format(matches_found))

    #function for text to speech
    def text_to_speech():
        mytext = content_text.get(1.0,END)
        # Language in which you want to convert
        # init function to get an engine instance for the speech synthesis
        engine = pyttsx3.init()

        # say method on the engine that passing input text to be spoken
        engine.say(mytext)

        # run and wait method, it processes the voice commands.
        engine.runAndWait()

    def importAudioFlie():

        # Create a string
        string = content_text.get(1.0,END)

        # Initialize the Pyttsx3 engine
        engine = pyttsx3.init()

        # We can use file extension as mp3 and wav, both will work
        engine.save_to_file(string, 'speech.mp3')

        # Wait until above command is not finished.
        engine.runAndWait()
        messagebox.showinfo("Audio Imported", "Your audio file has been imported.")


    def addDate():
        full_date = time.localtime()
        day = str(full_date.tm_mday)
        month = str(full_date.tm_mon)
        year = str(full_date.tm_year)
        date = day + '/' + month + '/' + year
        content_text.insert(INSERT, date, "a")

    # Bold Text
    def bold_it(e):
        # Create our font
        try:
            if e:
                content_text.event_generate("<<Cut>>")
                on_content_changed()
                return "break"
            bold_font = font.Font(content_text, content_text.cget("font"))
            bold_font.configure(weight="bold")

            # Configure a tag
            content_text.tag_configure("bold", font=bold_font)

            # Define Current tags
            current_tags = content_text.tag_names("sel.first")

            # If statment to see if tag has been set
            if "bold" in current_tags:
                content_text.tag_remove("bold", "sel.first", "sel.last")
            else:
                content_text.tag_add("bold", "sel.first", "sel.last")

        except Exception:
            pass


    # Italics Text
    def italics_it():
        # Create our font
        try:
            italics_font = font.Font(content_text, content_text.cget("font"))
            italics_font.configure(slant="italic")

            # Configure a tag
            content_text.tag_configure("italic", font=italics_font)

            # Define Current tags
            current_tags = content_text.tag_names("sel.first")

            # If statment to see if tag has been set
            if "italic" in current_tags:
                content_text.tag_remove("italic", "sel.first", "sel.last")
            else:
                content_text.tag_add("italic", "sel.first", "sel.last")
        except Exception:
            pass

    def insertImage():
        select_image = filedialog.askopenfilename(title="Select your image",filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg")])
        global img
        img = PhotoImage(file=select_image)
        content_text.image_create(END, image=img)
        #content_text.window_create(tk.END, window=tk.Label(text, image=select_image))  # Example 2

    def insertCartoon():
        try:
            select_photo = filedialog.askopenfilename(title="Select you Photo",filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg")])

            cartoon=cv.imread(select_photo)
            gray_image=cv.cvtColor(cartoon, cv.COLOR_BGR2GRAY)
            blur_image=cv.GaussianBlur(gray_image, (3,3),0)
            edge_image=cv.adaptiveThreshold(blur_image,255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,5,3)

            output=cv.bitwise_and(cartoon,cartoon,mask=edge_image)
            cv.imshow(select_photo, output)
            cv.waitKey(0)
            if tkinter.messagebox.askyesno("Save", "Do you want to save your cartooned image?"):
                input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg")])
                if input_file_name:
                    cv.imwrite(input_file_name, output)
                    cv.destroyAllWindows()
                
        except Exception:
            pass

    def overstrike():
        """Toggles overstrike for selected text."""
        try:
            current_tags = content_text.tag_names("sel.first")
            if "overstrike" in current_tags:
                content_text.tag_remove("overstrike", "sel.first", "sel.last")
            else:
                content_text.tag_add("overstrike", "sel.first", "sel.last")
                overstrike_font = Font(content_text, content_text.cget("font"))
                overstrike_font.configure(overstrike=1)
                content_text.tag_configure("overstrike", font=overstrike_font)
        except:
            pass
    #ABOUT MENU

    def display_about(event=None):
        tkinter.messagebox.showinfo(
            "About", PROGRAM_NAME + "\nA Simple Text Editor made in Python with Tkinter\n -Tanishka\n -Ishika Khandelwal")


    def display_help(event=None):
        tkinter.messagebox.showinfo(
            "Help", "This Text Editor works similar to any other editors.",
            icon='question')


    def exit_editor(event=None):
        if tkinter.messagebox.askokcancel("Exit", "Are you sure you want to Quit?"):
            root.destroy()

    #adding Line Numbers Functionality
    def get_line_numbers():
        output = ''
        if show_line_number.get():
            row, col = content_text.index("end").split('.')
            for i in range(1, int(row)):
                output += str(i) + '\n'
        return output

    def on_content_changed(event=None):
        update_line_numbers()
        update_cursor()

    def update_line_numbers(event=None):
        line_numbers = get_line_numbers()
        line_number_bar.config(state='normal')
        line_number_bar.delete('1.0', 'end')
        line_number_bar.insert('1.0', line_numbers)
        line_number_bar.config(state='disabled')

    # Adding Cursor Functionality
    def show_cursor():
        show_cursor_info_checked = show_cursor_info.get()
        if show_cursor_info_checked:
            cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
        else:
            cursor_info_bar.pack_forget()


    def update_cursor(event=None):
        row, col = content_text.index(INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
        infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
        cursor_info_bar.config(text=infotext)


    #Adding Text Highlight Functionality
    def highlight_line(interval=100):
        content_text.tag_remove("active_line", 1.0, "end")
        content_text.tag_add(
            "active_line", "insert linestart", "insert lineend+1c")
        content_text.after(interval, toggle_highlight)


    def undo_highlight():
        content_text.tag_remove("active_line", 1.0, "end")


    def toggle_highlight(event=None):
        if to_highlight_line.get():
            highlight_line()
        else:
            undo_highlight()


    #Adding Change Theme Functionality
    def change_theme(event=None):
        selected_theme = theme_choice.get()
        fg_bg_colors = color_schemes.get(selected_theme)
        foreground_color, background_color = fg_bg_colors.split('.')
        content_text.config(
            background=background_color, fg=foreground_color)

    #pop-up menu
    def show_popup_menu(event):
        popup_menu.tk_popup(event.x_root, event.y_root)



    # ICONS for the compound menu
    global new_file_icon
    global open_file_icon
    global save_file_icon
    global cut_icon
    global copy_icon
    global paste_icon
    global undo_icon
    global redo_icon
    global find_icon
    new_file_icon = PhotoImage(file='icons/new_file.gif')
    open_file_icon = PhotoImage(file='icons/open_file.gif')
    save_file_icon = PhotoImage(file='icons/save.gif')
    cut_icon = PhotoImage(file='icons/cut.gif')
    copy_icon = PhotoImage(file='icons/copy.gif')
    paste_icon = PhotoImage(file='icons/paste.gif')
    undo_icon = PhotoImage(file='icons/undo.gif')
    redo_icon = PhotoImage(file='icons/redo.gif')
    find_icon = PhotoImage(file='icons/find_text.gif')


    #MENU CODES GOES HERE
    menu_bar = Menu(root) #menu begins

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', image=new_file_icon, underline=0, command=new_file)
    file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', image=open_file_icon, underline=0, command=open_file)
    file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left', image=save_file_icon, underline=0, command=save)
    file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S', compound='left', underline=0, command = save_as)
    file_menu.add_separator()
    file_menu.add_command(label="Compare File", command=compare_files)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", accelerator='Alt+F4', compound='left', underline=0, command=exit_editor)
    menu_bar.add_cascade(label='File', menu=file_menu)
    # end of File Menu

    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label='Undo', accelerator='Ctrl + Z', compound='left', image=undo_icon, underline=0, command=undo)
    edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', image=redo_icon, underline=0, command=redo)
    edit_menu.add_separator()
    edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left',  image=cut_icon, underline=0, command=cut)
    edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left', image=copy_icon, underline=0, command=copy)
    edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',  image=paste_icon, underline=0, command=paste)
    edit_menu.add_separator()
    edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left',  image=find_icon, underline=0, command=find_text)
    edit_menu.add_separator()
    edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound='left', underline=0, command=selectall)
    menu_bar.add_cascade(label='Edit', menu=edit_menu)
    #end of Edit Menu

    insert_menu = Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label="Insert", menu=insert_menu)
    insert_menu.add_command(label="Bold", command=bold_it, accelerator='Ctrl+B',compound='left', underline=0)
    insert_menu.add_command(label="Italic", command=italics_it, accelerator='Ctrl+I',compound='left', underline=0)
    insert_menu.add_separator()
    insert_menu.add_command(label="Insert Image",compound='left',command=insertImage)

    insert_menu.add_command(label="Add Date", command=addDate)
    #end of Insert Menu

    # Add Speech menu
    speech_menu = Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label="Speech", menu=speech_menu)
    speech_menu.add_command(label="Text to Speech", command=text_to_speech)
    speech_menu.add_command(label="Import Audio", command=importAudioFlie)

    view_menu = Menu(menu_bar, tearoff=0)
    show_line_number=IntVar()
    show_line_number.set(1)
    view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number)
    show_cursor_info=IntVar()
    show_cursor_info.set(1)
    view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor)
    to_highlight_line=IntVar()
    view_menu.add_checkbutton(label='Highlight Current Line', variable=to_highlight_line, onvalue=1, offvalue=0,command=toggle_highlight)
    view_menu.add_command(label="View Your Cartoon", compound='left', command=insertCartoon)
    view_menu.add_separator()
    themes_menu=Menu(menu_bar, tearoff=0)
    view_menu.add_cascade(label='Themes', menu=themes_menu, command=change_theme)

    ''' THEMES OPTIONS'''
    color_schemes = {
        'Default': '#000000.#FFFFFF',
        'Greygarious': '#83406A.#D1D4D1',
        'Aquamarine': '#5B8340.#D1E7E0',
        'Bold Beige': '#4B4620.#FFF0E1',
        'Cobalt Blue': '#ffffBB.#3333aa',
        'Olive Green': '#D1E7E0.#5B8340',
        'Night Mode': '#FFFFFF.#000000',
    }

    theme_choice=StringVar()
    theme_choice.set('Default')
    for k in sorted(color_schemes):
        themes_menu.add_radiobutton(label=k, variable=theme_choice, command=change_theme)

    menu_bar.add_cascade(label='View', menu=view_menu)


    #start of About Menu
    about_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='About', menu=about_menu)
    about_menu.add_command(label='About', underline=0, command=display_about)
    about_menu.add_command(label='Help', underline=0, command=display_help)
    #end of About Menu
    root.config(menu=menu_bar)

    #adding top shortcut bar and left line number bar
    shortcut_bar=Frame(root, height=25)
    shortcut_bar.pack(expand='no', fill='x')

    #adding shortcut icons
    icons=('new_file', 'open_file', 'save', 'cut', 'copy', 'paste','undo', 'redo', 'find_text')
    for i, icon in enumerate(icons):
        tool_bar_icon = PhotoImage(file='icons/{}.gif'.format(icon)).zoom(2,2)
        cmd = eval(icon)
        tool_bar = Button(shortcut_bar, image=tool_bar_icon, height=35,width=35, command=cmd,cursor="hand2")
        tool_bar.image = tool_bar_icon
        tool_bar.pack(side='left')


    line_number_bar = Text(root, width=4, padx=3, takefocus=0, fg='white', border=0, background='#282828', state='disabled',  wrap='none')
    line_number_bar.pack(side='left', fill='y')

    #adding the main context Text widget and Scrollbar Widget
    content_text = Text(root, wrap='word')
    content_text.pack(expand='yes', fill='both')

    scroll_bar = Scrollbar(content_text)
    content_text.configure(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=content_text.yview)
    scroll_bar.pack(side='right', fill='y')

    # addind cursor info label
    cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
    cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

    # setting up the pop-up menu
    popup_menu = Menu(content_text)
    for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
        cmd = eval(i)
        popup_menu.add_command(label=i, compound='left', command=cmd)
    popup_menu.add_separator()
    popup_menu.add_command(label='Select All', underline=7, command=selectall)
    content_text.bind('<Button-3>', show_popup_menu)


    #handling binding

    content_text.bind('<Control-N>', new_file)
    content_text.bind('<Control-n>', new_file)
    content_text.bind('<Control-O>', open_file)
    content_text.bind('<Control-o>', open_file)
    content_text.bind('<Control-S>', save)
    content_text.bind('<Control-s>', save)

    content_text.bind('<Control-Y>',redo)
    content_text.bind('<Control-y>',redo)
    content_text.bind('<Control-A>',selectall)
    content_text.bind('<Control-a>',selectall)
    content_text.bind('<Control-F>',find_text)
    content_text.bind('<Control-f>',find_text)
    content_text.bind("<Control-B>",bold_it)
    content_text.bind("<Control-b>",bold_it)
    content_text.bind("<Control-I>",italics_it)
    content_text.bind("<Control-i>",italics_it)

    content_text.bind('<KeyPress-F1>', display_help)

    content_text.bind('<Any-KeyPress>', on_content_changed)
    content_text.tag_configure('active_line', background='ivory2')

    content_text.bind('<Button-3>', show_popup_menu)
    content_text.focus_set()


    #END OF MENU

    root.protocol('WM_DELETE_WINDOW', exit_editor)

img=PhotoImage(file="icons1/enter2.png")
enterButton= Button(splashFrame,image=img,font=("Helvetica", 16,"bold"),borderwidth=0,relief=GROOVE,bg="#29648A",command=mainWindow,cursor="hand2")
enterButton.pack(side=BOTTOM,anchor=S,pady=10)

mainloop()
