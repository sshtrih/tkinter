import tkinter as tk
import tkinter.messagebox as mb

from tkinter import ttk
from PIL import ImageTk, Image


def convert_to_int(price):
    try:
        return int(price)
    except ValueError:
        return None


class MainWindow(tk.Toplevel):

    def __init__(self, user):
        super().__init__()

        self.user = user

        # конфигурация окна
        self.resizable(width=False, height=False)
        self.title('Hardware store')

        # конфигурация фреймов

        self.frame_find_product = tk.Frame(self, bg='#DFDAC5')
        self.frame_statistic = tk.Frame(self, bg='#FCECAD')
        self.frame_products = tk.Frame(self, bg='#D8D7C4')

        self.frame_find_product.grid(row=0, column=0, sticky='ns')
        self.frame_statistic.grid(row=0, column=1)
        self.frame_products.grid(row=1, column=0, columnspan=2, sticky='we')

        # Фрейм статистики

        self.l_top_sales = tk.Label(self.frame_statistic, text="The best products of the past months")
        self.l_top_sales_value = tk.Label(self.frame_statistic, text=user.get_top_sales(), font='Helvetica 14 bold')
        self.l_top_category = tk.Label(self.frame_statistic, text="The best categories of the past months")
        self.l_top_category_value = tk.Label(self.frame_statistic, text=user.get_top_categories(),
                                             font='Helvetica 14 bold')

        basket_img = ImageTk.PhotoImage(Image.open(r"C:\Users\danii\PycharmProjects\tkinter\res\basket.png"))
        self.basket = tk.Label(self.frame_statistic, image=basket_img)
        self.basket.image = basket_img

        self.basket.grid(row=0, column=2, sticky='e', padx=30, pady=10)
        self.l_top_sales.grid(row=1, column=0, sticky='w', padx=20, pady=20)
        self.l_top_sales_value.grid(row=1, column=1, sticky='e', padx=20, pady=20)
        self.l_top_category.grid(row=2, column=0, sticky='w', padx=20, pady=20)
        self.l_top_category_value.grid(row=2, column=1, sticky='e', padx=20, pady=20)

        self.basket.bind('<Button-1>', self.prep)
        # фрейм со списком продуктов

        self.lst = [[value for key, value in d.items()] for d in user.get_products()]
        self.heads = ['Model', 'Price', 'Manufacturer', 'Amount', 'Category']
        self.table = ttk.Treeview(self.frame_products, show='headings')
        self.table['columns'] = self.heads
        self.table['displaycolumns'] = ['Model', 'Manufacturer', 'Category', 'Price', 'Amount']

        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        for row in self.lst:
            self.table.insert('', tk.END, values=row)

        scroll_pane = ttk.Scrollbar(self.frame_products, command=self.table.yview)
        scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=scroll_pane.set)

        self.table.pack(expand=tk.YES, fill=tk.BOTH)

        self.table.bind("<<TreeviewSelect>>", self.item_selected)
        # Фрейм поиска продуктов

        self.l_key_word = ttk.Label(self.frame_find_product, text='Product name')
        self.l_key_word_value = ttk.Entry(self.frame_find_product)

        self.l_start_prise = ttk.Label(self.frame_find_product, text='From ')
        self.l_start_prise_value = ttk.Entry(self.frame_find_product, justify=tk.RIGHT)

        self.l_end_prise = ttk.Label(self.frame_find_product, text='To')
        self.l_end_prise_value = ttk.Entry(self.frame_find_product, justify=tk.RIGHT)

        self.l_manufacturer = ttk.Label(self.frame_find_product, text='Manufacturer')
        self.l_manufacturer_value = ttk.Entry(self.frame_find_product)

        self.l_category = ttk.Label(self.frame_find_product, text='Category')
        self.l_category_value = ttk.Combobox(self.frame_find_product,
                                             values=list(map(lambda x: x['name'], user.get_categories())))

        self.btm_find = ttk.Button(self.frame_find_product, text='Search', command=self.find_product)

        self.l_key_word.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.l_key_word_value.grid(row=0, column=1, sticky='e', padx=10, pady=10)
        self.l_start_prise.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.l_start_prise_value.grid(row=1, column=1, sticky='e', padx=10, pady=10)
        self.l_end_prise.grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.l_end_prise_value.grid(row=2, column=1, sticky='e', padx=10, pady=10)
        self.l_manufacturer.grid(row=3, column=0, sticky='w', padx=10, pady=10)
        self.l_manufacturer_value.grid(row=3, column=1, sticky='e', padx=10, pady=10)
        self.l_category.grid(row=4, column=0, sticky='w', padx=10, pady=10)
        self.l_category_value.grid(row=4, column=1, sticky='e', padx=10, pady=10)
        self.btm_find.grid(row=5, column=0, columnspan=2, sticky='n', padx=10, pady=10)

    def find_product(self):
        products = [[value for key, value in d.items()] for d in self.user.find_product(
            convert_to_int(self.l_start_prise_value.get()),
            convert_to_int(self.l_end_prise_value.get()),
            self.l_category_value.get(),
            self.l_key_word_value.get(),
            self.l_manufacturer_value.get())]

        self.table.delete(*self.table.get_children())

        for i in products:
            self.table.insert('', tk.END, values=i)

    def prep(self, event):
        print('Кнопка нажата')

    def item_selected(self, event):
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            product = item["values"]
            if mb.askyesno('?', f'Добавить товар {product[0]} в корзину?'):
                self.user.add_product_to_basket(product)


