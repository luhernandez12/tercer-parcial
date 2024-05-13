from clases import *
cargar=CargarDicom()
pacientes=Pacientes()
modificarImg = modificarImg()
diccPacs={}
diccDicom={}
while True:
    menu=int(input("Ingrese la opcion:\n1-Ingresar paciente\n2-Ingresar imagenes JPG o PNG\n5-Tranformación geometrica de rotación \n4-Gestión y manipualción de la imagen PNG o JPG\n5-salir"))
    if menu==1:
        
        ruta=input("Ingrese la ruta de la carpeta: ")
        cargar.asignar_archDicom(ruta)
        nombres_dcm, datos=cargar.leer_DICOM()   #Retorna una lista con todos los dcm de la carpeta
        a=cargar.extraccion(datos[0]) #Retorma lista con nombre, edad , id y archivo imgen nifti 
        print(f"Se guardaron los datos asi: \n Nombre:{a[0]}\nEdad:{a[1]}\nID:{a[2]}\nImagen nifti:{a[3]}")
        diccDicom[a[2]]=datos
        diccPacs[a[2]]=[a[0],a[1],a[3]]
 
    elif menu==2:
        dg=input("Ingrese la una imagen JPG y PNG")
        clave=int(input("Ingrese una clave asociada a la imgagen"))
        diccDicom[clave]=dg
    elif menu==3:
        input("Los siguientes archivos dicom estan  almacenados:  ")
        for i,a in enumerate(nombres_dcm):
            print(f"{i}-->{a}")
        ruta_original=input(f" escriba la ruta del que desea rotar.  ")
        ruta_final = input("Ingrese la ruta donde desea guardar la imagen DICOM rotada:  ")
        ds = pydicom.dcmread(ruta_original)
        img = ds.pixel_array
        rotated = modificarImg.rotate(img, 45)
        modificarImg.graficar(img,rotated)
        modificarImg.guardar_img_rotada(rotated, ruta_original, ruta_final)

    elif menu==4:
        print(diccDicom)
        clav=int(input("Ingrese la clave asociada a la imagen"))
        ruta=diccDicom[clav]
        if ruta!=None:          
            a,b=modificarImg.binarizar(ruta)
            modificarImg.graficar_binarizada(a,b)
            c,K1,K2 = modificarImg.transformacion(b)
            d = modificarImg.texto(c,K1,K2)
            modificarImg.graficar_binarizada(b,d)
    else:
        break
