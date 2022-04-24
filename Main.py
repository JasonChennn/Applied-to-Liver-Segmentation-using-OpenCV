import sys
import pydicom
#import scipy.misc
import os
import cv2
import numpy as np
import skimage
#import matplotlib.pyplot as plt
import warnings
import threading
#import mritopng
import re
import time
import shutil
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap,QImage
from MainUI import MainUI_Dialog,Multi_Dialog,Reveal_Dialog
from skimage import morphology
from numba import jit 
import datetime


Initialization = False

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def SaveLogs(txt):
    now = datetime.datetime.now()
    string = "Logs/"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"#"+str(now.hour)+str(now.minute)+".txt"
    fp = open(string, "a")
    fp.write(txt)
    fp.close()

class Dicom():
    def __init__(self):
        self.index = 0
        self.save_index = -1
        self.bottom_index = -1
        self.top_index = -1
        self.BoneValue = 210 #Best:210
        self.LiverValue = 178 #Best:178 FROM MIDDLE IN DATASET
        self.dpath = "Dicoms"
        self.rpath = "Registers"
        self.LoopProcess = False
        self.dfiles = sorted_aphanumeric(os.listdir(self.dpath))
        self.rfiles = sorted_aphanumeric(os.listdir(self.rpath))
        self.len = len(self.rfiles)
        self.Dicom2jpg(self.index)
        self.afreaVol = 0
        self.setArea = 0
        self.setSliceLocations = []
        self.setImagePositon_z = []
        print("Index:"+str(self.index))
        
    # if you need to convert to image file from dicom, use this function. 
    def Dicom2jpg(self,value):
        self.index = value
        self.rpath = "Registers/" + self.rfiles[self.index]
        self.Image = cv2.imread(self.rpath,0)
        self.TargetImage = cv2.imread(self.rpath,0)
        self.ReturnImage = cv2.imread(self.rpath,0)
        if os.path.isfile(self.rpath):
            pass
        else:
            self.fullpath = os.path.join(self.dpath, self.dfiles[self.index])
            path = os.getcwd()
            os.system("cd "+ path)
            #ds = pydicom.read_file(self.fullpath)
            #img = ds.pixel_array
            
            outpath = "Registers"
            cmd = 'dcm2jpg -o ' + os.path.abspath(outpath) + ' ' + os.path.abspath(self.fullpath)
            os.system(cmd)
            #scaled_img = cv2.convertScaleAbs(img-np.min(img), alpha=(255.0 / min(np.max(img)-np.min(img), 10000)))
            #with warnings.catch_warnings():
            #    warnings.simplefilter("ignore")
            #    scipy.misc.imsave(self.rpath,img)
            #cv2.imwrite(self.rpath,scaled_img) # write png image
            self.Image = cv2.imread(self.rpath,0)
            self.TargetImage = cv2.imread(self.rpath,0)

        
    def CreateTempImage(self):
        win.SetPixmap()
        
    def MedianBlurImage(self,img):
        img = cv2.medianBlur(img, 5) 
        #print("MedianBlurImage")
        return img
        
    def BinaryImage(self,img,value):
        ret,img = cv2.threshold(img, value, 255, cv2.THRESH_BINARY)
        #print("BinaryImage")
        return img
        
    def OtsuImage(self,img):
        ret,img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        #print("OtsuImage")
        return img

    def DilateImage(self,img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5)) 
        img = cv2.dilate(img, kernel) 
        #print("DilateImage")
        return img

    def ClearTheBone(self,img):
        original = self.Image
        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                if(img[i,j] != 0): 
                    original[i,j] = 0; 
        
        self.Image = cv2.imread(self.rpath,0)
        img = original
        #print("ClearTheBone")
        return img
                    
    def CloseImage(self,img,value):
        kernel = np.ones((value,value), np.uint8)
        img = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
        #print("CloseImage")
        return img
        
    def MeasureLabel(self,img):
        labels=skimage.measure.label(self.TargetImage,connectivity=2) 
        cv2.imshow("test",self.TargetImage)
        regions = skimage.measure.regionprops(labels)
        self.MaxLabel = []
        for i in range(labels.max()):
            self.MaxLabel.append(regions[i]['area'])
        self.MaxLabel.sort(reverse=True)
        skimage.morphology.remove_small_objects(labels, min_size=self.MaxLabel[0], connectivity=2, in_place=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cv_image = skimage.img_as_ubyte(labels)
            
        img = cv_image
        #print("MeasureLabel")
        return img
        
    def CannyImage(self,img):
        canny = cv2.Canny(img, 3, 3)
        img = cv2.addWeighted(self.Image, 1, canny, 1, 0)
        #print("CannyImage")
        return img
        
    def FindContours(self,tarimg,img,Type=1):
        index = str(self.index)
        index = index.zfill(6)
        if Type == 1:
            contours, hierarchy = cv2.findContours(tarimg,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img,contours,-1,(0,0,255),3)
            backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            cv2.drawContours(backtorgb,contours,-1,(0,0,255),3)
            cv2.imwrite ("Produce_bmp/"+index+".bmp", backtorgb)
        else:
            contours, hierarchy = cv2.findContours(tarimg,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
            c_max = []
            c_maxArea = []
            for i in range(len(contours)):
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                #perimeter = cv2.arcLength(cnt,True)
                c_maxArea.append(area)
                
            for c in range(len(contours)):
                cnt = contours[c]
                area = cv2.contourArea(cnt)
                #perimeter = cv2.arcLength(cnt,True)
                #if(area > max(c_maxArea)/3):
                c_max.append(cnt)
                print(area)
                self.setArea = self.setArea+area
                print("Summary:"+str(self.setArea))
                #perimeter = cv2.arcLength(cnt,True)
                #print(perimeter)
            
            cv2.drawContours(img,c_max,-1,(0,0,255),3)
            backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            cv2.drawContours(backtorgb,contours,-1,(0,0,255),3)
            cv2.imwrite ("Produce_bmp/"+index+".bmp", backtorgb)
                
        #print("FindContours")
        return img
        
    def ConvertToDicom(self,img):
        ds = pydicom.read_file(self.fullpath)
        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                if(img[i,j] == 0):
                    ds.pixel_array[i,j] = 0;
        ds.PixelData = ds.pixel_array.tostring()  
        index = str(self.index)
        index = index.zfill(6)
        ds.save_as("Produce_dcm/"+index+".dcm")
        print("# convert to 'Dicom' completed.")
        
    def ResizeImageArray(self,img,cropType):
        areaVol = 0 
        for row in range(0,img.shape[0]):
            for col in range(0,img.shape[1]):
                if(img[row,col] == 255):
                    areaVol += 1
                    
        if(cropType == 2):
            if((areaVol - self.afreaVol) > 0):
                print("Current state: Liver is getting bigger!")
                if(abs(areaVol - self.afreaVol) > areaVol/30):
                    print("Current state: Liver gap is too large, back to original sample!")
                else:
                    self.CanyImage = self.ExtendImage(img,5)
            else:
                print("Current state: Liver is getting smaller!")
                if(abs(areaVol - self.afreaVol) > areaVol/30):
                    print("Current state: Liver gap is too large, back to original sample!")
                else:
                    self.CanyImage = self.ExtendImage(img,1)
        else:
            self.CanyImage = img
            
        self.afreaVol = areaVol
        print("Surface Area: ",areaVol)
        
    @jit
    def ExtendImage(self,result,value):
        for times in range(value):
            for row in range(0,result.shape[0]):
                for col in range(0,result.shape[1]):
                    if(result[row,col] == 255):
                        if(result[row-1,col] == 0):
                            result[row-1,col] = 255
                        if(result[row+1,col] == 0):
                            result[row+1,col] = 254
                        if(result[row,col-1] == 0):
                            result[row,col-1] = 255
                        if(result[row,col+1] == 0):
                            result[row,col+1] = 254
                    if(result[row,col] == 254):
                            result[row,col] = 255
        #print("ExtendImage")
        return result
    
    def SetRevealPixmap(self,img):
        rev.show()
        height, width = img.shape
        qImg = QImage(dicom.TargetImage.data, width, height, width, QImage.Format_Grayscale8)
        qPixImg = QPixmap(QPixmap.fromImage(qImg))
        rev.ui.label.setPixmap(qPixImg)
        
    def ReadTargetImage(self):
        #img = cv2.imread('Image\TargetImage.jpg',0)
        #cv2.imshow("test",img)
        cv2.waitKey(1)
            
    def ProcessImage(self,Multing=0):
        print("Index:"+str(self.index))
        dicom.TargetImage = dicom.Image
        dicom.TargetImage = dicom.MedianBlurImage(dicom.TargetImage)
        dicom.TargetImage = dicom.BinaryImage(dicom.TargetImage,dicom.BoneValue)
        dicom.TargetImage = dicom.DilateImage(dicom.TargetImage)
        dicom.TargetImage = dicom.ClearTheBone(dicom.TargetImage)
        dicom.TargetImage = dicom.BinaryImage(dicom.TargetImage,dicom.LiverValue)
        dicom.TargetImage = dicom.CloseImage(dicom.TargetImage,3)
        dicom.TargetImage = dicom.MeasureLabel(dicom.TargetImage)
        dicom.TargetImage = dicom.OtsuImage(dicom.TargetImage)
        dicom.TargetImage = dicom.CloseImage(dicom.TargetImage,30)
        dicom.ResizeImageArray(dicom.TargetImage,1)
        tarImg = dicom.TargetImage.copy()
        tarImg2 = self.Image.copy()
        dicom.TargetImage = dicom.FindContours(tarImg,tarImg2)    
        if(Multing == 0):
            self.CreateTempImage()
            th = threading.Thread(self.ReadTargetImage())
            th.start()
        print("process to 'Original Image' completed.")
        print("=====================================")
            
    def ProcessCropImage(self,Multing=False):
        print("Index:"+str(self.index))
        dicom.TargetImage = self.Image
        for i in range(0,dicom.TargetImage.shape[0]):
            for j in range(0,dicom.TargetImage.shape[1]):
                if(dicom.CanyImage[i,j] == 0):
                    dicom.TargetImage[i,j] = 0
        self.Image = cv2.imread(self.rpath,0)
        dicom.TargetImage = dicom.MedianBlurImage(dicom.TargetImage)
        tarImg = dicom.TargetImage.copy()
        tarImg = dicom.BinaryImage(tarImg,dicom.BoneValue)
        for i in range(0,tarImg.shape[0]):
            for j in range(0,tarImg.shape[1]):
                if(tarImg[i,j] != 0):
                    dicom.TargetImage[i,j] = 0;
        dicom.TargetImage = dicom.BinaryImage(dicom.TargetImage,dicom.LiverValue)
        tarImg = dicom.TargetImage.copy()
        tarImg = dicom.CloseImage(tarImg,15)
        dicom.ResizeImageArray(tarImg,2)
        dicom.TargetImage = dicom.CloseImage(dicom.TargetImage,10)
        dicom.ConvertToDicom(dicom.TargetImage)
        tarImg = dicom.TargetImage.copy()
        tarImg2 = self.Image.copy()
        dicom.TargetImage = dicom.FindContours(tarImg,tarImg2,2)    
        if(Multing == False):
            cv2.imwrite('Image\TargetImage.jpg', dicom.TargetImage, [cv2.IMWRITE_JPEG_QUALITY, 90])
            self.CreateTempImage()
            #self.SetRevealPixmap()
            th = threading.Thread(self.ReadTargetImage())
            th.start()
        print("process to 'Inherit Image' completed.")
        print("==================================")

class MainUI(QDialog):
    
    def __init__(self):
        super().__init__()
        self.ui = MainUI_Dialog()
        self.ui.setupUi(self)
        self.ui.spinBox.setRange(0, dicom.len-1)
        self.ui.spinBox_2.setRange(0, 255)
        self.ui.horizontalSlider.setMaximum(dicom.len-1)
        self.ui.verticalSlider.setMaximum(255)
        self.ui.spinBox.valueChanged.connect(self.SpinBoxValueChanged)
        self.ui.spinBox_2.valueChanged.connect(self.SpinBox2ValueChanged)
        self.ui.pushButton.clicked.connect(self.OnPushButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.OnPushButton_2Clicked)
        self.ui.pushButton_7.clicked.connect(self.OnPushButton_7Clicked)
        self.ui.label.setScaledContents (True)
        self.pixmap = QPixmap(dicom.rpath)
        self.ui.label.setPixmap(self.pixmap)
        self.ui.label_5.setPixmap(self.pixmap)
        self.ui.spinBox.setValue(dicom.index)
        self.ui.spinBox_2.setValue(dicom.LiverValue)
        
    def SpinBoxValueChanged(self):
        dicom.Dicom2jpg(self.ui.spinBox.value())
        if dicom.LoopProcess == False:
            self.SetPixmap()
        self.SetOriginalPixmap(dicom.rpath)        
        
    def SetPixmap(self):
        height, width = dicom.TargetImage.shape
        qImg = QImage(dicom.TargetImage.data, width, height, width, QImage.Format_Grayscale8)
        qPixImg = QPixmap(QPixmap.fromImage(qImg))
        self.ui.label.setPixmap(qPixImg)
        return qPixImg
        
    def SetOriginalPixmap(self,path):
        self.pixmap = QPixmap(path)
        self.ui.label_5.setPixmap(self.pixmap)
        
    def SpinBox2ValueChanged(self):
        if Initialization == True:
            dicom.LiverValue = self.ui.spinBox_2.value()
    
    def OnPushButtonClicked(self):
        if Initialization == True:
            dicom.TargetImage = dicom.Image
            dicom.ProcessImage()
            
    def OnPushButton_2Clicked(self):
        mul.ProcessBreak = False
        mul.ui.pushButton.setEnabled(False)
        mul.ui.pushButton_2.setEnabled(False)
        mul.ui.label.setText("Image Processing ...")
        mul.ui.label_2.setText("Image Processing ...")
        mul.ui.label_3.setText("Image Processing ...")
        mul.ui.label_4.setText("Image Processing ...")
        mul.ui.label_5.setText("Image Processing ...")
        mul.ui.label_6.setText("Image Processing ...")
        mul.ui.label_7.setText("Image Processing ...")
        mul.ui.label_8.setText("Image Processing ...")
        mul.show()
        win.hide()
        th = threading.Thread(target=self.StartMultiDialog)
        th.start()
        
    def OnPushButton_7Clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self,"Select Data Folder","src\Dicoms") 

        if dir_choose == "":
            print("\nCancel")
            return

        print("\nSelected Data Folder:")
        print(dir_choose)    
        dfiles = sorted_aphanumeric(os.listdir(dir_choose))
        dpath = "Dicoms"
        outpath = "Registers"
        
        try:
            #shutil.rmtree(dpath)
            #shutil.rmtree(outpath)
            os.system("rd/s/q "+dpath)
            os.system("rd/s/q "+outpath)
            pass
        except OSError as e:
            print(e)
        else:
            print("The directory is deleted successfully")
            
        os.mkdir(dpath)
        os.mkdir(outpath)
        path = os.getcwd()
        for i in range(1,len(dfiles)):
            print(dfiles[i])
            print(dir_choose)
            fixedpath = os.path.abspath(dir_choose)
            inputpath = fixedpath + "/" +str(dfiles[i])
            fullpath = os.path.join(dpath, dfiles[i])
            shutil.copy(inputpath, dpath) 
            os.system("cd "+ path)        
            cmd = 'dcm2jpg -o ' + os.path.abspath(outpath) + ' ' + os.path.abspath(fullpath)
            os.system(cmd)
        print("===========Data imported successfully, please restart the program!===========")
        sys.exit(app.exec_())
                
    def LoopProcessCropImag(self):
        stage = 0
        for i in range(dicom.bottom_index,dicom.top_index+2):
            if Initialization == True:
                if stage == 0:
                    dicom.ProcessCropImage()
                    dicom.index = dicom.index + 1
                    self.ui.spinBox.setValue(dicom.index)
                    if dicom.index == dicom.top_index+1:
                        stage = 1
                elif stage == 1:
                    dicom.index = dicom.save_index-1
                    self.ui.spinBox.setValue(dicom.index)
                    dicom.TargetImage = dicom.Image
                    dicom.ProcessImage()
                    stage = 2
                elif stage == 2:
                    dicom.ProcessCropImage()
                    dicom.index = dicom.index - 1
                    self.ui.spinBox.setValue(dicom.index)    
                    if dicom.index == dicom.bottom_index-1:
                        print("Consecutive liver segmentation completed!")
                        self.tEnd = time.time()
                        print("It cost %f sec" % (self.tEnd - self.tStart))
                        string = "Index:"+str(dicom.bottom_index)+" to "+str(dicom.top_index)+"slice\nTime:"+str(self.tEnd - self.tStart)+"seconds\nSurface:"+ str(dicom.setArea) + ""
                        SaveLogs(string)
                        dicom.LoopProcess = False
                
    def SetLabelPixmap(self,sheet):
        if sheet == 0:
            mul.ui.label.setPixmap(self.pix[0])
        elif sheet == 1:
            mul.ui.label_2.setPixmap(self.pix[1])
        elif sheet == 2:
            mul.ui.label_3.setPixmap(self.pix[2])
        elif sheet == 3:
            mul.ui.label_4.setPixmap(self.pix[3])
        elif sheet == 4:
            mul.ui.label_5.setPixmap(self.pix[4])
        elif sheet == 5:
            mul.ui.label_6.setPixmap(self.pix[5])
        elif sheet == 6:
            mul.ui.label_7.setPixmap(self.pix[6])
        elif sheet == 7:
            mul.ui.label_8.setPixmap(self.pix[7])
            
    def StartMultiDialog(self):
        self.OriginalValue = dicom.LiverValue
        self.value = [dicom.LiverValue+80,dicom.LiverValue+60,dicom.LiverValue+40,dicom.LiverValue+20,dicom.LiverValue,dicom.LiverValue-20,dicom.LiverValue-40,dicom.LiverValue-60]
        for i in range(len(self.value)):
            if self.value[i] > 250:
                self.value[i] = 250
            elif self.value[i] < 1:
                self.value[i] = 1
        self.pix = []
        mul.ui.radioButton.setText(""+str(self.value[0]))
        mul.ui.radioButton_2.setText(""+str(self.value[1]))
        mul.ui.radioButton_3.setText(""+str(self.value[2]))
        mul.ui.radioButton_4.setText(""+str(self.value[3]))
        mul.ui.radioButton_5.setText(""+str(self.value[4]))
        mul.ui.radioButton_6.setText(""+str(self.value[5]))
        mul.ui.radioButton_7.setText(""+str(self.value[6]))
        mul.ui.radioButton_8.setText(""+str(self.value[7]))
        for i in range(8):
            if mul.ProcessBreak == False:
                print("The "+str(i+1)+" image is being processed.")
                dicom.LiverValue = self.value[i]
                dicom.ProcessImage(1)
                self.pix.append(self.SetPixmap())
                self.SetLabelPixmap(i)
            
        mul.ui.pushButton.setEnabled(True)
        mul.ui.pushButton_2.setEnabled(True)
        dicom.LiverValue = self.OriginalValue

           
class MultiUI(QDialog):
    
    def __init__(self):
        super().__init__()
        self.ui = Multi_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.OnPushButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.OnPushButton_2Clicked)
        self.ui.label.setScaledContents(True)
        self.ui.label_2.setScaledContents(True)
        self.ui.label_3.setScaledContents(True)
        self.ui.label_4.setScaledContents(True)
        self.ui.label_5.setScaledContents(True)
        self.ui.label_6.setScaledContents(True)
        self.ui.label_7.setScaledContents(True)
        self.ui.label_8.setScaledContents(True)
        self.ProcessBreak = False
       
    def OnPushButtonClicked(self):
        self.ProcessBreak = True
        if self.ui.radioButton.isChecked():
            dicom.LiverValue = win.value[0]
        elif self.ui.radioButton_2.isChecked():
            dicom.LiverValue = win.value[1]
        elif self.ui.radioButton_3.isChecked():
            dicom.LiverValue = win.value[2]
        elif self.ui.radioButton_4.isChecked():
            dicom.LiverValue = win.value[3]
        elif self.ui.radioButton_5.isChecked():
            dicom.LiverValue = win.value[4]
        elif self.ui.radioButton_6.isChecked():
            dicom.LiverValue = win.value[5]
        elif self.ui.radioButton_7.isChecked():
            dicom.LiverValue = win.value[6]
        elif self.ui.radioButton_8.isChecked():
            dicom.LiverValue = win.value[7]
            
        win.ui.spinBox_2.setValue(dicom.LiverValue)
        dicom.ProcessImage()
        mul.hide()
        win.show()
        
    def OnPushButton_2Clicked(self):
        self.ProcessBreak = True
        dicom.TargetImage = dicom.Image
        dicom.CreateTempImage()
        mul.hide()
        win.show()
        
class RevealUI(QDialog):
    
    def __init__(self):
        super().__init__()
        self.ui = Reveal_Dialog()
        self.ui.setupUi(self)
        

        
if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    dicom = Dicom()
    app = QApplication(sys.argv)
    win = MainUI()
    mul = MultiUI()
    rev = RevealUI()
    win.show()
    #mul.show()
    #dicom.ProcessImage()
    Initialization = True
    sys.exit(app.exec_())
