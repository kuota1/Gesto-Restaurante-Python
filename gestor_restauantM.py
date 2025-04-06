from tkinter import *
import csv
import os
import datetime
from tkinter import filedialog, messagebox

operador = ""
precios_comida = [115, 165, 231, 322, 122, 199, 205, 265]
precios_bebida = [25, 29, 25, 54, 80, 80, 60, 58]
precios_postres = [54, 68, 32, 97, 55, 64, 94, 74]

def click_boton(numero):
    global operador
    operador = operador + numero
    visor_calculadora.delete(0,END)
    visor_calculadora.insert(END,operador)

def borrar():
    global operador
    operador = ""
    visor_calculadora.delete(0,END)

def obtener_resultado():
    global operador
    resultado=str(eval(operador))
    visor_calculadora.delete(0,END)
    visor_calculadora.insert(0,resultado)
    operador = ""

def validar_entrada(valor):
    return valor.isdigit() or valor ==""


def revisar_check():
    #comida
    x = 0
    for c in cuadros_comidas:
        if variable_comida[x].get() == 1:
            cuadros_comidas[x].config(state=NORMAL)
            if cuadros_comidas[x].get() == '0':
                cuadros_comidas[x].delete(0, END)
            cuadros_comidas[x].focus()
        else:
            cuadros_comidas[x].config(state=DISABLED)
            texto_comida[x].set('0')
        x += 1
    #bebida
    x = 0
    for c in cuadros_bebida:
        if variable_bebida[x].get() == 1:
            cuadros_bebida[x].config(state=NORMAL)
            if cuadros_bebida[x].get() == '0':
                cuadros_bebida[x].delete(0, END)
            cuadros_bebida[x].focus()
        else:
            cuadros_bebida[x].config(state=DISABLED)
            texto_bebida[x].set('0')
        x += 1

    #postre
    x = 0
    for c in cuadros_postres:
        if variable_postres[x].get() == 1:
            cuadros_postres[x].config(state=NORMAL)
            if cuadros_postres[x].get() == '0':
                cuadros_postres[x].delete(0, END)
            cuadros_postres[x].focus()
        else:
            cuadros_postres[x].config(state=DISABLED)
            texto_postres[x].set("0")
        x += 1

def total():
    #comida
    sub_total_comida = 0
    p=0
    for cantidad in texto_comida:
        sub_total_comida = sub_total_comida + (float(cantidad.get()) * precios_comida[p])
        p += 1

    #bebida
    sub_total_bebida = 0
    p = 0
    for cantidad in texto_bebida:
        sub_total_bebida = sub_total_bebida + (float(cantidad.get()) * precios_bebida[p])
        p += 1

    #postre
    sub_total_postres = 0
    p = 0
    for cantidad in texto_postres:
        sub_total_postres = sub_total_postres + (float(cantidad.get()) * precios_postres[p])
        p += 1

    sub_total= sub_total_comida + sub_total_bebida + sub_total_postres
    impuestos= sub_total * 0.16
    total= sub_total+impuestos

    var_costo_comida.set(f"$ {round(sub_total_comida,2)}")
    var_costo_bebida.set(f"$ {round(sub_total_bebida, 2)}")
    var_costo_postre.set(f"$ {round(sub_total_postres, 2)}")
    var_subtotal.set(f"$ {round(sub_total, 2)}")
    var_impuesto.set(f"$ {round(impuestos, 2)}")
    var_total.set(f"$ {round(total, 2)}")

def recibo():
    texto_recibo.delete(1.0, END)

    # Obtener o crear número de ticket
    ruta_contador = "contador_tickets.txt"
    if not os.path.exists(ruta_contador):
        with open(ruta_contador, "w") as f:
            f.write("1")
    with open(ruta_contador, "r") as f:
        num_ticket = int(f.read().strip())

    # Fecha y encabezado del recibo
    fecha = datetime.datetime.now()
    fecha_recibo = f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year} - {fecha.hour:02d}:{fecha.minute:02d}"
    texto_recibo.insert(END, f"Datos:\t{num_ticket}\t\t{fecha_recibo}\n")
    texto_recibo.insert(END, "*" * 48 + "\n")
    texto_recibo.insert(END, f'{"Producto":<20}{"cant.":<10}{"Costo"}\n')
    texto_recibo.insert(END, "-" * 48 + "\n")

    # Historial CSV
    ruta_csv = "historial_ventas.csv"
    existe_csv = os.path.exists(ruta_csv)
    with open(ruta_csv, "a", newline="") as archivo_csv:
        write = csv.writer(archivo_csv)
        if not existe_csv:
            write.writerow(["ticket", "fecha", "producto", "cantidad", "costo"])

        # Comida
        for i, comida in enumerate(texto_comida):
            if comida.get() != "0":
                nombre = lista_comidas[i]
                cantidad = comida.get()
                costo = int(cantidad) * precios_comida[i]
                texto_recibo.insert(END, f"{nombre:<20}{cantidad:<10}${costo:.2f}\n")
                write.writerow([num_ticket, fecha_recibo, nombre, cantidad, costo])

        # Bebida
        for i, bebida in enumerate(texto_bebida):
            if bebida.get() != "0":
                nombre = lista_bebidas[i]
                cantidad = bebida.get()
                costo = int(cantidad) * precios_bebida[i]
                texto_recibo.insert(END, f"{nombre:<20}{cantidad:<10}${costo:.2f}\n")
                write.writerow([num_ticket, fecha_recibo, nombre, cantidad, costo])

        # Postre
        for i, postres in enumerate(texto_postres):
            if postres.get() != "0":
                nombre = lista_postres[i]
                cantidad = postres.get()
                costo = int(cantidad) * precios_postres[i]
                texto_recibo.insert(END, f"{nombre:<20}{cantidad:<10}${costo:.2f}\n")
                write.writerow([num_ticket, fecha_recibo, nombre, cantidad, costo])

    # Totales
    texto_recibo.insert(END, "-" * 70 + "\n")
    texto_recibo.insert(END, f"Costo de la Comida: \t\t\t{var_costo_comida.get()}\n")
    texto_recibo.insert(END, f"Costo de la Bebida: \t\t\t{var_costo_bebida.get()}\n")
    texto_recibo.insert(END, f"Costo de la Postre: \t\t\t{var_costo_postre.get()}\n")
    texto_recibo.insert(END, "-" * 70 + "\n")
    texto_recibo.insert(END, f"Sub-total: \t\t\t{var_subtotal.get()}\n")
    texto_recibo.insert(END, f"IVA: \t\t\t{var_impuesto.get()}\n")
    texto_recibo.insert(END, f"Total: \t\t\t{var_total.get()}\n")
    texto_recibo.insert(END, "*" * 58 + "\n")
    texto_recibo.insert(END, "Lo esperamos pronto")

    # Incrementar número de ticket
    with open(ruta_contador, "w") as f:
        f.write(str(num_ticket + 1))


def guardar():
    info_recibo=texto_recibo.get(1.0,END)
    archivo = filedialog.asksaveasfile(mode="w",defaultextension=".txt")
    if archivo:
        archivo.write(info_recibo)
        archivo.close()
        messagebox.showinfo("informacion","su recibo ha sido guardado")
    else:
        messagebox.showinfo("informacion","Su recibo no fue guardado")

def resetear():
    texto_recibo.delete(0.1,END)
    for texto in texto_comida:
        texto.set(0)
    for texto in texto_bebida:
        texto.set(0)
    for texto in texto_postres:
        texto.set(0)

    for cuadro in cuadros_comidas:
        cuadro.config(state=DISABLED)
    for cuadro in cuadros_bebida:
        cuadro.config(state=DISABLED)
    for cuadro in cuadros_postres:
        cuadro.config(state=DISABLED)

    for v in variable_comida:
        v.set(0)
    for v in variable_bebida:
        v.set(0)
    for v in variable_postres:
        v.set(0)

    var_costo_comida.set("")
    var_costo_bebida.set("")
    var_costo_postre.set("")
    var_subtotal.set("")
    var_impuesto.set("")
    var_total.set("")

#iniciar tkinter
aplicacion = Tk()

#tamaño de la ventana
aplicacion.geometry("1140x630+0+0")

#evitar maximizar
aplicacion.resizable(0,0)

#titulo de ventana
aplicacion.title("Sistema de Facturacion y Gestor de restaurante")

#color de fondo de la ventana
aplicacion.config(bg="dark salmon")

#panel superior
panel_superior = Frame(aplicacion, bd=1, relief=GROOVE)
panel_superior.pack(side=TOP)

#etiqueta titulo
etiqueta_titulo=Label(panel_superior, text="Sistema de Facturacion", fg="azure4", font=("Dosis",58), bg="dark salmon", width=20)
etiqueta_titulo.grid(row=0,column=0)

# panel izquierdo
panel_izquierdo=Frame(aplicacion,bd=1, relief=GROOVE)
panel_izquierdo.pack(side=LEFT)

#etiqueta costos
panel_costos = Frame(panel_izquierdo, bd=1, relief=GROOVE,bg="azure4",padx=50)
panel_costos.pack(side=BOTTOM)

#panel comida
panel_comida = LabelFrame(panel_izquierdo,text="Comida",font=("Dosis", 19,"bold"), bd=1, relief=GROOVE, fg="azure4")
panel_comida.pack(side=LEFT)


#panel bebidas
panel_bebidas = LabelFrame(panel_izquierdo,text="Bebidas",font=("Dosis", 19,"bold"), bd=1, relief=GROOVE, fg="azure4")
panel_bebidas.pack(side=LEFT)

#panel postres
panel_postres = LabelFrame(panel_izquierdo,text="Postres",font=("Dosis", 19,"bold"), bd=1, relief=GROOVE, fg="azure4")
panel_postres.pack(side=LEFT)

#panel derecha
panel_derecha=Frame(aplicacion, bd=1, relief=GROOVE)
panel_derecha.pack(side=RIGHT)

#panel calculadora
panel_calculadora = Frame(panel_derecha, bd=1, relief=GROOVE, bg="burlywood")
panel_calculadora.pack()

#panel recibo
panel_recibo = Frame(panel_derecha, bd=1, relief=GROOVE, bg="burlywood")
panel_recibo.pack()

#panel botones
panel_botones = Frame(panel_derecha, bd=1, relief=GROOVE, bg="burlywood")
panel_botones.pack()

#lista de productos
lista_comidas =["pollo", "cordero","salmon","asado", "kebab", "pizza1","costillar","filete"]
lista_bebidas= ["agua","joya","jugo","coca","vino1","vino2","cerveza1","cerveza2"]
lista_postres= ["helado","fruta","brownies","flan","mousse","pastel1","pastel2","pastel3"]

#generar items comida
variable_comida=[]
cuadros_comidas=[]
texto_comida=[]
contador = 0
for i in lista_comidas:
    #crear checkbutton
    variable_comida.append("")
    variable_comida[contador]=IntVar()
    i = Checkbutton(panel_comida,
                    text=i.title(),
                    font=("Dosis",19,"bold"),
                    onvalue=1,offvalue=0,
                    variable=variable_comida[contador],
                    command=revisar_check)
    i.grid(row=contador,column=0, sticky=W)

    #crear los cuadros de entrada
    validacion= aplicacion.register(validar_entrada)
    cuadros_comidas.append("")
    texto_comida.append("")
    texto_comida[contador]=StringVar()
    texto_comida[contador].set("0")
    cuadros_comidas[contador]= Entry(panel_comida,
                                     font=("Dosis",18,"bold"),
                                     bd=1,width=6,
                                     state=DISABLED,
                                     textvariable=texto_comida[contador],
                                     validate="key",
                                     validatecommand=(validacion,"%P"))
    cuadros_comidas[contador].grid(row=contador,column=1)

    contador+=1

#generar items bebida
variable_bebida=[]
cuadros_bebida=[]
texto_bebida=[]
contador = 0
for n in lista_bebidas:
    # crear checkbutton
    validacion = aplicacion.register(validar_entrada)
    variable_bebida.append("")
    variable_bebida[contador]=IntVar()
    n = Checkbutton(panel_bebidas,text=n.title(),
                    font=("Dosis",19,"bold"),
                    onvalue=1,offvalue=0,
                    variable=variable_bebida[contador],
                    command=revisar_check)
    n.grid(row=contador,column=0, sticky=W)
    # crear los cuadros de entrada
    cuadros_bebida.append("")
    texto_bebida.append("")
    texto_bebida[contador]=StringVar()
    texto_bebida[contador].set("0")
    cuadros_bebida[contador] = Entry(panel_bebidas,
                                      font=("Dosis", 18, "bold"),
                                      bd=1, width=6,
                                      state=DISABLED,
                                      textvariable=texto_bebida[contador],
                                      validate="key",
                                      validatecommand=(validacion, "%P"))
    cuadros_bebida[contador].grid(row=contador, column=1)
    contador+=1

#generar items postres
variable_postres=[]
cuadros_postres=[]
texto_postres=[]
contador = 0
for z in lista_postres:
    # crear checkbutton
    validacion = aplicacion.register(validar_entrada)
    variable_postres.append("")
    variable_postres[contador]=IntVar()
    z = Checkbutton(panel_postres,
                    text=z.title(),
                    font=("Dosis",19,"bold"),
                    onvalue=1,offvalue=0,
                    variable=variable_postres[contador],
                    command=revisar_check)
    z.grid(row=contador,column=0, sticky=W)
    # crear los cuadros de entrada
    cuadros_postres.append("")
    texto_postres.append("")
    texto_postres[contador]=StringVar()
    texto_postres[contador].set("0")

    cuadros_postres[contador] = Entry(panel_postres,
                                      font=("Dosis", 18, "bold"),
                                      bd=1, width=6,
                                      state=DISABLED,
                                      textvariable=texto_postres[contador],
                                      validate="key",
                                      validatecommand=(validacion, "%P"))
    cuadros_postres[contador].grid(row=contador, column=1)
    contador+=1

    # variables
var_costo_comida = StringVar()
var_costo_bebida = StringVar()
var_costo_postre = StringVar()
var_subtotal = StringVar()
var_impuesto = StringVar()
var_total = StringVar()

#etiquetas de costos y campos de entrada
#comida
etiqueta_costo_comida=Label(panel_costos,
                            text="costo comida",
                            font=("Dosis",12,"bold"),
                            bg="azure4",
                            fg="white")
etiqueta_costo_comida.grid(row=0,column=0)
texto_costo_comida=Entry(panel_costos,
                         font=
                         ("Dosis",12,"bold"),
                         bd=1, width=10,
                         state="readonly",
                         textvariable=var_costo_comida)
texto_costo_comida.grid(row=0,column=1,padx=41)

#bebida
etiqueta_costo_bebida=Label(panel_costos,
                            text="costo bebida",
                            font=("Dosis",12,"bold"),
                            bg="azure4",
                            fg="white")
etiqueta_costo_bebida.grid(row=1,column=0)
texto_costo_bebida=Entry(panel_costos,
                         font= ("Dosis",12,"bold"),
                         bd=1, width=10,
                         state="readonly",
                         textvariable=var_costo_bebida)
texto_costo_bebida.grid(row=1,column=1,padx=41)

#postre
etiqueta_costo_postre=Label(panel_costos,
                            text="costo postre",
                            font=("Dosis",12,"bold"),
                            bg="azure4",
                            fg="white")
etiqueta_costo_postre.grid(row=2,column=0)
texto_costo_postre=Entry(panel_costos,
                         font= ("Dosis",12,"bold"),
                         bd=1, width=10,
                         state="readonly",
                         textvariable=var_costo_postre)
texto_costo_postre.grid(row=2,column=1,padx=41)

#subtotal
etiqueta_subtotal=Label(panel_costos,
                            text="subtotal",
                            font=("Dosis",12,"bold"),
                            bg="azure4",
                            fg="white")
etiqueta_subtotal.grid(row=0,column=2)
texto_subtotal=Entry(panel_costos,
                         font= ("Dosis",12,"bold"),
                         bd=1, width=10,
                         state="readonly",
                         textvariable=var_subtotal)
texto_subtotal.grid(row=0,column=3,padx=41)

#IVA
etiqueta_impuesto=Label(panel_costos,
                            text="IVA",
                            font=("Dosis",12,"bold"),
                            bg="azure4",
                            fg="white")
etiqueta_impuesto.grid(row=1,column=2)
texto_impuesto=Entry(panel_costos,
                         font= ("Dosis",12,"bold"),
                         bd=1, width=10,
                         state="readonly",
                         textvariable=var_impuesto)
texto_impuesto.grid(row=1,column=3,padx=41)

#total
etiqueta_total=Label(panel_costos,
                            text="Total",
                            font=("Dosis",12,"bold"),
                            bg="azure4",
                            fg="white")
etiqueta_total.grid(row=2,column=2)
texto_total=Entry(panel_costos,
                         font= ("Dosis",12,"bold"),
                         bd=1, width=10,
                         state="readonly",
                         textvariable=var_total)
texto_total.grid(row=2,column=3,padx=41)

#botones
botones=["total","recibo", "guardar","resetear"]
botones_creados=[]

columnas=0
for boton in botones:
    boton = Button(panel_botones,
                   text=boton.title(),
                   font=("Dosis",14,"bold"),
                    fg="white",
                    bg="azure4",
                    bd=1,
                    width=9)
    botones_creados.append(boton)
    boton.grid(row=0,column=columnas)
    columnas+=1

botones_creados[0].config(command=total)
botones_creados[1].config(command=recibo)
botones_creados[2].config(command=guardar)
botones_creados[3].config(command=resetear)

#area de recibo
texto_recibo=Text(panel_recibo,
                  font=("Courier", 11, "bold"),
                  bd=1,
                  width=48,#42
                  height=10)#10
texto_recibo.grid(row=0,column=0)

#calculadora
visor_calculadora=Entry(panel_calculadora,
                        font=("Dosis",16,"bold"),
                        width=32,
                        bd=1)
visor_calculadora.grid(row=0,column=0,columnspan=4)

botones_calculadora=["7","8","9","+",
                     "4","5","6","-",
                     "1","2","3","x",
                     "B","0","=","/"]
botones_guardados = []

fila= 1
columna = 0
for boton in botones_calculadora:
    boton = Button(panel_calculadora,
                   text=boton.title(),
                   font=("Dosis",16,"bold"),
                   fg="white",
                   bg="azure4",
                   bd=1,
                   width=8)
    botones_guardados.append(boton)

    boton.grid(row=fila,column=columna)

    if columna ==3:
        fila +=1

    columna +=1

    if columna == 4:
        columna = 0

botones_guardados[0].config(command=lambda : click_boton("7"))
botones_guardados[1].config(command=lambda : click_boton("8"))
botones_guardados[2].config(command=lambda : click_boton("9"))
botones_guardados[3].config(command=lambda : click_boton("+"))
botones_guardados[4].config(command=lambda : click_boton("4"))
botones_guardados[5].config(command=lambda : click_boton("5"))
botones_guardados[6].config(command=lambda : click_boton("6"))
botones_guardados[7].config(command=lambda : click_boton("-"))
botones_guardados[8].config(command=lambda : click_boton("1"))
botones_guardados[9].config(command=lambda : click_boton("2"))
botones_guardados[10].config(command=lambda : click_boton("3"))
botones_guardados[11].config(command=lambda : click_boton("*"))
botones_guardados[13].config(command=lambda : click_boton("0"))
botones_guardados[15].config(command=lambda : click_boton("/"))
botones_guardados[12].config(command=borrar)
botones_guardados[14].config(command=obtener_resultado)


#evitar que la pantalla se cierre
aplicacion.mainloop()