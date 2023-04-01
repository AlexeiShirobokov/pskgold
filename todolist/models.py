from django.utils import timezone  # мы будем получать дату создания todo
from django.db import models


from django.utils import timezone
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class TodoList(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey(Category, default="general", on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

import os
import pandas as pd
df = pd.read_excel(os.path.join('Excel_dir', 'Регламент_инструкции.xlsx'), "Регламент")
df1 = pd.read_excel(os.path.join('Excel_dir', 'Регламент_инструкции.xlsx'), "Артикулы")
#df2 = pd.read_excel(os.path.join('Excel_dir', 'Регламент_инструкции.xlsx'), "Тип обслуживания")
#df3 = pd.read_excel(os.path.join('Excel_dir', 'Календарный План ТО_2023.xlsx'), "Календарь ТО")

####работа с
class MyModel(models.Model):
    brand = models.CharField(max_length=100)
    inventory_number = models.IntegerField()

    @staticmethod
    def create_from_dataframe(df):
        for index, row in df.iterrows():
            MyModel.objects.create(
                brand=row['brand'],
                inventory_number=row['inventory_number']
            )