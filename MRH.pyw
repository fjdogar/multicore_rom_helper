import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import frogtool_mod

class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master: tk.Tk = master
        self.pack(anchor="w")
        self.create_widgets()

        # Create frame for header
        self.header_frame = tk.Frame(self.master)
        self.header_frame.pack(anchor="w")

        # Create frame for ZFB File creation
        self.frame = tk.Frame(self.master)
        self.frame.pack(anchor="w")

        # Create bold font for label
        bold_font = ("Helvetica", 10, "bold")
        label_font = ("Helvetica", 10, "normal")

        instructions_text = "Select the Working Directory"

        # Instructions
        self.header_label = tk.Label(self.header_frame, text=instructions_text, font=bold_font)
        self.header_label.pack()




        # Input Folder - Label
        self.input_folder_label = tk.Label(self.frame, text="Working Directory: ", font=label_font)
        self.input_folder_label.grid(row=0, column=0, sticky="w")

        # Input Folder - Input box
        self.input_folder_var = tk.StringVar()
        self.input_folder_entry = tk.Entry(self.frame, textvariable=self.input_folder_var, width=50)
        self.input_folder_entry.grid(row=0, column=1, sticky="w")

        #edit
        self.input_folder_var.set(os.getcwd())
        #edit

        # Input Folder - Browse button
        self.input_folder_button = tk.Button(self.frame, text="Browse", command=self.select_input_folder)
        self.input_folder_button.grid(row=0, column=2, sticky="w")




        self.mdir_label = tk.Label(self.frame, text = "Select the Multicore Dir :", 
          font = ("Times New Roman", 10)).grid(column = 0, row = 2, sticky="w")

        self.mdirselected = tk.StringVar()
        self.mdir = ttk.Combobox(self.frame, width = 45, textvariable = self.mdirselected) 
    
        
        
        # Adding combobox drop down list 
        
        
        self.build_mdirs()

        

        
        self.mdir.grid(column = 1, row = 2 , sticky="w") 
        self.mdir.current()

        self.sdir_label = tk.Label(self.frame, text = "Select the Stock Dir :", 
          font = ("Times New Roman", 10)).grid(column = 0, row = 4, sticky="w")

        self.sdirselected = tk.StringVar()
        self.sdir = ttk.Combobox(self.frame, width = 45, textvariable = self.sdirselected) 
        


        # Adding combobox drop down list 
        self.sdir['values'] = (' ARCADE',  
                                  ' FC', 
                                  ' SFC', 
                                  ' GB', 
                                  ' GBC', 
                                  ' GBA', 
                                  ' SEGA') 
          
        self.sdir.grid(column = 1, row = 4 , sticky="w") 
        self.sdir.current(5)


        self.pdir_label = tk.Label(self.frame, text = "Placeholder", font = ("Times New Roman", 10)).grid(column = 0, row = 5, sticky="w")

        self.pdirselected = tk.StringVar()
        self.pdir = ttk.Combobox(self.frame, width = 45, textvariable = self.pdirselected)
        self.pdir.grid(column = 1, row = 5 , sticky="w")
    
        
        
        # Adding combobox drop down list 
        
        
        self.build_pfiles()
        print(self.sdir.current())

        

        
        """
        # Output Folder - Label
        self.output_folder_label = tk.Label(self.frame, text="Output Folder: ", font=label_font)
        self.output_folder_label.grid(row=3, column=0, sticky="w")

        # Output Folder - Input box
        self.output_folder_var = tk.StringVar()
        self.output_folder_entry = tk.Entry(self.frame, textvariable=self.output_folder_var, width=70)
        self.output_folder_entry.grid(row=3, column=1, sticky="w")

        # Output Folder - Browse button
        self.output_folder_button = tk.Button(self.frame, text="Browse", command=self.select_output_folder)
        self.output_folder_button.grid(row=3, column=2, sticky="w")

        # Core Label
        self.core_label = tk.Label(self.frame, text="CORE: ", font=label_font)
        self.core_label.grid(row=4, column=0, sticky="w")

        # Core Input box
        self.core_var = tk.StringVar()
        self.core_entry = tk.Entry(self.frame, textvariable=self.core_var, width=70)
        self.core_entry.grid(row=4, column=1, sticky="w")

        # Extension Label
        self.extension_label = tk.Label(self.frame, text="EXTENSION: ", font=label_font)
        self.extension_label.grid(row=4, column=0, sticky="w")

        # Extension Input box
        self.extension_var = tk.StringVar()
        self.extension_entry = tk.Entry(self.frame, textvariable=self.extension_var, width=70)
        self.extension_entry.grid(row=5, column=1, sticky="w")


        
        """

        # Create STUB Files button
        self.create_stub_button = tk.Button(self.frame, text="Create STUB Files", command=self.create_stub_files,
                                           font=("Helvetica", 14))
        self.create_stub_button.grid(row=6, column=1)


        # Create ZFB Files button
        self.create_zfb_button = tk.Button(self.frame, text="Create ZFB Files", command=self.create_zfb_files,
                                           font=("Helvetica", 14))
        self.create_zfb_button.grid(row=7, column=1)

    def create_widgets(self):
        # Menu bar creation
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.exit_handler)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.master.config(menu=self.menubar)

    def create_stub_files(self):
        core = self.mdirselected.get()
        core = core.strip()
        wdir = self.input_folder_var.get()
        romdir = wdir + "\\ROMS\\" + core

        if not wdir or not romdir or not core: #or not extension:
                messagebox.showwarning('Warning', 'Please fill in all the fields and select multicore rom directory')
                return

        for rom in os.listdir(romdir):
            with open(os.path.join(wdir,"ROMS",f"{core};{rom}.gba"), 'w'): 
                pass

        messagebox.showinfo("Hello" , "STUBS created")

    def build_mdirs(self):
        wdir = self.input_folder_var.get()
        self.mdir.set("")

        #subdir = "\\ROMS"       
        try:
            self.mdir['values'] = [f.name for f in os.scandir(wdir +"\\ROMS") if f.is_dir() and f.name != "save" and f.name != "mnt" ]
            self.mdir.current(0)
        except:
            messagebox.showwarning('Warning', 'No multicore ROMS folder found in current Working Directory')
            self.mdir['values'] = []
            self.mdir.current()
        #print(mdir.get())

    def build_pfiles(self):

        if not os.path.isdir('placeholders'):
            os.makedirs("placeholders")
        wdir = self.input_folder_var.get()
        self.pdir.set("")

        #subdir = "\\ROMS"
        imgtypes = (".jpg" , ".png" , ".bmp")       
        #try:
        self.pdir['values'] = [f.name for f in os.scandir(wdir +"\\placeholders") if not f.is_dir() and f.name.lower().endswith(imgtypes) ]
            #self.pdir.current(0)
        
        if not self.pdir['values']:
            messagebox.showwarning('Warning', 'No Placeholder files found in Placeholder Directory')
            #self.pdir['values'] = []
            #self.pdir.current()

        #self.pdir.append("Dont Use Placeholder")

        noph = ["Dont Use Placeholder"]

        current_values = list(self.pdir['values'])
        self.pdir['values'] = noph + current_values
        self.pdir.current(0)
        

    def exit_handler(self):
        os._exit(0)

    def select_input_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_folder_var.set(folder_path)
        else:
            self.input_folder_var.set(os.getcwd())

        self.build_mdirs()            

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_var.set(folder_path)

    def rebuildAll(self):
        frogtool.run(self.input_folder_var.get(), "ALL", "-sc")
        return

    def create_zfb_files(self):

        sdir = self.sdirselected.get()
        pdir = self.pdirselected.get()
        core = self.mdirselected.get()

        sdir = sdir.strip()
        core = core.strip()
        pdir = pdir.strip()

        try:
            input_fold = self.input_folder_var.get()
            
            #output_folder = self.output_folder_var.get()
            output_folder = input_fold + "\\" +  sdir

            
            #edit
            input_folder = os.path.join(input_fold , "ROMS\\" + core)
            #edit

            print(output_folder)

            #core = self.core_var.get()
            #extension = self.extension_var.get()


            if not os.path.isdir(output_folder):
                tdq = messagebox.askquestion('Stock Directory', 'Selected Stock Folder doesnt Exist , Do you want to Create it?')
                if tdq == "yes":
                    os.makedirs(output_folder)
                    messagebox.showinfo("Directory" , "Directory Created")
                else:
                    return
            # Check if folders are selected
            if not input_folder or not output_folder or not core: #or not extension:
                messagebox.showwarning('Warning', 'Please fill in all the fields and select multicore rom dir and Stock dir.')
                return

            thumb_size = (144, 208)

            rom_list = [];

            # Iterate over all files in the input folder
            for file_name in os.listdir(input_folder):
                

                file_path = os.path.join(input_folder, file_name)
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                #print(file_path)

                #if file_name in rom_list:
                 #   continue
                try:
                    # Attempt to open the file as an image
                    with Image.open(file_path) as img:

                        rom_list.append(file_name)
                        
                        zfb_from_image(img , input_folder , core ,  file_name , output_folder )

                except Exception as img_error:

                    
                    tfp = input_fold + "\\placeholders\\" + pdir
                    print("the placeholder dir n file is " + tfp)
                    try:
                        with Image.open(tfp) as img:

                            print("using the placeholder " + pdir)
                        
                            zfb_from_image(img , input_folder , core ,  file_name , output_folder )

                    except:


                        print("Not using placeholder " + pdir)
                        placeholder_data = b'\x00' * 0xEA00 + b'\x00\x00\x00\x00' + f"{core};{file_name}.gba".encode('utf-8') + b'\x00\x00'
                        #zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')
                        zfb_filename = os.path.join(output_folder , file_name + '.zfb')
                        print(os.path.splitext(file_name)[0])
                        with open(zfb_filename, 'wb') as zfb:
                            zfb.write(placeholder_data)

            messagebox.showinfo('Success', 'ZFB files created successfully.')
            #self.rebuildAll()
            #messagebox.showinfo('Roms Refresh', 'All Rom lists have been refreshed.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while creating the ZFB files: {str(e)}')

    def zfb_from_image(img , input_folder , core ,  file_name , output_folder):
        img = img.resize(thumb_size)
        img = img.convert("RGB")

        raw_data = []

        # Convert image to RGB565
        for y in range(thumb_size[1]):
            for x in range(thumb_size[0]):
                r, g, b = img.getpixel((x, y))
                rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                raw_data.append(struct.pack('H', rgb))

        raw_data_bytes = b''.join(raw_data)

        # Create .zfb filename
        #zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')

        zfb_filename = os.path.join(output_folder , file_name + '.zfb')

        # Write the image data to the .zfb file
        with open(zfb_filename, 'wb') as zfb:
            # Fill with 00 bytes until offset 0xEA00
            zfb.write(raw_data_bytes)
            zfb.write(b'\x00\x00\x00\x00')  # Write four 00 bytes
            #zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))  # Write the modified filename
            
            zfb.write(f"{core};{filename}.gba".encode('utf-8'))  # Write the modified filename

            zfb.write(b'\x00\x00')  # Write two 00 bytes

# Create the application window
root = tk.Tk()
root.geometry("550x200")
root.resizable(False, False)
root.title("Multicore Rom Helper")

app = Application(master=root)

# Redefine the window's close button to trigger the custom exit handler
root.protocol("WM_DELETE_WINDOW", app.exit_handler)

# Start the application
app.mainloop()
