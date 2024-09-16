from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import mrh_ui as mainDialog

import sys
import os
import glob
import requests
import struct

import frogtool_mod
from PIL import Image

class MainDialog(QDialog, mainDialog.Ui_Dialog):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(632, 529)

        basedir = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(os.path.join(basedir, 'icon.png')))


        #icon_path = os.path.join(sys._MEIPASS, 'icon.png')
        self.wdir.setPlainText(os.getcwd())

        self.pdir_root = self.wdir.toPlainText() + "\\placeholders"

        #self.setWindowIcon(QIcon(os.path.join(self.wdir.toPlainText(), 'icon.png')))
        self.build_mdirs()
        self.sdir.addItems(["ARCADE" , "FC" , "SFC" , "GB" , "GBC" , "GBA"  , "MD"])
        self.sdir.setCurrentIndex(5)
        self.build_pfiles()

        self.chk_stub.stateChanged.connect(self.stub_clicked)
        self.chk_refresh.stateChanged.connect(self.refresh_clicked)

        self.btn_wdir.clicked.connect(self.setWorkingDir)
        self.btn_process.clicked.connect(self.doProcess)

        #self.pdir = self.wdir.toPlainText() 


    def stub_clicked(self):
        if(self.chk_stub.isChecked()):
            #self.chk_stub.setCheckState(True)
            self.chk_refresh.setCheckState(False)
            return
        #self.chk_stub.setCheckState(Qt.Checked)
        return

    def refresh_clicked(self):
        if(self.chk_stub.isChecked()):
            self.chk_stub.setCheckState(False)
            return
        #self.chk_refresh.setCheckState(Qt.Checked)
        return


    def setWorkingDir(self):
        wodir = QFileDialog.getExistingDirectory()
        if wodir:
            self.wdir.setPlainText(wodir)
            self.build_mdirs()

    def build_mdirs(self):
        wdir = self.wdir.toPlainText()

        try:
            self.mdir.addItems([f.name for f in os.scandir(wdir +"\\ROMS") if f.is_dir() and f.name != "save" and f.name != "mnt" ])
        except:
            QMessageBox.information(self, "No Rom Directories",'No multicore ROMS folder found in current Root Directory')

        count = self.mdir.count()

        self.mdir.setCurrentIndex(0)


    def build_pfiles(self):

        pdir_root = self.pdir_root
        if not os.path.isdir(pdir_root):
            os.makedirs(pdir_root)
        wdir = self.wdir.toPlainText()
        #self.pdir.set("")

        #subdir = "\\ROMS"
        imgtypes = ("jpg" , "png" , "bmp" , "gif")       
        #try:
        #self.pdir.addItems([f.name for f in os.scandir(wdir +"\\placeholders") if not f.is_dir() and f.name.lower().endswith(imgtypes)] )
            #self.pdir.current(0)
        for f in os.scandir(pdir_root):
            if f.name.lower().endswith(imgtypes):
                self.pdir.addItem(QIcon(f.path) , f.name)
        self.pdir.setIconSize(QSize(59, 85))
        if not self.pdir.count() > 0:
            QMessageBox.information(self,'No Placeholders', 'No Placeholder files found in Placeholder Directory')
            #self.pdir['values'] = []
            #self.pdir.current()

        self.pdir.insertItem(0,"      Dont Use Placeholder")
        self.pdir.setCurrentIndex(0)
        print("pdir selected item is " + self.pdir.currentText().strip())
        """
        noph = ["Dont Use Placeholder"]

        current_values = list(self.pdir['values'])
        self.pdir['values'] = noph + current_values
        self.pdir.current(0)
        """

    def doProcess(self):
        if self.chk_stub.isChecked():
            self.create_stub_files()
        else:
            self.create_zfb_files()

    def find_matching_ext(self,file_name, isRom):
        
        input_fold = self.wdir.toPlainText()
        core = self.mdir.currentText()

        input_folder = os.path.join(input_fold , "ROMS\\" + core)
        
        fnA = file_name.split(".")
        file_name = fnA[0];
        file_ext = fnA[1];

        input_path = input_folder + "\\" + file_name

        files = glob.glob(input_path + ".*" )
        print("path to file is " + input_path)
        print(files)

        for x in glob.glob(input_path + ".*" ):
            fname = os.path.splitext(os.path.basename(x))[0]
            fext = os.path.splitext(x)[1][1:]
            if fext != file_ext:
                if isRom:
                    print("file except png found , extension is " + fext)
                    return fext
                else:
                    if fext in ["bmp" , "png" , "gif" , "jpeg" , "jpg"]:
                        print("file for img found , extension is " + fext)
                        return fext
        
        if not isRom:
            print("Image file not found")
        else:
            print("Rom File not found")
        return False

    def create_stub_files(self):
        core = self.mdir.currentText()
        wdir = self.wdir.toPlainText()
        core = core.strip()
        #wdir = self.input_folder_var.get()
        romdir = wdir + "\\ROMS\\" + core

        if not wdir or not romdir or not core: #or not extension:
                QMessageBox.warning(self,'Warning', 'Please fill in all the fields and select multicore rom directory')
                return

        for rom in os.listdir(romdir):
            re = rom.split(".")[1]
            if re not in ["png" , "gif" , "jpg" , "jpeg" , "gif" , "txt"]:
                with open(os.path.join(wdir,"ROMS",f"{core};{rom}.gba"), 'w'): 
                    pass

        QMessageBox.information(self ,"Processed" , "STUBS created")



    def zfb_from_image(self , img , input_folder , core ,  file_name, output_folder):
        thumb_size = (144, 208)
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
            
            zfb.write(f"{core};{file_name}.gba".encode('utf-8'))  # Write the modified filename
            print(f"Shortcut is : {core};{file_name}.gba")
            zfb.write(b'\x00\x00')  # Write two 00 bytes

    def create_zfb_files(self):

        sdir = self.sdir.currentText()
        print("stock dir is " + sdir)
        pdir = self.pdir.currentText().strip()
        core = self.mdir.currentText()

        sdir = sdir.strip()
        core = core.strip()
        pdir = pdir.strip()

        rom_ext = False;
        img_ext = False;

        try:
            input_fold = self.wdir.toPlainText()
            
            output_folder = input_fold + "\\" +  sdir

            
            #edit
            input_folder = os.path.join(input_fold , "ROMS\\" + core)
            #edit

            if not os.path.isdir(output_folder):
                tdq = QMessageBox.question(self,'Stock Directory', 'Selected Stock Folder doesnt Exist , Do you want to Create it?' , QMessageBox.Yes|QMessageBox.No)
                if tdq == QMessageBox.Yes:
                    os.makedirs(output_folder)
                    QMessageBox.information(self,"Directory" , "Directory Created")
                else:
                    return
            # Check if folders are selected
            if not input_folder or not output_folder or not core: #or not extension:
                QMessageBox.warning(self,'Warning', 'Please fill in all the fields and select multicore rom dir and Stock dir.')
                return

            thumb_size = (144, 208)

            rom_list = [];

            # Iterate over all files in the input folder
            for file_name in os.listdir(input_folder):
                
                print("File name before : " + file_name)
                file_path = os.path.join(input_folder, file_name)
                print("File name after : " + file_name)
                fname_noext = os.path.splitext(os.path.basename(file_path))[0]
                file_ext = os.path.splitext(file_name)[1][1:]
                #file_ext = file_ext.lstrip(".")
                print("extension is " + file_ext)

                # Skip if file name has been processed
                if fname_noext in rom_list:
                    print("skipping as name already in rom list")
                    continue

                # if File is an Image , try to find a matching ROM extension
                if file_ext in ["png" , "bmp" , "jpg" , "jpeg" , "gif"]:
                    rom_ext = self.find_matching_ext(file_name , True)
                    if img_ext:
                        file_name = os.path.join(input_folder, fname_noext + "." +rom_ext)

                else:
                    img_ext = self.find_matching_ext(file_name , False)
                    if img_ext:
                        file_path = os.path.join(input_folder, fname_noext + "." +img_ext)

                if rom_ext or img_ext:
                     with Image.open(file_path) as img:

                        self.zfb_from_image(img , input_folder , core ,  file_name , output_folder )
                        rom_list.append(fname_noext)

                else:

                    tfp = self.pdir_root + "\\" + pdir
                    print("the placeholder dir n file is " + tfp)

                    try:

                        with Image.open(tfp) as img:

                            print("using the placeholder " + pdir)
                        
                            self.zfb_from_image(img , input_folder , core ,  file_name, output_folder )
                            print("png created with placeholder")

                    except:

                        print("Not using placeholder " + pdir)
                        print(f"shortcut is {core};{file_name}.gba")
                        placeholder_data = b'\x00' * 0xEA00 + b'\x00\x00\x00\x00' + f"{core};{file_name}.gba".encode('utf-8') + b'\x00\x00'
                        #zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')
                        zfb_filename = os.path.join(output_folder , file_name + '.zfb')
                        #print(os.path.splitext(file_name)[0])
                        with open(zfb_filename, 'wb') as zfb:
                            zfb.write(placeholder_data)

                    
            QMessageBox.information(self,'Success', 'ZFB files created successfully.')

            if self.chk_refresh.isChecked():
                self.rebuildAll()
                QMessageBox.information(self,'Roms Refresh', 'All Rom lists have been refreshed.')
        except Exception as e:
            QMessageBox.critical(self,'Error', f'An error occurred while creating the ZFB files: {str(e)}')
                

    def rebuildAll(self):
        frogtool_mod.run(self.wdir.toPlainText(), "ALL", "-sc")
        return




if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    app.exec_()