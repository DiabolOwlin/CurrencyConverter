import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import urllib.request
import xml.dom.minidom as minidom


def get_data(xml_url):
    web_file = urllib.request.urlopen(xml_url)
    return web_file.read()


def get_currencies_dictionary(xml_content):
    dom = minidom.parseString(xml_content)
    dom.normalize()

    elements = dom.getElementsByTagName("pozycja")
    curr_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == "kurs_sredni":
                    if child.firstChild.nodeType == 3:
                        kurs_sredni = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == "kod_waluty":
                    if child.firstChild.nodeType == 3:
                        kod_waluty = child.firstChild.data
        curr_dict[kod_waluty] = kurs_sredni
    return curr_dict


def print_dict(in_dict):
    for key in in_dict.keys():
        print(key, in_dict[key])


class ConverterFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}

        # label
        self.label = ttk.Label(self, text='Currency exchange')
        self.label.grid(column=0, row=0, sticky=tk.W, **options)

        # entry
        self.enter_quantity = tk.StringVar()
        self.enter_quantity_entry = ttk.Entry(self, textvariable=self.enter_quantity)
        self.enter_quantity_entry.grid(column=1, row=0, **options)
        self.enter_quantity_entry.focus()

        # button
        self.button = ttk.Button(self, text='Exchange')
        self.button['command'] = self.button_clicked
        self.button.grid(column=2, row=0, sticky=tk.W, **options)

        # result label
        self.result_label = ttk.Label(self)
        self.result_label.grid(row=1, columnspan=3, **options)

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    @staticmethod
    def button_clicked():
        showinfo(title='Information',
                 message='Hello, Tkinter!')


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('National Bank of Poland')
        self.geometry('375x75')
        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    ConverterFrame(app)
    app.mainloop()
    url = "https://www.nbp.pl/kursy/xml/lasta.xml"
    currency_dict = get_currencies_dictionary(get_data(url))
    # print_dict(currency_dict)
