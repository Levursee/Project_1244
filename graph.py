import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class GraphFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, padx=5)
        self.fig = None
        self.axes = None
        self.toolbar = None
        self.canvas = None
        self.linewidth = 1
        self.style_list = ['solid', '-', '--', 'dashed', '-.', 'dashdot', ':', 'dotted']
        self.style = '-'
        self.x_axis = 'x'
        self.y_axis = 'y'
        self.title = None
        self.ngraphs = 0
        self._start()

    def _start(self):
        """
        Приватный метод который задает конфигурации графика
        """
        self.fig = Figure(figsize=(4.5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(padx=(1, 1), pady=(2, 2))
        _Toolbar = tk.Frame(self)
        _Toolbar.pack(side=tk.TOP, fill=tk.BOTH)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.X)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

        plt.subplots_adjust(top = 1, bottom=0.1, hspace=0.8, wspace=1)
        if self.title is not None:
            self.axes.set_title(self.title)

        self.axes.set_xlabel(self.x_axis)
        self.axes.set_ylabel(self.y_axis)
        self.fig.tight_layout(pad = 2.5)


    def set_axis(self,xl, yl):
        '''
        Подпись осей
        :param xl: название оси х
        :param yl: название оси у
        '''
        self.x_axis = xl
        self.y_axis = yl
        self.axes.set_xlabel(self.x_axis)
        self.axes.set_ylabel(self.y_axis)
    def draw_graph(self, files):
        """
        Метод который рисует графикии
        """
        self.canvas.get_tk_widget().pack_forget()
        self.toolbar.pack_forget()
        self._start()

        for i in range(files.shape[0]):
            self.axes.plot(files[i], linewidth=self.linewidth, linestyle=self.style)
            self.canvas.draw()

    def set_title(self, value):
        self.title = value
        self.axes.set_title(self.title)

class NavigationToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, window):
        super().__init__(canvas, window, pack_toolbar=False)

    # override _Button() to re-pack the toolbar button in vertical direction
    def _Button(self, text, image_file, toggle, command):
        b = super()._Button(text, image_file, toggle, command)
        b.pack(side=tk.TOP)  # re-pack button in vertical direction
        return b

    # override _Spacer() to create vertical separator
    def _Spacer(self):
        s = tk.Frame(self, width=26, relief=tk.RIDGE, bg="DarkGray", padx=2)
        s.pack(side=tk.TOP, pady=5)  # pack in vertical direction
        return s

    # disable showing mouse position in toolbar
    def set_message(self, s):
        pass


    toolitems = (
        ('Home', 'Вернутся в начальный вид', 'home', 'home'),
        ('Back', 'Обратно в предыдущий вид', 'back', 'back'),
        ('Forward', 'Вперед к следующему виду', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan',
         'Левый клик для движения, Правый клик для увеличения\n'
         'x/y фиксирует оси, CTRL фиксирует стороны',
         'move', 'pan'),
        ('Save', 'Сохранить', 'filesave', 'save_figure'),
        (None, None, None, None))
