"""
APP que realiza calculos de lotaje con la informacion ingresada por el usuario

Toma el Balance de la cuenta 
El $ a arriesgar
La diferencia de Pip entre el precio actual y el precio del SL

En base ha eso genera el calculo del lotaje e ingresa una orden 1:3 R:B

"""


import MetaTrader5 as mt5
import tkinter as tk

from tkinter import *
from tkinter import ttk


# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()


#Creamos INTERFAZ
app = tk.Tk()
app.geometry('250x400')
app.title("Forexito")

#Label Par
labelTop = tk.Label(app,
                    text = "Elija su par")
labelTop.grid(column=0, row=1)

#BALANCE
labelBalance=tk.Label(app,
                    text = 'Balance:$')
labelBalance.grid(column=0, row=0)
labelBalance1=tk.Label(app,
                    text = '')
labelBalance1.grid(column=1, row=0)


# Lista de Pares
comboExample = ttk.Combobox(app,
                            values=[
                                    "GBPJPY",
                                    ],
                                    state="readonly")


# Se ejecuta este evento cada vez que se elige un par desde la lista
def defocus(event):


    event.widget.master.focus_set()
    
    entrysl.delete(0, tk.END)

    #Obtenemos el Par para hacer calculos
    par = comboExample.get()

    if(len(par)!=0):

        selected=mt5.symbol_select(par,True)

        info_par =mt5.symbol_info_tick(par)._asdict()
        symbol_info_dict = mt5.symbol_info(par)._asdict()
        #print(info_par)

        ask = info_par['ask']
        bid = info_par['bid']
        spr = symbol_info_dict['spread']/10.0

        labelAsk1.configure(text= ask)
        labelBid1.configure(text= bid)
        labelSpread1.configure(text= spr)
        entrysl.insert(0, ask)

        account_info_dict = mt5.account_info()._asdict()
        bal =account_info_dict['balance']

        labelBalance1.configure(text=bal)
####################################
#Construimos Interfaz

#Lista de Pares
comboExample.grid(column=0, row=2)
comboExample.bind("<FocusIn>", defocus)
#comboExample.current(1)

# Precio Ask del Par
labelAsk = tk.Label(app,
                    text = "Ask:")
labelAsk.grid(column=0, row=3)

labelAsk1 = tk.Label(app, text="")
labelAsk1.grid(column=1, row=3)

# Precio BID del Par
labelBid =tk.Label(app,
                    text = "Bid:")
labelBid.grid(column=0, row=4)
labelBid1 = tk.Label(app, text="")
labelBid1.grid(column=1, row=4)

# Spread del Par
labelSpread =tk.Label(app,
                    text = "Spread:")
labelSpread.grid(column=0, row=5)
labelSpread1 = tk.Label(app, text="")
labelSpread1.grid(column=1, row=5)

# Label Lotaje Calcculado
labelLot =tk.Label(app,
                    text = "Lot:")
labelLot.grid(column=0, row=6)
labelLot1 = tk.Label(app, text="")
labelLot1.grid(column=1, row=6)

#PIP SL
labelpsl =tk.Label(app,
                    text = "P_SL:")
labelpsl.grid(column=0, row=7)
labelpsl1 = tk.Label(app, text="")
labelpsl1.grid(column=1, row=7)

#PIP TP
labelptp =tk.Label(app,
                    text = "P_TP:")
labelptp.grid(column=0, row=8)
labelptp1 = tk.Label(app, text="")
labelptp1.grid(column=1, row=8)

# Label Dinero de Riesgo
labelRiesgo =tk.Label(app,
                    text = "Riesgo $:")
labelRiesgo.grid(column=0, row=9)
labelRiesgo1 = tk.Label(app, text="")
labelRiesgo1.grid(column=1, row=9)

# Label Dinero de Beneficio
labelGanan =tk.Label(app,
                    text = "Ganan $:")
labelGanan.grid(column=0, row=10)
labelGanan1 = tk.Label(app, text="")
labelGanan1.grid(column=1, row=10)

#########################################
# Label SL
labelsl=Label(app,text = 'SL')
labelsl.grid(column=0, row=11)

#Introducir Precio SL
entrysl = ttk.Entry(app)
entrysl.grid(column=0, row=12)

""""
# Label %
labelpor=Label(app,text = '%')
labelpor.grid(column=0, row=13)

#Introducir % de Riesgo
entrypor = ttk.Entry(app)
entrypor.grid(column=0, row=14)
"""

# Dinero a Ariesgar
labelpor=Label(app,text = '$ Riesgo')
labelpor.grid(column=0, row=13)

#Introducir % de Riesgo
entrypor = ttk.Entry(app)
entrypor.grid(column=0, row=14)

# Funcion que Calcula el Lotaje
def calcular_lotaje(par,por,sl,bal):
    #par
    #balance
    #% riesgo
    #pip sl

    bal = float(bal)
    par = par
    
    # Ahora de debe calcular el % ya que la variable de entrada es el $
    
    por = (float(por)*100)/bal
    
    #por =float(por)
    sl = float(sl)

    #Actualizamos
    if(par == "GBPJPY"):
        """
        pedimos precio  ya que nuestra moneda base es el USD y estamos transando GBP
        """
        symbol_info_dict = mt5.symbol_info("GBPUSD")._asdict()

        aux_ask =symbol_info_dict['ask']
        
        print("aux_ask:",aux_ask)

        factor = aux_ask/10
        print("factor:",factor)

    riesgo = bal * por / 100
    #print(riesgo,type(riesgo))
    win = riesgo *3
    #print(win,type(win))
    lotsize = riesgo / sl  * factor
    #print(lotsize,type(lotsize))

    return(riesgo,lotsize,win)

# Funcion que mete Venta
def ordenventa():
    text_sl  = float(entrysl.get())
    text_por = float(entrypor.get())
    par = comboExample.get()

    #Cantidad de 0
    decimal =0

    selected=mt5.symbol_select(par,True)


    info_par =mt5.symbol_info_tick(par)._asdict()
    symbol_info_dict = mt5.symbol_info(par)._asdict()

    ask = info_par['ask']
    bid = info_par['bid']
    spr = symbol_info_dict['spread']
    dig = symbol_info_dict['digits']

    print("ASK:",ask)
    print("BID:",bid)
    print("SPREAD:",spr)
    print("DIG:",dig)

    account_info_dict = mt5.account_info()._asdict()
    bal =account_info_dict['balance']


    print("Bal:$",bal)

    pip_sl = abs(bid - text_sl)

    if(dig == 3):
        pip_sl = pip_sl*100
        decimal = 100
    elif(dig == 5):
        pip_sl = pip_sl *10000
        decimal = 10000
    print("Pip:",pip_sl)


    perdida,lot,win = calcular_lotaje(par,text_por,pip_sl,bal)

    print("perdida :$",perdida)
    print("Lotaje:",lot)

    labelLot1.configure(text=round(lot,3))
    labelRiesgo1.configure(text=perdida)

    labelGanan1.configure(text=win)

    labelpsl1.configure(text=round(pip_sl,2))
    labelptp1.configure(text=round(pip_sl*3,2))

    labelStatus1.configure(text="Ok")

    print("############################")

    point = mt5.symbol_info(par).point

    tp = round(bid-((pip_sl*3)/decimal),5)

    print("TP:",tp)

    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": par,
    "volume": round(lot,2),
    "type": mt5.ORDER_TYPE_SELL,
    "price": bid,
    "sl": text_sl,
    "tp":tp,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
    }


    # enviamos la solicitud comercial
    result = mt5.order_send(request)

    print(result)

# Funcion que mete Compra
def ordencompra():
    text_sl  = float(entrysl.get())
    text_por = float(entrypor.get())
    par = comboExample.get()

    #Cantidad de 0
    decimal =0

    selected=mt5.symbol_select(par,True)


    info_par =mt5.symbol_info_tick(par)._asdict()
    symbol_info_dict = mt5.symbol_info(par)._asdict()

    ask = info_par['ask']
    bid = info_par['bid']
    spr = symbol_info_dict['spread']

    dig = symbol_info_dict['digits']

    print("ASK:",ask)
    print("BID:",bid)
    print("SPREAD:",spr)
    print("DIG:",dig)

    account_info_dict = mt5.account_info()._asdict()
    bal =account_info_dict['balance']

    print("Bal:$",bal)

    pip_sl =abs(ask - text_sl)

    if(dig == 3):
        pip_sl = pip_sl*100
        decimal = 100
    elif(dig == 5):
        pip_sl = pip_sl *10000
        decimal = 10000
    print("Pip:",pip_sl)

    perdida,lot,win = calcular_lotaje(par,text_por,pip_sl,bal)

    print("perdida :$",perdida)
    print("Lotaje:",lot)

    labelLot1.configure(text=round(lot,3))
    labelRiesgo1.configure(text=perdida)

    labelpsl1.configure(text=round(pip_sl,2))
    labelptp1.configure(text=round(pip_sl*3,2))

    labelGanan1.configure(text=win)

    labelStatus1.configure(text="Ok")

    print("############################")

    point = mt5.symbol_info(par).point

    tp = round(ask+((pip_sl*3)/decimal),5)

    print("TP:",tp)

    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": par,
    "volume": round(lot,2),
    "type": mt5.ORDER_TYPE_BUY,
    "price": ask,
    "sl": text_sl,
    "tp":tp,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # enviamos la solicitud comercial
    result = mt5.order_send(request)

    print(result)

#BOTON1 BUY
buy = Button(app, text = "Buy",bg='green', command = ordencompra)
buy.grid(column=0, row=15)

#BOTON2 SELL
sell= Button(app, text = "Sell",bg='red',command = ordenventa)
sell.grid(column=1, row=15)

# Label Status
labelStatus =tk.Label(app,
                    text = "Status :")
labelStatus.grid(column=0, row=16)
labelStatus1 = tk.Label(app, text="")
labelStatus1.grid(column=1, row=16)

app.mainloop()
