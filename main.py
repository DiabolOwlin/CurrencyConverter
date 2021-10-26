import tkinter as tk

from tkinter.messagebox import showerror
from tkinter import ttk

import urllib.request
import xml.dom.minidom as minidom


class GetData:

    @classmethod
    def get_data(cls):
        web_file = urllib.request.urlopen("https://www.nbp.pl/kursy/xml/lasta.xml")
        return web_file.read()


class GetCurrenciesDictionary:
    curr_dict = {}

    def __init__(self):
        pass

    def get_currencies_dictionary(self):

        dom = minidom.parseString(GetData.get_data())
        dom.normalize()

        elements = dom.getElementsByTagName("pozycja")

        for node in elements:
            for child in node.childNodes:
                if child.nodeType == 1:
                    if child.tagName == "kurs_sredni":
                        if child.firstChild.nodeType == 3:
                            sredni_kurs = float(child.firstChild.data.replace(',', '.'))
                    if child.tagName == "kod_waluty":
                        if child.firstChild.nodeType == 3:
                            kod_wal = child.firstChild.data
            self.curr_dict[kod_wal] = sredni_kurs


# def print_dict(in_dict):
#     print("Nasze kursy srednie:\n")
#     for key in in_dict.keys():
#         print(key, in_dict[key])

class CurrencyConverter:
    @classmethod
    def curr_to_curr(cls, a, curr_out):
        return a * curr_out


class CurrencyError(Exception):
    pass


class ConverterFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}

        # temperature label
        self.enter_quantity_label = ttk.Label(self, width=25, text='Currency Exchange')
        self.enter_quantity_label.grid(column=0, row=0, columnspan=4, sticky=tk.N, **options)

        # temperature entry
        self.in_quantity = tk.StringVar()
        self.in_quantity = ttk.Entry(self, textvariable=self.in_quantity)
        self.in_quantity.grid(column=0, row=1, **options)
        self.in_quantity.focus()

        self.currency_in = ttk.Combobox(self, width=5)
        self.currency_in['values'] = (
            'PLN', 'THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP',
            'UAH', 'JPY', 'CZK', 'DKK', 'ISK', 'NOK', 'SEK', 'HRK', 'RON', 'BGN', 'TRY', 'ILS',
            'CLP', 'PHP', 'MXN', 'ZAR', 'BRL', 'MYR', 'RUB', 'IDR', 'INR', 'KRW', 'CNY', 'XDR')

        self.currency_in.grid(column=1, row=1, sticky=tk.W, **options)

        self.currency_out = ttk.Combobox(self, width=5)
        self.currency_out['values'] = (
            'PLN', 'THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP',
            'UAH', 'JPY', 'CZK', 'DKK', 'ISK', 'NOK', 'SEK', 'HRK', 'RON', 'BGN', 'TRY', 'ILS',
            'CLP', 'PHP', 'MXN', 'ZAR', 'BRL', 'MYR', 'RUB', 'IDR', 'INR', 'KRW', 'CNY', 'XDR')

        self.currency_out.grid(column=2, row=1, sticky=tk.W, **options)

        self.convert_button = ttk.Button(self, text='Convert', command=self.convert)
        self.convert_button.grid(column=3, row=1, sticky=tk.W, **options)

        # result label
        self.result_label = ttk.Label(self)
        self.result_label.grid(row=2, columnspan=3, **options)

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def convert(self):
        """  Handle button click event
        """
        quantity = self.in_quantity.get()
        curr_in = self.currency_in.get()
        # print(type(curr_in))
        curr_out = self.currency_out.get()
        # print(type(curr_out))
        try:
            if quantity.isdigit():
                pass
            else:
                raise ValueError()
            if not curr_in or not curr_out:
                raise CurrencyError()
        except ValueError:
            showerror(title="Error!", message="Need to enter a digit!")
        except CurrencyError:
            showerror(title="Error", message="You need to choose currency!")
        else:
            quantity = float(quantity)
            if curr_in == curr_out:
                result = quantity
            elif curr_in == 'PLN':
                result_curr = 1.0 / GetCurrenciesDictionary.curr_dict[curr_out]
                result = CurrencyConverter.curr_to_curr(quantity, result_curr)
            elif curr_out == 'PLN':
                result_curr = GetCurrenciesDictionary.curr_dict[curr_in]
                result = CurrencyConverter.curr_to_curr(quantity, result_curr)
            else:
                result_curr = GetCurrenciesDictionary.curr_dict[curr_in] / GetCurrenciesDictionary.curr_dict[curr_out]
                result = CurrencyConverter.curr_to_curr(quantity, result_curr)

            result_text = f'{quantity:.4f} {curr_in} = {result:.4f} {curr_out}'
            self.result_label.config(text=result_text)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Currency Converter')
        self.geometry('365x100')
        self.resizable(False, False)


if __name__ == "__main__":
    GetCurrenciesDictionary().get_currencies_dictionary()
    # print_dict(GetCurrenciesDictionary.curr_dict)
    app = App()
    ConverterFrame(app)
    app.mainloop()
