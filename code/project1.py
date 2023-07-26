
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import requests
import datetime as dt


class CurrencyConverter:

    def __init__(self, url):
        self.url = 'https://api.exchangerate.host/latest'
        self.response = requests.get(url)
        self.data = self.response.json()
        self.rates = self.data.get('rates')

    def convert(self, amount, base_currency, des_currency):
        if base_currency != 'EUR':
            amount = amount/self.rates[base_currency]

       
        amount = round(amount*self.rates[des_currency], 2)

        amount = '{:,}'.format(amount)
        return amount


class Main(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.geometry('400x400')
        self.config(bg='green')
        self.CurrencyConverter = converter


        self.title_label = Label(self, text='Currency Converter', bg='green', fg='white', font=('franklin gothic medium', 20), relief='sunken')
        self.title_label.place(x=200, y=35, anchor='center')


        self.date_label = Label(self, text=f'{dt.datetime.now():%A, %B %d, %Y}', bg='green', fg='white', font=('calibri', 10))
        self.date_label.place(x=400, y=400, anchor='se')


        self.version_label = Label(self, text='v1.0', bg='green', fg='white', font=('calibri', 10))
        self.version_label.place(x=0, y=400, anchor='sw')

        
        self.amount_label = Label(self, text='Input Amount: ', bg='green', fg='white', font=('franklin gothic book', 15))
        self.amount_label.place(x=200, y=80, anchor='center')

        
        self.amount_entry = Entry(self)
        self.amount_entry.config(width=25)
        self.amount_entry.place(x=200, y=110, anchor='center')

        
        self.base_currency_label = Label(self, text='From: ', bg='green', fg='white', font=('franklin gothic book', 15))
        self.base_currency_label.place(x=200, y=140, anchor='center')

       
        self.destination_currency_label = Label(self, text='To: ', bg='green', fg='white', font=('franklin gothic book', 15))
        self.destination_currency_label.place(x=200, y=200, anchor='center')

       
        self.currency_variable1 = StringVar(self)
        self.currency_variable2 = StringVar(self)
        self.currency_variable1.set('USD')
        self.currency_variable2.set('IDR')

        self.currency_combobox1 = ttk.Combobox(self, width=20, textvariable=self.currency_variable1, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox1.place(x=200, y=170, anchor='center')

        self.currency_combobox2 = ttk.Combobox(self, width=20, textvariable=self.currency_variable2, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox2.place(x=200, y=230, anchor='center')

        
        self.convert_button = Button(self, text='Convert', bg='#52595D', fg='white', command=self.processed)
        self.convert_button.place(x=170, y=270, anchor='center')

        
        self.clear_button = Button(self, text='Clear', bg='red', fg='white', command=self.clear)
        self.clear_button.place(x=230, y=270, anchor='center')

       
        self.final_result = Label(self, text='', bg='green', fg='white', font=('calibri', 12), relief='sunken', width=40)
        self.final_result.place(x=200, y=310, anchor='center')

   
    def clear(self):
        clear_entry = self.amount_entry.delete(0, END)
        clear_result = self.final_result.config(text='')
        return clear_entry, clear_result

    
    def processed(self):
        try:
            given_amount = float(self.amount_entry.get())
            given_base_currency = self.currency_variable1.get()
            given_des_currency = self.currency_variable2.get()
            converted_amount = self.CurrencyConverter.convert(given_amount, given_base_currency, given_des_currency)
           
            given_amount = '{:,}'.format(given_amount)

            self.final_result.config(text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}')

       
        except ValueError:
            convert_error = messagebox.showwarning('WARNING!', 'Please Fill the Amount Field (integer only)!')
            return convert_error


if __name__ == '__main__':
    converter = CurrencyConverter('https://api.exchangerate.host/latest')
    Main(converter)
    mainloop()

