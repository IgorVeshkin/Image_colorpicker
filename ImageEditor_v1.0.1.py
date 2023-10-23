import time
import tkinter as tk
from tkinter import messagebox as ms
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageGrab
import keyboard


# Создание класса приложения


class PickUpColorApp(tk.Tk):
    def __init__(self):
        # Инициализация Tkinter
        super(PickUpColorApp, self).__init__()

        # Инициализация размеров окна приложения
        self.w_width, self.w_height = 1280, 680
        self.s_width, self.s_height = self.winfo_screenwidth(), self.winfo_screenheight()

        # Задание размеров и центрирование
        self.geometry(f"{self.w_width}x{self.w_height}+"
                      f"{int((self.s_width - self.w_width) / 2)}+{int((self.s_height - self.w_height) / 2)}")

        # Задание заголовка приложения
        self.title("Image Color Picker v1.0.1 by IgorVeshkin")

        # Задание иконки для приложения
        self.iconbitmap('D:\Documents\Python_files\ImageEditor\icon_for_ImageEditor_App.ico')

        # Задание невозможности изменения размеров окна в ручную
        self.resizable(False, False)

        # Окна всегда отрисовывается поверх других
        self.attributes("-topmost", True)
        self.focus()
        self.grab_set()

        # Задание виджетов (элементов) окна приложения

        self.CanvasFrame = tk.LabelFrame(self, text="Picture")

        self.CanvasFrame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        self.PictureCanvas = tk.Canvas(self.CanvasFrame, width=self.w_width - 200, height=self.w_height - 20,
                                       bg="white")
        self.PictureCanvas.pack()

        self.CanvasDataFrame = tk.LabelFrame(self, text="Picture Data")
        self.CanvasDataFrame.pack(side=tk.RIGHT, fill="y", padx=5, pady=5, ipadx=25)

        self.LoadPic_lbl = tk.Label(self.CanvasDataFrame, text="Load Pic: ")
        self.LoadPic_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nws")

        self.LoadPic_btn = tk.Button(self.CanvasDataFrame, text="Load", width=7, command=self.LoadPicture)
        self.LoadPic_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nws")

        self.Pic_ColorRGB_lbl = tk.Label(self.CanvasDataFrame, text="RGB Color: ")
        self.Pic_ColorRGB_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="nws")

        self.Pic_ColorRGB_entry = tk.Entry(self.CanvasDataFrame, width=13)
        self.Pic_ColorRGB_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nes")

        self.Pic_ColorHEX_lbl = tk.Label(self.CanvasDataFrame, text="HEX Color: ")
        self.Pic_ColorHEX_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="nws")

        self.Pic_ColorHEX_entry = tk.Entry(self.CanvasDataFrame, width=13)
        self.Pic_ColorHEX_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nes")

        self.Mouse_x_lbl = tk.Label(self.CanvasDataFrame, text="Mouse x: ")
        self.Mouse_x_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="nws")

        self.Mouse_x_entry = tk.Entry(self.CanvasDataFrame, width=13)
        self.Mouse_x_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nes")

        self.Mouse_y_lbl = tk.Label(self.CanvasDataFrame, text="Mouse y: ")
        self.Mouse_y_lbl.grid(row=4, column=0, padx=5, pady=5, sticky="nws")

        self.Mouse_y_entry = tk.Entry(self.CanvasDataFrame, width=13)
        self.Mouse_y_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nes")

        self.Selected_Color_LabelFrame = tk.LabelFrame(self.CanvasDataFrame, text="Selected Color")

        self.Selected_Color_LabelFrame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nw")

        self.Selected_Color_Canvas = tk.Canvas(self.Selected_Color_LabelFrame, width=140, height=140,
                                               bg="white")
        self.Selected_Color_Canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nw")

        self.Info_lbl = tk.Label(self.CanvasDataFrame, text="F9-to make screenshot")
        self.Info_lbl.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.Info2_lbl = tk.Label(self.CanvasDataFrame, text="Right Mouse btn-to zoom")
        self.Info2_lbl.grid(row=8, column=0, columnspan=2, rowspan=2, padx=5, pady=5, sticky="w")

        self.offset_factor = 50

        self.image = None

        self.temp_image = None

        # Блокирование любого ввода в RBG-поле, кроме сочитания клавиш для выделения и копирования
        self.Pic_ColorRGB_entry.bind("<Key>", "break")
        self.Pic_ColorRGB_entry.bind("<Control-a>", self.allow_select_copy_from_entry)
        self.Pic_ColorRGB_entry.bind("<Control-c>", self.allow_select_copy_from_entry)

        # Блокирование любого ввода в HEX-поле, кроме сочитания клавиш для выделения и копирования
        self.Pic_ColorHEX_entry.bind("<Key>", "break")
        self.Pic_ColorHEX_entry.bind("<Control-a>", self.allow_select_copy_from_entry)
        self.Pic_ColorHEX_entry.bind("<Control-c>", self.allow_select_copy_from_entry)

        # Подключение событий для виджета Canvas
        # При нажатии по Canvas левой кнопкой мыши будет получен цвет текущего пикселя
        self.PictureCanvas.bind("<Button-1>", self.get_canvas_pixel_color)

        # При движении мыши внутри Canvas будет просчитана ее позиция
        self.PictureCanvas.bind("<Motion>", self.reflect_canvasdata)

        # При движении мыши и удерживании правой кнопки мыши внутри Canvas будет появляться zoom-окно
        self.PictureCanvas.bind("<B3-Motion>", self.popup_canvas)

        # При отпускании правой кнопки мыши zoom-окно будет скрыто
        self.PictureCanvas.bind("<ButtonRelease-3>",
                                lambda event: self.close_popup_window(event, window=self.popup_window))

        # Создание zoom-окна
        self.popup_window = tk.Toplevel(self)

        # Zoom-окно будет отображаться поверх всех остальных окон
        self.popup_window.overrideredirect(True)

        # По умолчанию zoom-окно скрыто
        self.popup_window.withdraw()

        # Bool-переменная, характеризующая отображение zoom-окно
        self.Appeared = True

        # Создание Canvas-виджета внутри zoom-окна
        self.ViewCanvas = tk.Canvas(self.popup_window, width=150, height=150, bg="white")

        # Задание позиции Canvas-виджета внутри zoom-окна
        self.ViewCanvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nws")

        # Протокол выполняющийся при закрытии окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Если нажата кнопка F9, запускается функция, создающая screenshot
        keyboard.add_hotkey('F9', self.Make_Screenshot)

        # Цикл обработчик событий Tkinter
        self.mainloop()

    def allow_select_copy_from_entry(self, event):
        pass

    # Функция, создающая screenshot

    def Make_Screenshot(self):
        # Сворачиваем текущее окно
        self.withdraw()

        # Выводит окно вопроса, хочет ли пользователь создать скриншот
        take_screenshot = ms.askyesno(title="Screenshot creation", message="The previous image will be replaced!\n"
                                                                           "Do you really want to take screenshot?")
        # Если ответ положительный
        if take_screenshot:
            # Ждем полсекунды, чтобы окно вопроса успело скрыться
            time.sleep(0.5)

            # Делаем скриншот
            screenshot = ImageGrab.grab()

            # Загружаем скриншот в Canvas внутри основного окна приложения
            self.LoadPicture(skip_file_search=True, screenshot=screenshot)

        # Обновляем окно
        self.update()

        # Разворачиваем окна, новое screenshot-изображение отображается
        self.deiconify()

    # Функция закрытия zoom-окна
    def close_popup_window(self, event, window):
        window.withdraw()
        self.Appeared = True

    # Функция отображения zoom-окна
    def popup_canvas(self, event):

        # Проверка требуется, чтобы избежать разворачивания окна
        # из свернутого вида в каждый момент времени
        if self.Appeared:
            self.popup_window.update()
            self.popup_window.deiconify()
            self.Appeared = False

        # Высчитываем координаты мыши в виде целых чисел
        int_x, int_y = event.x_root // 1, event.y_root // 1

        # Применяем координаты мыши как позицию zoom-окна
        self.popup_window.geometry(f"+{int_x + 5}+{int_y + 5}")

        # Запускаем функцию, высчитывающую зоны отображающейся в zoom-окне
        self.reflect_canvasdata(event)
        # Zoom-окно будет отрисовываться поверх всех остальных окон
        self.popup_window.attributes("-topmost", True)

    # Функция получения цвета текущего пикселя в формате HEX и RGB
    def get_canvas_pixel_color(self, event):

        # Получаем координаты мышки
        x, y = event.x, event.y

        # Если в памяти переменная с изображением не пустая, то
        if self.temp_image:

            # Получаем RGB-кортеж пикселя в текущей точке
            rbg_tuple = self.image.getpixel((x, y))

            # Очищаем HEX-Поле
            self.Pic_ColorHEX_entry.delete(0, tk.END)

            # Разделяем RBG-кортеж на 3 переменные
            char1, char2, char3 = "{:X}".format(rbg_tuple[0]), "{:X}".format(rbg_tuple[1]), "{:X}".format(rbg_tuple[2])

            # Если длина каждой переменной не превышает 1 элемента, то дописываем нуль в начале

            if len(char1) == 1:
                char1 = "0" + char1

            if len(char2) == 1:
                char2 = "0" + char2

            if len(char3) == 1:
                char3 = "0" + char3

            # Задаем HEX значение
            self.Pic_ColorHEX_entry.insert(tk.END, ('#{}{}{}').format(char1, char2, char3))

            # Задаем полученный цвет в дополнительный Canvas, предназначенный для отображения цвета
            self.Selected_Color_Canvas.config(bg='#{}{}{}'.format(char1.lower(), char2.lower(), char3.lower()))

            # Получаем RGB-значение цвета
            hex = '{:X}{:X}{:X}'.format(rbg_tuple[0], rbg_tuple[1], rbg_tuple[2])
            rgb = []

            # Каждый элемент RGB-кортежа переводиться в целое число по основанию 16
            for i in (0, 2, 4):
                try:
                    decimal = int(hex[i:i + 2], 16)

                except ValueError as error:
                    pass

                rgb.append(decimal)

            # Очищаем RGB-Поле
            self.Pic_ColorRGB_entry.delete(0, tk.END)

            # Задаем полученные значения в RGB-Поле
            self.Pic_ColorRGB_entry.insert(tk.END, "{}, {}, {}".format(rgb[0], rgb[1], rgb[2]))

    def reflect_canvasdata(self, event):
        x, y = event.x, event.y

        self.Mouse_x_entry.delete(0, tk.END)
        self.Mouse_y_entry.delete(0, tk.END)

        self.Mouse_x_entry.insert(tk.END, f"{x}")
        self.Mouse_y_entry.insert(tk.END, f"{y}")

        if x + 5 <= self.w_width - 200 and x - 5 >= 0 and y + 5 <= self.w_height - 25 and y - 5 >= 0:
            if self.image:
                size = 10
                self.temp_image = self.image
                self.temp_image = self.temp_image.crop((x - size, y - size, x + size, y + size))
                self.temp_image = self.temp_image.resize((150, 150), Image.Resampling.HAMMING)
                self.ViewCanvas.image = ImageTk.PhotoImage(self.temp_image)
                self.ViewCanvas.create_image(0, 0, image=self.ViewCanvas.image, anchor="nw")
                self.ViewCanvas.create_rectangle((73, 73, 78, 78), fill='red')

    # Функция закрузки изображения в Canvas
    def LoadPicture(self, skip_file_search=False, screenshot=None):
        try:
            pic_width_changed, pic_height_changed = False, False

            # Если пользовать указал в параметре, что нужно выполнить поиск изображения, то
            if not skip_file_search:

                # Открывается контексное окно с выбором изображение с расширением JPG или PNG
                # Внутри переменной сохраняется путь до изображения
                image_path = askopenfilename(title='Images',
                                             filetypes=(("PNG file", "*.png"), ("JPG file", "*.jpg")))

                # Загружаем переменную в виде байт-кода в переменную
                self.image = Image.open(image_path)

                # Считываем ширину и высоту изображения
                image_w, image_h = self.image.size

                # Выводим получившиеся параметры в консоль
                print(self.image.size)

            # Если же конкестное окно поиска изображений не требуется, то
            else:
                # В переменную изображения загружаем скриншот, переданный в виде параметра
                self.image = screenshot

                # Считываем ширину и высоту изображения
                image_w, image_h = self.image.size

                # Выводим получившиеся параметры в консоль
                print(self.image.size)

            # Если размер изображения больше размера Canvas по горизонтали, то
            if image_w > self.w_width - 200:

                # Маштабируем изображение по горизонтали
                self.image = self.image.resize((self.w_width - 200, self.image.size[1]), Image.Resampling.BILINEAR)

            # Если размер изображения меньше размера Canvas по горизонтали, то
            elif image_w <= self.w_width - 200:

                # Помечаем, что нужно изменить размер изображения по горизонтали
                pic_width_changed = True

            # Если размер изображения больше размера Canvas по вертикали
            if image_h > self.w_height - 20:
                # Маштабируем изображение по вертикали
                self.image = self.image.resize((self.image.size[0], self.w_height - 20), Image.Resampling.BILINEAR)

            # Если размер изображения меньше размера Canvas по вертикали, то
            elif image_h <= self.w_height - 20:

                # Помечаем, что нужно изменить размер изображения по вертикали
                pic_height_changed = True

            # Если изображению требуется изменение размера, то
            if pic_width_changed or pic_height_changed or (pic_width_changed and pic_height_changed):

                # Создаем переменную, внутри которой создается изображение белого цвета размером с Canvas
                self.image_bg_pic = Image.new('RGBA', (self.w_width - 200, self.w_height - 20), color='white')

                # В центр белого изображения помещается изображение, которое было мешьше Canvas
                self.image_bg_pic.paste(self.image, (int((self.w_width - 200) / 2 - self.image.size[0] / 2),
                                                     int((self.w_height - 20) / 2 - self.image.size[1] / 2)))

                # В перенную изображения, помещается изображение с белым фоном
                self.image = self.image_bg_pic

            # Помещаем изображение в Canvas
            self.PictureCanvas.image = ImageTk.PhotoImage(self.image)

            # Если изображение меньше, то
            if image_w < self.w_width - 200 and image_h < self.w_height - 20:

                # Применяем изображение в центре Canvas
                self.PictureCanvas.create_image((self.w_width - 200) / 2, (self.w_height - 20) / 2,
                                                image=self.PictureCanvas.image, anchor=tk.CENTER)

                # Выходим из функции
                return

            # В случае если изображение не меньше Canvas, применяем изображение к Canvas
            self.PictureCanvas.create_image(0, 0, image=self.PictureCanvas.image, anchor="nw")

        except AttributeError as e:
            pass

    # При закрытии окна приложения
    def on_close(self):
        # Уничтожаем окно
        self.destroy()

# Создаем экземпляр класса приложения


if __name__ == "__main__":
    App = PickUpColorApp()
