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
print(df)
####работа с
class MyModel(models.Model):
    brand = models.CharField(max_length=100)
    inventory_number = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    @classmethod
    def create_from_dataframe(cls, df):
        for _, row in df.iterrows():
            cls.objects.create(
                brand=row['Марка техники'],
                inventory_number=row['Вид ТО']
            )

    def __str__(self):
        return f"{self.brand}, {self.inventory_number}"


from django.db import models
from django.contrib.auth.models import User, Group


#заявка
class Request(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, null=True, blank=True, related_name='processed_requests', on_delete=models.CASCADE)
    processed_at = models.DateTimeField(null=True, blank=True)

class Detail(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    requested_by = models.ForeignKey(User, related_name='requested_details', on_delete=models.CASCADE)
    processed_by = models.ForeignKey(User, null=True, blank=True, related_name='processed_details', on_delete=models.CASCADE)
    processed_at = models.DateTimeField(null=True, blank=True)

class CustomUser(User):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
