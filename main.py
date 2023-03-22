import openpyxl

########
import os
import pandas as pd
from PyQt5 import QtWidgets
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

# загрузка данных из файла в датафрейм
#df = pd.read_excel('data.xlsx', sheet_name='ТО')

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # добавляем виджеты на форму
        self.date_label = QtWidgets.QLabel('Дата:')
        self.date_edit = QtWidgets.QLineEdit()
        self.hours_label = QtWidgets.QLabel('Машиночасы:')
        self.hours_edit = QtWidgets.QLineEdit()
        self.mark_label = QtWidgets.QLabel('Марка техники:')
        self.mark_edit = QtWidgets.QLineEdit()
        self.inventory_label = QtWidgets.QLabel('Инвентарный номер:')
        self.inventory_edit = QtWidgets.QLineEdit()
        self.to_label = QtWidgets.QLabel('Номер ТО:')
        self.to_edit = QtWidgets.QLineEdit()
        self.submit_button = QtWidgets.QPushButton('Отправить')

        # добавляем таблицу для вывода результатов
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['Работы', 'Количество план', 'Количество факт'])

        # размещаем виджеты на форме
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.date_label, self.date_edit)
        form_layout.addRow(self.hours_label, self.hours_edit)
        form_layout.addRow(self.mark_label, self.mark_edit)
        form_layout.addRow(self.inventory_label, self.inventory_edit)
        form_layout.addRow(self.to_label, self.to_edit)
        form_layout.addWidget(self.submit_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.result_table)

        self.setLayout(main_layout)

        # связываем сигнал нажатия кнопки с методом on_submit_clicked
        self.submit_button.clicked.connect(self.on_submit_clicked)

        self.save_button = QtWidgets.QPushButton('Сохранить в Excel')
        form_layout.addRow(self.save_button)
        self.save_button.clicked.connect(self.save_to_excel)

    def on_submit_clicked(self):
        mark = self.mark_edit.text()
        to_number = self.to_edit.text()

        # поиск данных в датафрейме
        data = df[(df['Марка техники'] == mark) & (df['Вид ТО'] == to_number)]

        if not data.empty:
            # задаем данные для таблицы
            works = data['Наименование'].tolist()
            amounts = data['Кол-во'].tolist()

            self.result_table.setRowCount(len(works))

            for i, (work, amount) in enumerate(zip(works, amounts)):
                self.result_table.setItem(i, 0, QtWidgets.QTableWidgetItem(work))
                self.result_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(amount)))

                edit = QtWidgets.QLineEdit()
                self.result_table.setCellWidget(i, 2, edit)
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', f'Неверный номер ТО для выбранной марки техники "{mark}"')

    def save_to_excel(self):
        # Получение данных из таблицы
        rows = self.result_table.rowCount()
        cols = self.result_table.columnCount()

        # Получение вводных данных
        date = self.date_edit.text()
        mark = self.mark_edit.text()
        hours = self.hours_edit.text()
        to_number = self.to_edit.text()
        inventory_number = self.inventory_edit.text()

        # Получение данных о проделанных работах
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.result_table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    # Если это столбец "Количество факт", то добавляем значение из поля ввода
                    if col == 2:
                        edit = self.result_table.cellWidget(row, col)
                        if isinstance(edit, QtWidgets.QLineEdit):
                            row_data.append(edit.text())
                        else:
                            row_data.append('')
                    else:
                        row_data.append('')
            data.append(row_data)

            # Сохранение данных в Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Результаты ТО"

        # Вставка заголовка таблицы
        header = ['Дата', 'Марка техники', 'Машиночасы', 'Номер ТО', 'Инвентарный номер', 'Работы', 'Количество план',
                  'Количество факт']
        ws.append(header)

        # Вставка вводных данных
        input_data = [date, mark, hours, to_number, inventory_number]
        for i in range(len(data)):
            ws.append(input_data + data[i])

        wb.save('Результаты ТО.xlsx')



'''
        for row in range(rows):
            row_data = []
            for col in range(cols):
                item = self.result_table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)'''
'''
        # Сохранение данных в Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Результаты ТО"

        # Вставка заголовка таблицы
        header = ['Дата', 'Марка техники', 'Машиночасы', 'Номер ТО', 'Инвентарный номер', 'Работы', 'Количество план',
                  'Количество факт']
        ws.append(header)

        # Вставка вводных данных
        input_data = [date, mark, hours, to_number, inventory_number]
        for i in range(len(data)):
            ws.append(input_data + data[i])

        wb.save('Результаты ТО.xlsx')'''


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
