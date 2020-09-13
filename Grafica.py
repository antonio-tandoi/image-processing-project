import tkinter as tk
import datetime
from datetime import date
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from email.policy import default


#SEZIONE 1 - IMPOSTAZIONE INIZIALE FINESTRA
window = tk.Tk()
window.geometry("1250x740")
window.title("NDVI Application Tool")
window.resizable(False, False)
window.configure(background="white")
satellite = datetime.date(2015, 6, 23)

#SEZIONE 2 - DEFINIZIONE FUNZIONI
   
def controllo_testo():
    if (checkCoord() == False):return    
    if (checkDate() == False): return
    
def cambio_grafico1():
    canvagraf = Canvas(window, width = 520, height = 390, bg = "white")
    canvagraf.config(bd = 0, highlightbackground = "white")
    canvagraf.create_rectangle(5, 10, 20, 25, fill = "#18ca23", outline = "")
    canvagraf.create_rectangle(5, 30, 20, 45, fill = "#e5d215", outline = "")
    canvagraf.create_text(25, 10, text = "Percentuale irrigata", fill = "black", 
                          font = ("Product Sans", 10), anchor = "nw", justify = "left")
    canvagraf.create_text(25, 30, text = "Percentuale non irrigata", fill = "black",
                          font = ("Product Sans", 10), anchor = "nw", justify = "left")
    arcopos = canvagraf.create_arc(130, 65, 380, 315, extent = 240, fill = "#18ca23", activefill = "#0fe71c", 
                                outline = "", activewidth = 3.5, activeoutline = "#049e12")
    arconeg = canvagraf.create_arc(160, 95, 360, 295, extent = 120, start = 240, fill = "#e5d215",
                                activefill = "#e0cc08", outline = "", activewidth = 3.5, activeoutline = "#d5bd14")
    
    canvagraf.grid(row = 3, column = 3, columnspan = 2, pady = 20)
    cambia = tk.Button(text = "Grafico", command = cambio_grafico2, font = ("Product Sans", 10),
                    activebackground = "#1cb904", activeforeground = "white", fg = "white",
                    highlightthickness = 0, background = "#3498db", borderwidth= 0, width = 10)
    cambia.grid(row = 4, column = 3, sticky = "W")
    labelgraf = tk.Label(window, text = "Distribuzione area irrigata", font = ("Product Sans", 12), 
                   background = "white", width = 35 )
    labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "E", padx = 20)
    
       
def cambio_grafico2():
    canva2 = Canvas(window, width = 520, height = 390)
    canva2.config(bd = 0, highlightbackground = "white")
    grafico = Image.open("/home/antonio/Documenti/chart.png")
    grafico = grafico.resize((520, 390), Image.ANTIALIAS)
    grafico.save("/home/antonio/Documenti/chart_re.png")
    graf = Image.open("/home/antonio/Documenti/chart_re.png")
    canva2.image = ImageTk.PhotoImage(graf)
    canva2.create_image(0, 0, image = canva2.image, anchor = "nw")
    canva2.grid(row = 3, column = 3, columnspan = 2, pady = 20)
    cambia = tk.Button(text = "Istogramma", command = cambio_grafico1, font = ("Product Sans", 10),
                    activebackground = "#1cb904", activeforeground = "white", fg = "white",
                    highlightthickness = 0, background = "#3498db", borderwidth= 0, width = 10)
    cambia.grid(row = 4, column = 3, sticky = "W")
    labelgraf = tk.Label(window, text = "Andamento NDVI nell'intervallo selezionato", font = ("Product Sans", 12), 
                   background = "white" )
    labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "E", padx = 20)
         
def zoomerP(event):
        canva1.scale("all", event.x, event.y, 1.5, 1.5)
        canva1.configure(scrollregion = canva1.bbox("all"))
def zoomerM(event):
        canva1.scale("all", event.x, event.y, 0.5, 0.5)
        canva1.configure(scrollregion = canva1.bbox("all"))    
       
###Funzioni cancellazione TextBox quando hanno il focus        
def cancellaX(event): inputX.delete(0, tk.END)
def cancellaY(event): inputY.delete(0, tk.END)    

#Funzione per convertire mese in numero
def monthNumber(mese):
    switcher = {
        'Gennaio': '01', 'Febbraio': '02', 'Marzo': '03', 'Aprile': '04',  
        'Maggio': '05', 'Giugno': '06', 'Luglio': '07',  'Agosto': '08', 
        'Settembre': '09', 'Ottobre': '10', 'Novembre': '11', 'Dicembre': '12'
        } 
    return switcher[mese]

#Funzione per controllo errori su coordinate
def checkCoord():
    if inputX.get():
        coordinataX = inputX.get()
        if (coordinataX == "Coordinata X"):
            messagebox.showerror("Errore coordinata", "Inserire coordinata X")
            return False
        if (coordinataX.find(".") !=2):
            messagebox.showerror("Errore coordinata", "Inserire una coordinata X corretta!")
            return False
    else:
        messagebox.showerror("Errore coordinata", "Coordinata X vuota!")
        return False
    if inputY.get():
        coordinataY = inputX.get()
        if (coordinataX == "Coordinata Y"):
            messagebox.showerror("Errore coordinata", "Inserire coordinata Y")
            return False
        if (coordinataY.find(".") != 2):
            messagebox.showerror("Errore coordinata", "Inserire una coordinata Y corretta!")
            return False
    else:
        messagebox.showerror("Errore coordinata", "Coordinata Y vuota!")
        return False

#Funzione per controllo sulle date inserite
def checkDate():
    oggi = date.today()
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
    dataI = datetime.date(annoI, meseI, giornoI)
    dataF = datetime.date(annoF, meseF, giornoF)
    if (dataI < satellite):
        messagebox.showerror("Errore data", "Data iniziale precendente al lancio del satellite (23/06/2015)!")
        return False
    if (dataF < dataI):
        messagebox.showerror("Errore data", "Data finale minore della data iniziale!")
        return False
    if (oggi < dataI or oggi < dataF):
        messagebox.showerror("Errore data", "Data odierna superata!")
        return False
    
    
#SEZIONE 3 - DEFINIZIONE INTERFACCIA
###Riga 1    
punto_label = tk.Label(window, text="Coordinate del punto : ", font = ("Product Sans", 14), background = "white")
punto_label.grid(row = 0, column = 0, padx = 30, pady = 30, sticky = "E")
pos_ico = PhotoImage(file="/home/antonio/Documenti/position.png")
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

ok_ico = PhotoImage(file="/home/antonio/Documenti/ok.png")
applica = tk.Button(text = "Applica!", command = controllo_testo, font = ("Product Sans", 14),
                    activebackground = "#1cb904", activeforeground = "white", fg = "white",
                    highlightthickness = 0, background = "#3498db", borderwidth= 0,
                    image = ok_ico, compound = LEFT)
applica.grid(row=0, column=4, padx = 40, pady = 30, sticky = "W")

ndvimess = tk.Label(window, text = "La zona potrebbe essere irrigata", font = ("Product Sans", 14), 
                   background = "white", fg = "green" )
ndvimess.grid(row = 2, column = 3, columnspan = 2, sticky = "WE", padx = 20)

###Riga 2
cal_ico = PhotoImage(file="/home/antonio/Documenti/calendar.png")
calendar = tk.Label(window, image = cal_ico, background = "white", borderwidth = 0)
calendar.grid(row = 1, column = 0, rowspan = 2, padx = 120, pady = 10, sticky = "W")
inizio = tk.Label(window, text = "Inizio osservazione : ", 
                  font = ("Product Sans", 14), background = "white")
inizio.grid(row = 1, column = 0, padx = 30, pady = 5, sticky = "E")
fine = tk.Label(window, text = "Fine osservazione : ", 
                font = ("Product Sans", 14), background = "white")
fine.grid(row = 2, column = 0, padx = 30, pady = 5, sticky = "E")

#####Anno di inizio
stringa_anno1 = tk.StringVar(window)
stringa_anno1.set("Anno")
menuAnniI = tk.OptionMenu(window, stringa_anno1, "2019", "2018", "2017", "2016", "2015")
menuAnniI.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 5, 
                  highlightthickness=0, borderwidth = 0, activebackground = "#3498db", activeforeground = "white")
menuAnniI["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                            relief=tk.GROOVE, font = ("Product Sans", 9))
menuAnniI.grid(row = 1, column = 1, sticky = "E")

######Anno di fine
stringa_anno2 = tk.StringVar(window)
stringa_anno2.set("Anno")
menuAnniF = tk.OptionMenu(window, stringa_anno2, "2019", "2018", "2017", "2016", "2015")
menuAnniF.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 5, 
                  highlightthickness=0, borderwidth = 0, activebackground = "#3498db", activeforeground = "white")
menuAnniF["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                               relief=tk.GROOVE, font = ("Product Sans", 9))
menuAnniF.grid(row = 2, column = 1, sticky = "E")

######Mese di inizio
stringa_mese1 = tk.StringVar(window)
stringa_mese1.set("Mese")
menuMesiI = tk.OptionMenu(window, stringa_mese1,  "Gennaio", "Febbraio", "Marzo", "Aprile", 
            "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre")
menuMesiI.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 7, 
                  highlightthickness=0, borderwidth = 0, activebackground = "#3498db", activeforeground = "white")
menuMesiI["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                               relief=tk.GROOVE, font = ("Product Sans", 9))
menuMesiI.grid(row = 1, column = 1, columnspan = 2)

######Mese di fine
stringa_mese2 = tk.StringVar(window)
stringa_mese2.set("Mese")
menuMesiF = tk.OptionMenu(window, stringa_mese2, "Gennaio", "Febbraio", "Marzo", "Aprile", 
             "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre")
menuMesiF.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 7, 
                  highlightthickness=0, borderwidth = 0, activebackground = "#3498db", activeforeground = "white")
menuMesiF["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                               relief=tk.GROOVE, font = ("Product Sans", 9))
menuMesiF.grid(row = 2, column = 1, columnspan=2)

######Giorno di inizio
stringa_giorno1 = tk.StringVar(window)
stringa_giorno1.set("Giorno")
menuGiorniI = tk.OptionMenu(window, stringa_giorno1, "1", "2", "3", "4", "5", "6", "7", "8", "9", 
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", 
            "25", "26", "27", "28", "29", "30", "31")
menuGiorniI.config(bg = "gray97", relief = tk.GROOVE, font = ("Product Sans", 12), width = 5, 
                   highlightthickness=0, borderwidth= 0, activebackground = "#3498db", activeforeground = "white")
menuGiorniI["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                               relief=tk.GROOVE, font = ("Product Sans", 9))
menuGiorniI.grid(row = 1, column = 1, columnspan = 2, sticky = "W")

######Giorno di fine
stringa_giorno2 = tk.StringVar(window)
stringa_giorno2.set("Giorno")
menuGiorniF = tk.OptionMenu(window, stringa_giorno2, "1", "2", "3", "4", "5", "6", "7", "8", "9", 
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", 
            "25", "26", "27", "28", "29", "30", "31")
menuGiorniF.config(bg = "gray97", relief=tk.GROOVE, font = ("Product Sans", 12), width = 5,
                    highlightthickness=0, borderwidth = 0, activebackground = "#3498db", activeforeground = "white")
menuGiorniF["menu"].configure(borderwidth = 0, activebackground = "#3498db", activeforeground = "white",
                               relief=tk.GROOVE, font = ("Product Sans", 9))
menuGiorniF.grid(row = 2, column = 1, columnspan = 2, sticky = "W")

###Riga 3
canva1 = Canvas(window, width = 640, height = 390)
canva1.config(bd = 0, highlightbackground = "white")
mappa = Image.open("/home/antonio/Documenti/Screen.png")
mappa = mappa.resize((640, 390), Image.ANTIALIAS)
mappa.save("/home/antonio/Documenti/mappa_re.png")
map_ = Image.open("/home/antonio/Documenti/mappa_re.png")
canva1.image = ImageTk.PhotoImage(map_)
canva1.create_image(0, 0, image = canva1.image, anchor = "nw")
canva1.grid(row = 3, column = 0, columnspan = 2, padx = 30)
canva1.bind("<Button-4>", zoomerP)
canva1.bind("<Button-5>", zoomerM)

canva2 = Canvas(window, width = 520, height = 390)
canva2.config(bd = 0, highlightbackground = "white")
grafico = Image.open("/home/antonio/Documenti/chart.png")
grafico = grafico.resize((520, 390), Image.ANTIALIAS)
grafico.save("/home/antonio/Documenti/chart_re.png")
graf = Image.open("/home/antonio/Documenti/chart_re.png")
canva2.image = ImageTk.PhotoImage(graf)
canva2.create_image(0, 0, image = canva2.image, anchor = "nw")
canva2.grid(row = 3, column = 3, columnspan = 2, pady = 20) 


###Riga 4 
blu = PhotoImage(file = "/home/antonio/Documenti/blue.png")
blu_label = tk.Label(window, image = blu)
blu_label.grid(row = 4, column = 0, padx = 45, sticky = "W")
legend1 = tk.Label(window, text = "Campi sicuramente irrigati", font = ("Product Sans", 10), 
                   background = "white")
legend1.grid(row = 4, column = 0, sticky = "W", padx = 65)

cambia = tk.Button(text = "Istogramma", command = cambio_grafico1, font = ("Product Sans", 10),
                    activebackground = "#1cb904", activeforeground = "white", fg = "white",
                    highlightthickness = 0, background = "#3498db", borderwidth= 0, width = 10)
cambia.grid(row = 4, column = 3, sticky = "W")
labelgraf = tk.Label(window, text = "Andamento NDVI nell'intervallo selezionato", font = ("Product Sans", 12), 
                   background = "white", width = 30 )
labelgraf.grid(row = 4, column = 3, columnspan = 2, sticky = "E", padx = 20)

###Riga 5
rosso = PhotoImage(file="/home/antonio/Documenti/red.png")
rosso_label = tk.Label(window, image = rosso)
rosso_label.grid(row = 5, column = 0, padx = 45, sticky = "W")
legend2 = tk.Label(window, text = "Campi sicuramente non irrigati", font = ("Product Sans", 10), 
                   background = "white")
legend2.grid(row = 5, column = 0, sticky = "W", padx = 65)

###Riga 6
firma = tk.Label(window, text = "Antonio Tandoi - 2018/2019", font = ("Product Sans", 7), 
                   background = "white" )
firma.grid(row = 6, column = 4, sticky = "E", pady = 30, padx = 10)
window.mainloop()
