import os
import pydicom
import nibabel as nib
import cv2
import matplotlib.pyplot as plt
import numpy as np

class CargarDicom:  # Clase para cargar carpetas con archivos DICOM
    def __init__(self):
        self.__archDicom = None  # Inicializa __archDicom como None

    def ver_archDicom(self):
        return self.__archDicom

    def asignar_archDicom(self, arch):
        self.__archDicom = arch

    def leer_DICOM(self):     
        if self.__archDicom is None:
            raise ValueError("La ruta del directorio DICOM no ha sido asignada.")
        
        slices = [os.path.join(self.__archDicom, filename) for filename in os.listdir(self.__archDicom) if filename.endswith('.dcm')]
        slices.sort(key=lambda x: int(pydicom.dcmread(x).InstanceNumber))
        lista = []
        for i in slices:
            dicom_image = pydicom.dcmread(i)
            lista.append(dicom_image) 
        return slices, lista

    def extraccion(self, datos_paciente): 
        pacientes = []          
        nombre = datos_paciente.PatientName
        pacientes.append(nombre)
        edad = datos_paciente.PatientAge
        pacientes.append(edad)
        ID = datos_paciente.PatientID
        pacientes.append(ID)
        pixel_array = datos_paciente.pixel_array
        nifti_img = nib.Nifti1Image(pixel_array, affine=None)
        pacientes.append(nifti_img)
        return pacientes

class Pacientes(CargarDicom): 
    def __init__(self):
        super().__init__()
        self.__nombre = ""
        self.__edad = ""
        self.__ID = ""
        self.__nifthi = None  # Inicializa __nifthi como None

    def verNombre(self):
        return self.__nombre

    def verEdad(self):
        return self.__edad

    def verID(self):
        return self.__ID

    def verNifthi(self):
        return self.__nifthi

    def asignarNombre(self, nombre):
        self.__nombre = nombre

    def asignarEdad(self, edad):
        self.__edad = edad

    def asignarID(self, ID):
        self.__ID = ID

    def asignarNifthi(self, img):
        self.__nifthi = img



class modificarImg:

    def rotate(self,img, angle=0, rotPoint=None):
        while True:
            try:
                angle_input = input('''Seleccione el ángulo que desea rotar la imagen:\n
                            1. Rotar 90°\n
                            2. Rotar 180°\n
                            3. Rotar 270°\n''')
                angle = int(angle_input)
                if angle == 1:
                    angle = 90
                    break
                elif angle == 2:
                    angle = 180
                    break
                elif angle == 3:
                    angle = 270
                    break
                else:
                    print("La opción que eligió no es válida")
            except ValueError:
                print("Ingrese un número válido.")
        
        (height,width) = img.shape[:2]

        if rotPoint is None:
            rotPoint = (width//2,height//2)
        
        rotMat = cv2.getRotationMatrix2D(rotPoint, angle, 1.0)
        dimensions = (width,height)

        return cv2.warpAffine(img, rotMat, dimensions)
    
    def graficar(self,img,rotated):
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.title("Dicom")

        plt.subplot(1, 2, 2)
        plt.imshow(rotated)
        plt.title("Dicom Rotado")

        plt.show()
    
    def guardar_img_rotada(self,imagen_rotada,ruta_original,ruta_final):
        ds = pydicom.dcmread(ruta_original)
        ds.Rows, ds.Columns = imagen_rotada.shape
        ds.PixelData = imagen_rotada.tobytes()
        ds.save_as(ruta_final)


    def binarizar(self,ruta):
        #Leer la imagen
        img0=cv2.imread(ruta)
        
        #Imagen binarisada 
        imgb=cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
        #plt.imshow(imgb, cmap='gray', vmin=0, vmax=255)
        #Transformacion morfologica 
        umb,imgB=cv2.threshold(imgb,20,250,cv2.THRESH_BINARY)
        return imgb,imgB

    def graficar_binarizada(self,img1,img2):
        plt.figure(figsize=(15,6))
        plt.subplot(1,2,1)
        plt.imshow(img1, cmap='gray', vmin=0, vmax=255)
        plt.subplot(1,2,2)
        plt.imshow(img2, cmap='gray', vmin=0, vmax=255)

        plt.show()

    def transformacion(self,binarizada):
        #Kernel
        K1=int(input(f"Ingrese el primer valor del Kernel:  "))
        K2=int(input(f"Ingrese el segundo valor del Kernel:  "))
        kernel = np.ones((K1,K2),np.uint8)
        imaOp2=cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel, iterations = 3)

        return imaOp2,K1,K2
    
    def texto(self,img,K1,K2):
        print(img.shape)
        text = f"Imagen transformada\nUmbral usado: 20\nKernel usado:{K1},{K2}"
        imgTexto = cv2.putText(img, text, (13,33), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255,255,0), 2)
        return imgTexto

        #putText(imagen,texto,(de dónde), fuente, escala, color, grueso)
        

