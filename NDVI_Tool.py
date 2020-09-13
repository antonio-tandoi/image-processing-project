import ee, ee.mapclient
import tkinter as tk
import pyscreenshot as ImageGrab
import gi
from reportlab.graphics.widgets.grids import centroid
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
import datetime, time, sys
from datetime import date
from tkinter import messagebox
from PIL import Image
from PIL.ImageTk import PhotoImage
from ipygee import *
from geetools import ui, tools
from datetime import date
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import geopandas as gpd
from shapely.geometry import shape
import webbrowser
import urllib.request

#-----INIZIALIZZAZIONE OGGETTO EARTH ENGINE
ee.Initialize()
area = ee.Geometry.Polygon([[15.374081, 41.686399], [16.146577, 41.686399],
                            [15.374081, 41.371181], [16.146577, 41.371181]])

#-----SEZIONE 1 - IMPOSTAZIONE INIZIALE FINESTRA
window = tk.Tk()
window.geometry("1250x700")
window.title("NDVI Application Tool")
window.resizable(False, False)
window.configure(background = "white")
satellite = datetime.date(2015, 6, 23)
ndviPalette = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'black']}
count = 1
pngbutton = tk.Button(text = "PNG", width = 4, font = ("Product Sans", 8), fg = "white", 
            bg = "#3498db", borderwidth= 0, highlightcolor="#3498db", highlightbackground="#3498db",
            activebackground = "white", activeforeground = "#3498db", highlightthickness = 1,
            state = DISABLED)
                
svgbutton = tk.Button(text = "SVG", width = 4, font = ("Product Sans", 8), fg = "white", 
            bg = "#3498db", borderwidth= 0, highlightcolor="#3498db", highlightbackground="#3498db",
            activebackground = "white", activeforeground = "#3498db", highlightthickness = 1,
            state = DISABLED)
 
#-----SEZIONE 2 - DEFINIZIONE FUNZIONI
###CALCOLO NDVI           
def NDVI_calc(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']))

###CALCOLO PUNTO, GRAFICO, LINK
def applica(): 
    if (checkCoord() == False):return    
    if (checkDate() == False): return
    
    labelgraf = tk.Label(window, text = "", 
           font = ("Product Sans", 12), background = "white", width = 30 )
    labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "WE")
    
    #Immagine di loading
    load = PhotoImage(file = "/home/antonio/Documenti/Images/loading.png")
    canva2.create_image(0, 0, image = load, anchor = "nw")
    canva2.update_idletasks()
    
    #Costruzione punto di test
    annoI = int(stringa_anno1.get())
    annoF = int(stringa_anno2.get())
    meseI = int(monthNumber(stringa_mese1.get()))
    meseF = int(monthNumber(stringa_mese2.get()))
    giornoI = int(stringa_giorno1.get())
    giornoF = int(stringa_giorno1.get())
    dataI = str(date(annoI, meseI, giornoI))
    dataF = str(date(annoF, meseF, giornoF))
    eeDataI = ee.Date(dataI)
    eeDataF = ee.Date(dataF)
    coordinataX = float(inputX.get())
    coordinataY = float(inputY.get())
    area_ndvi = ee.Geometry.Point(coordinataX, coordinataY).buffer(500)
    
    #Interrogazione satellite
    collection_finale = (ee.ImageCollection('COPERNICUS/S2')
              .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60)) 
              .filterDate(eeDataI, eeDataF)
              .filterBounds(area))
    
    imNDVI1 = collection_finale.map(NDVI_calc)
    imNDVI2 = imNDVI1.select(['nd'])
    imNDVI3 = imNDVI2.median();
    imNDVI4 = imNDVI3.gt(0.35)
    
    #Creazione grafico      
    chartest = chart.Image.series(**
    {
            'imageCollection': imNDVI1,
            'region': area_ndvi,
            'scale': 10,
            'bands': ['nd'],
            'label_bands':['NDVI Band']
    })
    
    #Creazione URL per download
    urlpng_video = imNDVI3.getThumbURL(
    {
        'region': tools.geometry.getRegion(area_ndvi),
        'format': 'png',
        'palette': ['blue', 'white', 'green']
    })
    
    urlpng_threshold = imNDVI4.getThumbURL(
    {
        'region': tools.geometry.getRegion(area_ndvi),
        'format': 'png',
    })
    
    urlsvg = imNDVI3.getDownloadURL({ 'region': tools.geometry.getRegion(area_ndvi)})
    filename = "/home/antonio/Documenti/Images/fields.png"
    urllib.request.urlretrieve(urlpng_video, filename)
    
    chartest.render_to_png('/home/antonio/Documenti/Images/chart.png')
    time.sleep(3)    
    grafico = Image.open("/home/antonio/Documenti/Images/chart.png")
    grafico = grafico.resize((520, 390), Image.ANTIALIAS)
    grafico.save("/home/antonio/Documenti/Images/chart_re.png")
    graf = Image.open("/home/antonio/Documenti/Images/chart_re.png")
    canva2.image = ImageTk.PhotoImage(graf)
    canva2.create_image(0, 0, image = canva2.image, anchor = "nw")        
    
    labelgraf = tk.Label(window, text = "Andamento NDVI nell'intervallo selezionato", 
           font = ("Product Sans", 12), background = "white", width = 30 )
    labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "WE")
        
    field = Image.open("/home/antonio/Documenti/Images/fields.png")
    field = field.resize((640, 390), Image.ANTIALIAS)
    field.save("/home/antonio/Documenti/Images/field_re.png")
    field1 = Image.open("/home/antonio/Documenti/Images/field_re.png")
    canva1.image = ImageTk.PhotoImage(field1)
    canva1.create_image(0, 0, image = canva1.image, anchor = "nw")
    
    pngbutton["command"] = lambda: webbrowser.open(urlpng_threshold, new = 2, autoraise = True)
    pngbutton["state"] = NORMAL
    svgbutton["command"] = lambda: webbrowser.open(urlsvg, new = 2, autoraise = True)
    svgbutton["state"] = NORMAL
    
    rileva = tk.Button(text = "Rileva campi", font = ("Product Sans", 10), fg = "white", 
             bg = "#3498db", borderwidth= 0, highlightcolor="#3498db", highlightbackground="#3498db",
             activebackground = "white", activeforeground = "#3498db", highlightthickness = 1,
             command = rilevamento)
    rileva.place(x = 31, y = 552)
    
#Rilevamento campi irrigati e percentuale  
def rilevamento():
    #Costruzione punto di test
    annoI = int(stringa_anno1.get())
    annoF = int(stringa_anno2.get())
    meseI = int(monthNumber(stringa_mese1.get()))
    meseF = int(monthNumber(stringa_mese2.get()))
    giornoI = int(stringa_giorno1.get())
    giornoF = int(stringa_giorno1.get())
    dataI = str(date(annoI, meseI, giornoI))
    dataF = str(date(annoF, meseF, giornoF))
    eeDataI = ee.Date(dataI)
    eeDataF = ee.Date(dataF)
    coordinataX = float(inputX.get())
    coordinataY = float(inputY.get())
    area_rilevamento = ee.Geometry.Point(coordinataX, coordinataY).buffer(1500)
        
    #Interrogazione satellite
    collection_finale = (ee.ImageCollection('COPERNICUS/S2')
              .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60)) 
              .filterDate(eeDataI, eeDataF)
              .filterBounds(area_rilevamento))
    
    imNDVI1 = collection_finale.map(NDVI_calc)
    imNDVI2 = imNDVI1.select(['nd'])
    imNDVI3 = imNDVI2.median();
    imNDVI4 = imNDVI3.gt(0.35)
    
       
#       change_ico = PhotoImage(file="/home/antonio/Documenti/Images/pie.png")
#       cambia = tk.Button(command = cambio_grafico1, background = "white", highlightcolor = "white", 
#            highlightthickness = 0, borderwidth= 0, image = change_ico)
#       cambia_window = canva2.create_window(0, 390, anchor = "sw", window = cambia)
#       cambia.place(x = 715, y = 555)
        
    centroidi = imNDVI4.reduceToVectors(
        geometry = area_rilevamento,
        geometryType = 'centroid',
        scale = 30,
        crs = 'EPSG:4326',
        eightConnected = True
    )
    time.sleep(5)
    messagebox.showinfo("Rilevamento", "Campi rilevati")
    
    esporta = tk.Button(text = "Esporta in CSV", font = ("Product Sans", 10), fg = "white", 
             bg = "#3498db", borderwidth= 0, highlightcolor="#3498db", highlightbackground="#3498db",
             activebackground = "white", activeforeground = "#3498db", highlightthickness = 1,
             command = salvataggio)
    esporta.place(x = 140, y = 552)
 
#Salvataggio dei campi    
def salvataggio():
    #Costruzione punto di test
    annoI = int(stringa_anno1.get())
    annoF = int(stringa_anno2.get())
    meseI = int(monthNumber(stringa_mese1.get()))
    meseF = int(monthNumber(stringa_mese2.get()))
    giornoI = int(stringa_giorno1.get())
    giornoF = int(stringa_giorno1.get())
    dataI = str(date(annoI, meseI, giornoI))
    dataF = str(date(annoF, meseF, giornoF))
    eeDataI = ee.Date(dataI)
    eeDataF = ee.Date(dataF)
    coordinataX = float(inputX.get())
    coordinataY = float(inputY.get())
    area_rilevamento = ee.Geometry.Point(coordinataX, coordinataY).buffer(1500)
        
    #Interrogazione satellite
    collection_finale = (ee.ImageCollection('COPERNICUS/S2')
              .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60)) 
              .filterDate(eeDataI, eeDataF)
              .filterBounds(area_rilevamento))
    
    imNDVI1 = collection_finale.map(NDVI_calc)
    imNDVI2 = imNDVI1.select(['nd'])
    imNDVI3 = imNDVI2.median();
    imNDVI4 = imNDVI3.gt(0.35)
         
    centroidi = imNDVI4.reduceToVectors(
        geometry = area_rilevamento,
        geometryType = 'centroid',
        scale = 30,
        crs = 'EPSG:4326',
        eightConnected = True
    )
    
    features = centroidi.getInfo()['features']
    dictarr = []
    
    centroids_list = centroidi.toList(centroidi.size()).map(lambda f: ee.Feature(f).geometry().centroid()).getInfo()

    #File TXT
    data = [p['coordinates'] for p in centroids_list]
    filename = '/home/antonio/Documenti/Images/test.txt'
    with open(filename, 'w+') as thefile:
        text = ""
        text += "ID_Centroidi     Coordinate\n"
        for i, p in enumerate(data):
            text += '{}                {}\n'.format(i+1, p)
        thefile.write(text)
    
    #File CSV
    for f in features:
        attr = f['properties']
        attr['geometrytype'] = f['geometry']['coordinates']
        dictarr.append(attr)
           
    df = gpd.GeoDataFrame(dictarr)
    export_csv = df.to_csv('/home/antonio/Documenti/Images/dataframe.csv', index = None, header=True) 
    messagebox.showinfo("Rilevamento", "Le aree sono state salvate")
    
       
###DA GRAFICO A ISTOGRAMMA
def cambio_grafico1(): 
    #Costruzione area istogramma
    canvagraf = Canvas(window, width = 520, height = 390, bg = "white")
    canvagraf.config(bd = 0, background = "white", highlightbackground = "white")
    canvagraf.create_rectangle(5, 10, 20, 25, fill = "#18ca23", outline = "")
    canvagraf.create_rectangle(5, 30, 20, 45, fill = "#e5d215", outline = "")
    canvagraf.create_text(25, 10, text = "Percentuale irrigata", fill = "black", 
                          font = ("Product Sans", 10), anchor = "nw", justify = "left")
    canvagraf.create_text(25, 30, text = "Percentuale non irrigata", fill = "black",
                          font = ("Product Sans", 10), anchor = "nw", justify = "left")
    
    #Costruzione istogramma irrigato
    arcopos = canvagraf.create_arc(130, 65, 380, 315, extent = 240, fill = "#18ca23", 
             activefill = "#049e12", outline = "", activewidth = 3.5, activeoutline = "#18ca23")
    
    #Costruzione istogramma non irrigato
    arconeg = canvagraf.create_arc(160, 95, 360, 295, extent = 120, start = 240, fill = "#e5d215",
             activefill = "#d5bd14", outline = "", activewidth = 3.5, activeoutline = "#e5d215")
    
    #Pulsante per cambio grafico
    canvagraf.grid(row = 3, column = 3, columnspan = 2, pady = 20)
    cambia = tk.Button(text = "Grafico", command = cambio_grafico2, font = ("Product Sans", 10),
                    activebackground = "#1cb904", activeforeground = "white", fg = "white",
                    highlightthickness = 0, background = "#3498db", borderwidth= 0, width = 10)
    cambia.place(x = 715, y = 555)
   
    labelgraf = tk.Label(window, text = "Distribuzione area irrigata", font = ("Product Sans", 12), 
                   background = "white", width = 35 )
    labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "WE")
    
###DA ISTOGRAMMA A GRAFICO     
def cambio_grafico2(): 
    #Creazione area grafico
    canva2 = Canvas(window, width = 520, height = 390)
    canva2.config(bd = 0, background = "white", highlightbackground = "white")
    grafico = Image.open("/home/antonio/Documenti/Images/chart.png")
    grafico = grafico.resize((520, 390), Image.ANTIALIAS)
    grafico.save("/home/antonio/Documenti/Images/chart_re.png")
    graf = Image.open("/home/antonio/Documenti/Images/chart_re.png")
    canva2.image = ImageTk.PhotoImage(graf)
    canva2.create_image(0, 0, image = canva2.image, anchor = "nw")
    canva2.grid(row = 3, column = 3, columnspan = 2, pady = 20)
    
    #Pulsante cambio grafico
    cambia = tk.Button(text = "Istogramma", command = cambio_grafico1, font = ("Product Sans", 10),
                    activebackground = "#1cb904", activeforeground = "white", fg = "white",
                    highlightthickness = 0, background = "#3498db", borderwidth= 0, width = 10)
    cambia.place(x = 715, y = 555)
    
    labelgraf = tk.Label(window, text = "Andamento NDVI nell'intervallo selezionato", 
                font = ("Product Sans", 12), background = "white" )
    labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "WE")
         
def zoomerP(event):
        canva1.scale("all", event.x, event.y, 1.5, 1.5)
        canva1.configure(scrollregion = canva1.bbox("all"))
def zoomerM(event):
        canva1.scale("all", event.x, event.y, 0.5, 0.5)
        canva1.configure(scrollregion = canva1.bbox("all"))

###CANCELLAZIONE INPUT
def cancella():
    MsgBox = tk.messagebox.askquestion('Cancellazione','Azzerare i campi?')
    if MsgBox == 'yes':
        inputX.delete(0, tk.END)
        inputY.delete(0, tk.END)
              
###APERTURA BROWSER       
def download(): 
    global count, pngbutton, svgbutton
    count = count + 1
    if (count %2 == 0):
        pngbutton.place(x = 617, y = 590)
        svgbutton.place(x = 617, y = 620)
        return
    if (count %2 == 1):
        pngbutton.place_forget()
        svgbutton.place_forget()
        return
      
###CANCELLAZIONE INPUT AL FOCUS       
def cancellaX(event): inputX.delete(0, tk.END)
def cancellaY(event): inputY.delete(0, tk.END)    

###CONVERSIONE MESE IN NUMERO
def monthNumber(mese):
    switcher = {
        'Gennaio': '01', 'Febbraio': '02', 'Marzo': '03', 'Aprile': '04',  
        'Maggio': '05', 'Giugno': '06', 'Luglio': '07',  'Agosto': '08', 
        'Settembre': '09', 'Ottobre': '10', 'Novembre': '11', 'Dicembre': '12'
        } 
    return switcher[mese]

###CONTROLLO COORDINATE INSERITE
def checkCoord():
    if inputX.get():
        coordinataX = inputX.get()
        
        #Coordinata X assente
        if (coordinataX == "Coordinata X"):
            messagebox.showerror("Errore coordinata", "Inserire coordinata X")
            return False
        
        #Controllo che sia coordinata
        if (coordinataX.find(".") !=2):
            messagebox.showerror("Errore coordinata", "Inserire una coordinata X corretta!")
            return False
    else:
        messagebox.showerror("Errore coordinata", "Coordinata X vuota!")
        return False
    if inputY.get():
        coordinataY = inputY.get()
        
        #Coordinata Y assente
        if (coordinataY == "Coordinata Y"):
            messagebox.showerror("Errore coordinata", "Inserire coordinata Y")
            return False
        
        #Controllo che sia coordinata
        if (coordinataY.find(".") != 2):
            messagebox.showerror("Errore coordinata", "Inserire una coordinata Y corretta!")
            return False
    else:
        messagebox.showerror("Errore coordinata", "Coordinata Y vuota!")
        return False

###CONTROLLO DATE INSERITE
def checkDate():
    oggi = date.today()
    
    #Controllo se i valori sono inseriti
    if (stringa_anno1.get() == "Anno" or stringa_mese1.get() == "Mese" or stringa_giorno1.get()== "Giorno"):
        messagebox.showerror("Errore data", "Inserire data iniziale valida!")
        return False
    if (stringa_anno2.get() == "Anno" or stringa_mese2.get() == "Mese" or stringa_giorno2.get() == "Giorno"):
        messagebox.showerror("Errore data", "Inserire data finale valida!")
        return False
    annoI = int(stringa_anno1.get())
    annoF = int(stringa_anno2.get())
    meseI = int(monthNumber(stringa_mese1.get()))
    meseF = int(monthNumber(stringa_mese2.get()))
    giornoI = int(stringa_giorno1.get())
    giornoF = int(stringa_giorno1.get())
    
    #Controllo sui 30 giorni
    if (((giornoI == 31)) and ((meseI == 11) or (meseI == 4) or (meseI == 6) or (meseI == 9))
        or ((giornoF == 31)) and ((meseF == 11) or (meseF == 4) or (meseF == 6) or (meseF == 9))):
        messagebox.showerror("Errore data", "Data non valida")
        return False
       
    #Controllo su febbraio bisestile
    if meseI == 2:
        if giornoI == 29:
            if not (annoI%4 == 0 and annoI%100 == 0 and annoI%400 == 40):
                messagebox.showerror("Errore data", "Anno non bisestile")
                return False
    
    if meseF == 2:
        if giornoF == 29:
            if not (annoF%4 == 0 and annoF%100 == 0 and annoF%400 == 40):
                messagebox.showerror("Errore data", "Anno non bisestile")
                return False

    dataI = date(annoI, meseI, giornoI)
    dataF = date(annoF, meseF, giornoF)
    
    #Controllo data lancio satellite
    if (dataI < satellite):
        messagebox.showerror("Errore data", "Data iniziale precendente al lancio del satellite (23/06/2015)!")
        return False
    
    #Controllo coerenza data finale e iniziale
    if (dataF < dataI):
        messagebox.showerror("Errore data", "Data finale precendente alla data iniziale!")
        return False
    
    #Controllo che data odierna non sia superata
    if (oggi < dataI or oggi < dataF):
        messagebox.showerror("Errore data", "Data odierna superata!")
        return False

#----SEZIONE 4 - DEFINIZIONE INTERFACCIA
###RIGA 1    
punto_label = tk.Label(window, text="Coordinate del punto : ", font = ("Product Sans", 14), 
              background = "white")
punto_label.grid(row = 0, column = 0, padx = 30, pady = 30, sticky = "E")
pos_ico = PhotoImage(file="/home/antonio/Documenti/Images/position.png")
position = tk.Label(window, image = pos_ico, background = "white", borderwidth = 0)
position.grid(row = 0, column = 0, padx = 120, pady = 10, sticky = "W")

inputX = tk.Entry(font = ("Product Sans", 14), justify = "right", fg = "grey")
inputX.insert(0, "Coordinata X")
inputX.grid(row = 0, column = 1, pady = 30, sticky = "WE")
inputX.bind("<Button-1>", cancellaX)

virgola = tk.Label(window, text=", ", font = ("Product Sans", 14), background = "white")
virgola.grid(row = 0, column = 2, padx = 0, pady = 30, sticky = "W")

inputY = tk.Entry(font = ("Product Sans", 14), justify = "right", fg = "grey")
inputY.insert(0, "Coordinata Y")
inputY.grid(row = 0, column = 3, pady = 30, sticky = "WE")
inputY.bind("<Button-1>", cancellaY)

ok_ico = PhotoImage(file="/home/antonio/Documenti/Images/ok.png")
applica = tk.Button(text = "Applica!", command = applica, font = ("Product Sans", 14),
          activebackground = "white", activeforeground = "#3498db", fg = "white",
          highlightthickness = 2, background = "#3498db", borderwidth= 0, image = ok_ico, 
          compound = LEFT, highlightcolor="#3498db", highlightbackground="#3498db")
applica.grid(row=0, column=4, padx = 40, pady = 30, sticky = "W")

del_ico = PhotoImage(file="/home/antonio/Documenti/Images/delete.png")
delete = tk.Button(command = cancella, activebackground = "firebrick",
          highlightthickness = 2, background = "white", borderwidth= 0, image = del_ico, 
          highlightbackground = "firebrick")
delete.place(x = 1170, y = 30)


ndvimess = tk.Label(window, text = "La zona potrebbe essere irrigata", 
           font = ("Product Sans", 14), background = "white", fg = "green" )


###RIGA 2
cal_ico = PhotoImage(file="/home/antonio/Documenti/Images/calendar.png")
calendar = tk.Label(window, image = cal_ico, background = "white", borderwidth = 0)
calendar.grid(row = 1, column = 0, rowspan = 2, padx = 120, pady = 10, sticky = "W")

inizio = tk.Label(window, text = "Inizio osservazione : ", 
         font = ("Product Sans", 14), background = "white")
inizio.grid(row = 1, column = 0, padx = 30, pady = 5, sticky = "E")

fine = tk.Label(window, text = "Fine osservazione : ", font = ("Product Sans", 14), background = "white")
fine.grid(row = 2, column = 0, padx = 30, pady = 5, sticky = "E")

#####ANNO INIZIO
stringa_anno1 = tk.StringVar(window)
stringa_anno1.set("Anno")

menuAnniI = tk.OptionMenu(window, stringa_anno1, "2019", "2018", "2017", "2016", "2015")
menuAnniI.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 5, 
          highlightthickness=0, borderwidth = 0, activebackground = "#3498db", 
          activeforeground = "white")
menuAnniI["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
          relief=tk.GROOVE, font = ("Product Sans", 9))
menuAnniI.grid(row = 1, column = 1, sticky = "E")

######ANNO FINE
stringa_anno2 = tk.StringVar(window)
stringa_anno2.set("Anno")

menuAnniF = tk.OptionMenu(window, stringa_anno2, "2019", "2018", "2017", "2016", "2015")
menuAnniF.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 5, 
           highlightthickness=0, borderwidth = 0, activebackground = "#3498db", 
           activeforeground = "white")
menuAnniF["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
           relief=tk.GROOVE, font = ("Product Sans", 9))
menuAnniF.grid(row = 2, column = 1, sticky = "E")

######MESE INIZIO
stringa_mese1 = tk.StringVar(window)
stringa_mese1.set("Mese")

menuMesiI = tk.OptionMenu(window, stringa_mese1, "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", 
            "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre")
menuMesiI.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 7, 
            highlightthickness=0, borderwidth = 0, activebackground = "#3498db", 
            activeforeground = "white")
menuMesiI["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
            relief=tk.GROOVE, font = ("Product Sans", 9))
menuMesiI.grid(row = 1, column = 1, columnspan = 2)

######MESE FINE
stringa_mese2 = tk.StringVar(window)
stringa_mese2.set("Mese")

menuMesiF = tk.OptionMenu(window, stringa_mese2, "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", 
            "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre")
menuMesiF.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 7, 
             highlightthickness=0, borderwidth = 0, activebackground = "#3498db", 
             activeforeground = "white")
menuMesiF["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
             relief=tk.GROOVE, font = ("Product Sans", 9))
menuMesiF.grid(row = 2, column = 1, columnspan=2)

######GIORNO INIZIO
stringa_giorno1 = tk.StringVar(window)
stringa_giorno1.set("Giorno")

menuGiorniI = tk.OptionMenu(window, stringa_giorno1, "1", "2", "3", "4", "5", "6", "7", "8", "9", 
              "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
              "24", "25", "26", "27", "28", "29", "30", "31")
menuGiorniI.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 5, 
               highlightthickness=0, borderwidth= 0, activebackground = "#3498db", 
               activeforeground = "white")
menuGiorniI["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                relief=tk.GROOVE, font = ("Product Sans", 9))
menuGiorniI.grid(row = 1, column = 1, columnspan = 2, sticky = "W")

######GIORNO FINE
stringa_giorno2 = tk.StringVar(window)
stringa_giorno2.set("Giorno")

menuGiorniF = tk.OptionMenu(window, stringa_giorno2, "1", "2", "3", "4", "5", "6", "7", "8", "9", 
              "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
              "24", "25", "26", "27", "28", "29", "30", "31")
menuGiorniF.config(bg = "gray97", relief=tk.GROOVE, font = ("Product Sans", 12), width = 5,
               highlightthickness=0, borderwidth = 0, activebackground = "#3498db", 
               activeforeground = "white")
menuGiorniF["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
               relief=tk.GROOVE, font = ("Product Sans", 9))
menuGiorniF.grid(row = 2, column = 1, columnspan = 2, sticky = "W")


###RIGA 3
canva1 = Canvas(window, width = 640, height = 390)
canva1.config(bd = 0, background = "white", highlightbackground = "white")

map_ = Image.open("/home/antonio/Documenti/Images/mappa_re.png")
canva1.image = ImageTk.PhotoImage(map_)
canva1.create_image(0, 0, image = canva1.image, anchor = "nw")
canva1.grid(row = 3, column = 0, columnspan = 2, padx = 30)

canva1.bind("<Button-4>", zoomerP)
canva1.bind("<Button-5>", zoomerM)

down_ico = PhotoImage(file="/home/antonio/Documenti/Images/download.png")
download = tk.Button(command = download, highlightcolor = "grey", highlightthickness = 1, 
           background = "white", borderwidth= 0, image = down_ico)
download_window = canva1.create_window(640, 390, anchor = "se", window = download)


canva2 = Canvas(window, width = 520, height = 390)
canva2.config(bd = 0, background = "white", highlightbackground = "white")
canva2.grid(row = 3, column = 3, columnspan = 2, pady = 20) 

###RIGA 4 
blu = PhotoImage(file = "/home/antonio/Documenti/Images/blue.png")
blu_label = tk.Label(window, image = blu)
blu_label.grid(row = 4, column = 0, padx = 45, sticky = "W")

legend1 = tk.Label(window, text = "Campi sicuramente irrigati", font = ("Product Sans", 10), 
          background = "white")
legend1.grid(row = 4, column = 0, sticky = "W", padx = 65)
labelgraf = tk.Label(window, text = "", 
           font = ("Product Sans", 12), background = "white", width = 30 )

###RIGA 5
rosso = PhotoImage(file="/home/antonio/Documenti/Images/red.png")
rosso_label = tk.Label(window, image = rosso)
rosso_label.grid(row = 5, column = 0, padx = 45, sticky = "W")

legend2 = tk.Label(window, text = "Campi sicuramente non irrigati", font = ("Product Sans", 10), 
          background = "white")
legend2.grid(row = 5, column = 0, sticky = "W", padx = 65)

###RIGA 6
firma = tk.Label(window, text = "Antonio Tandoi - 2018/2019", font = ("Product Sans", 7), 
        background = "white" )
firma.grid(row = 6, column = 4, sticky = "E", pady = 30, padx = 10)

window.mainloop()