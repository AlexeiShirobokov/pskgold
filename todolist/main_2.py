import openpyxl

########
import sys
import os
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

import warnings


pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 100)
pd.set_option("display.precision", 100)

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
current_dir=os.path.dirname(os.path.abspath("__file__"))
df = pd.read_excel(os.path.join(current_dir, 'Регламент_инструкции.xlsx'), "Регламент")
df1 = pd.read_excel(os.path.join(current_dir, 'Регламент_инструкции.xlsx'), "Артикулы")
df2 = pd.read_excel(os.path.join(current_dir, 'Регламент_инструкции.xlsx'), "Тип обслуживания")
df3 = pd.read_excel(os.path.join(current_dir, 'Календарный План ТО_2023.xlsx'), "Календарь ТО")
# группировка датафрейма и получение уникальных значений Кат. № Аналог.
grouped = df1.groupby(['Кат. №', 'Кат. № Аналог'])['Кат. № Аналог'].unique()


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)  # загрузка файла формы
        self.service_button = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.service_button.clicked.connect(self.open_service_window)

        self.service_button2 = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.service_button2.clicked.connect(self.open_service_window_2)

    def open_service_window(self):
        self.service_window = MyWindows()
        self.service_window.show()

    def open_service_window_2(self):
        self.service_window2=MyWindows_2()
        self.service_window2.show()


class MyWindows_2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # добавляем виджеты на форму
        self.tipteh_label = QtWidgets.QLabel('Тип техники:')
        self.tipteh_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.tipteh_edit.addItems(list(df['Тип техники'].unique()))
        self.mark_label = QtWidgets.QLabel('Марка техники:')
        self.mark_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.mark_edit.addItems(list(df['Марка техники'].unique()))

        self.god_label = QtWidgets.QLabel('Год:')
        self.god_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.god_edit.addItems(map(str, [2022, 2023]))

        self.mouth_label = QtWidgets.QLabel('Месяц:')
        self.mouth_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.mouth_edit.addItems(["Январь", "Февраль", "Март", "Апрель","Май","Июнь","Июль", "Август","Сентябрь","Октябрь","Ноябрь","Декабрь"])

        #self.inventory_label = QtWidgets.QLabel('Инвентарный номер:')
        #self.inventory_edit = QtWidgets.QLineEdit()

        self.to_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.submit_button = QtWidgets.QPushButton('Получить список')
        self.submit_button.clicked.connect(self.get_list)

        # размещаем виджеты на форме
        form_layout = QtWidgets.QFormLayout()

        form_layout.addRow(self.tipteh_label, self.tipteh_edit)
        form_layout.addRow(self.mark_label, self.mark_edit)
        form_layout.addRow(self.god_label, self.god_edit)
        form_layout.addRow(self.mouth_label, self.mouth_edit)
        form_layout.addWidget(self.submit_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        # создаем атрибут result_table как экземпляр класса QtWidgets.QTableWidget()
        self.result_table = QtWidgets.QTableWidget()
        main_layout.addWidget(self.result_table)  # добавляем виджет в main_layout

        self.setLayout(main_layout)
        self.result_table.setColumnCount(10)
        self.result_table.setHorizontalHeaderLabels(
            ['Год проведения ТО', 'Тип техники', 'Марка техники', 'Инвентарный номер', 'План_Наработка, м/ч', 'Период ТО, м/ч', 'Факт_Наработка, м/ч',
             'Фактическая дата проведения ТО', 'Плановая дата проведения ТО', 'Месяц'])
    # задаем действие
    def get_list(self):
        # Получаем выбранные значения из ComboBox
        tipteh = self.tipteh_edit.currentText()
        mark = self.mark_edit.currentText()
        god = int(self.god_edit.currentText())
        mounth = self.mouth_edit.currentText()

        # = int(self.inventory_edit.text())
        # Применяем фильтры к DataFrame df3
        filtered_df = df3.loc[(df3['Год проведения ТО'] == god)&(df3['Месяц'] == mounth)]
        # Отображаем результаты в таблице
        self.result_table.setRowCount(len(filtered_df))
        for i, row in enumerate(filtered_df.values):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.result_table.setItem(i, j, item)
        self.result_table.update()
        print(filtered_df)
class MyWindows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # добавляем виджеты на форму
        self.date_label = QtWidgets.QLabel('Дата:')
        self.date_edit = QtWidgets.QLineEdit()
        self.department_label = QtWidgets.QLabel('Подразделение:')
        self.department_edit = QtWidgets.QLineEdit()

        self.tipteh_label = QtWidgets.QLabel('Тип техники:')
        self.tipteh_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.tipteh_edit.addItems(list(df['Тип техники'].unique()))
        self.mark_label = QtWidgets.QLabel('Марка техники:')
        self.mark_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.mark_edit.addItems(list(df['Марка техники'].unique()))

        self.inventory_label = QtWidgets.QLabel('Инвентарный номер:')
        self.inventory_edit = QtWidgets.QLineEdit()
        self.hours_label = QtWidgets.QLabel('Машиночасы:')
        self.hours_edit = QtWidgets.QLineEdit()
        self.to_label = QtWidgets.QLabel('Номер ТО:')

        self.to_edit = QtWidgets.QComboBox()
        # получаем уникальные значения из столбца "Марка техники" в DataFrame и добавляем их в выпадающий список
        self.to_edit.addItems(list(df['Вид ТО'].unique()))

        self.responsible_label = QtWidgets.QLabel('ФИО ответственного:')
        self.responsible_edit = QtWidgets.QLineEdit()

        self.submit_button = QtWidgets.QPushButton('Получить список')

        # добавляем таблицу для вывода результатов
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels(['Выполненые работы', 'Группа деталей', 'Детали', 'Кат. №', 'Кат. № Аналог', 'Ед. изм.', 'Количество план', 'Количество факт'])

        # размещаем виджеты на форме
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.date_label, self.date_edit)
        form_layout.addRow(self.department_label, self.department_edit)
        form_layout.addRow(self.tipteh_label, self.tipteh_edit)
        form_layout.addRow(self.mark_label, self.mark_edit)
        form_layout.addRow(self.inventory_label, self.inventory_edit)
        form_layout.addRow(self.hours_label, self.hours_edit)
        form_layout.addRow(self.to_label, self.to_edit)
        form_layout.addRow(self.responsible_label, self.responsible_edit)
        form_layout.addWidget(self.submit_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.result_table)

        self.setLayout(main_layout)

        # связываем сигнал нажатия кнопки с методом on_submit_clicked
        self.submit_button.clicked.connect(self.on_submit_clicked)

        self.save_button = QtWidgets.QPushButton('Сохранить')
        form_layout.addRow(self.save_button)
        self.save_button.clicked.connect(self.save_to_dataframe)

        self.add_row_button = QtWidgets.QPushButton('Добавить строку')
        form_layout.addWidget(self.add_row_button)
        self.add_row_button.clicked.connect(self.on_add_row_clicked)
    def on_add_row_clicked(self):
        # получаем количество строк в таблице
        row_count = self.result_table.rowCount()

        # добавляем новую строку
        self.result_table.insertRow(row_count)

        # заполняем новую строку данными
        for col in range(self.result_table.columnCount()):
            item = QtWidgets.QTableWidgetItem('')
            self.result_table.setItem(row_count, col, item)

            if col == 8:
                edit = QtWidgets.QLineEdit()
                self.result_table.setCellWidget(row_count, col, edit)
    def on_submit_clicked(self):
        mark = self.mark_edit.currentText()
        to_number = self.to_edit.currentText()

        # поиск данных в датафрейме
        data = df[(df['Марка техники'] == mark) & (df['Вид ТО'] == to_number)]

        if not data.empty:
            # задаем данные для таблицы
            vipols = data['Выполненые работы'].tolist()
            groups = data['Группа деталей'].tolist()
            works = data['Наименование'].tolist()
            articls = data['Кат. №'].tolist()

            # находим соответствующие элементы в df2 и создаем список аналогов для каждого элемента в столбце "Кат. №"
            analog_articls = []
            for art in articls:
                analogs = df1.loc[df1['Кат. №'] == art, 'Кат. № Аналог'].tolist()
                combo = QtWidgets.QComboBox()
                combo.addItems([str(analog) for analog in analogs])
                analog_articls.append(combo)

            eds = data['Ед. изм.'].tolist()
            amounts = data['Кол-во'].tolist()

            # Создаем словарь со списками аналогов для каждого уникального значения в столбце 'Кат. №'
            analog_dict = df1.groupby('Кат. №')['Кат. № Аналог'].agg(list).to_dict()

            self.result_table.setRowCount(len(works))

            for i, (vipol, group, work, articl, analog_articl, ed, amount) in enumerate(zip(vipols, groups, works, articls, analog_articls, eds, amounts)):
                self.result_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(vipol)))
                self.result_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(group)))
                self.result_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(work)))
                self.result_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(articl)))
                self.result_table.setCellWidget(i, 4, analog_articl)
                self.result_table.setItem(i, 5, QtWidgets.QTableWidgetItem(str(ed)))
                self.result_table.setItem(i, 6, QtWidgets.QTableWidgetItem(str(amount)))
                edit = QtWidgets.QLineEdit()
                self.result_table.setCellWidget(i, 7, edit)
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', f'Неверный номер ТО для выбранной марки техники "{mark}"')

    def save_to_dataframe(self):
        # Получение данных из таблицы
        df_TO = pd.read_excel(os.path.join(current_dir, 'Результаты ТО.xlsx'), "Sheet1")
        rows = self.result_table.rowCount()
        cols = self.result_table.columnCount()

        # Создание пустого dataframe
        df = pd.DataFrame(columns=['Дата', 'Тип техники', 'Марка техники', 'Машиночасы', 'Номер ТО', 'Инвентарный номер', 'Подразделение', 'ФИО ответственного', 'Выполненые работы', 'Группа деталей', 'Детали', 'Кат. №', 'Кат. № Аналог', 'Ед. изм.', 'Количество план', 'Количество факт'])

        # Получение вводных данных
        date = self.date_edit.text()
        tipteh = self.tipteh_edit.currentText()
        mark = self.mark_edit.currentText()
        hours = self.hours_edit.text()
        to_number = self.to_edit.currentText()
        department = self.department_edit.text()
        responsible = self.responsible_edit.text()
        inventory_number = self.inventory_edit.text()

        # Получение данных о проделанных работах
        #data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.result_table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    # Если это столбец "Количество факт", то добавляем значение из поля ввода
                    if col == 7:
                        edit = self.result_table.cellWidget(row, col)
                        if isinstance(edit, QtWidgets.QLineEdit):
                            row_data.append(edit.text())
                        else:
                            row_data.append('')
                    elif col == 4:
                        combo_box = self.result_table.cellWidget(row, col)
                        selected_item = combo_box.currentText()

                        #entText()
                        row_data.append(selected_item)
                    else:
                        row_data.append('')


            #data.append(row_data)
            # Вставка заголовка таблицы

            row_data = [date, tipteh, mark, hours, to_number,  inventory_number, department,  responsible] + row_data[0:7] + row_data[8:10] + row_data[7:8]

            df.loc[row] = row_data

        # Вывод dataframe в консоль
        #print(df_TO)
#%%
        dfmer = pd.concat([df_TO, df], axis=0)
        dfmer.to_excel(os.path.join(current_dir, 'Результаты ТО.xlsx'), index=False)
        # выводим сообщение об успешном сохранении
        QtWidgets.QMessageBox.information(self, 'Успешно', 'Сохранено!')
#%%



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
