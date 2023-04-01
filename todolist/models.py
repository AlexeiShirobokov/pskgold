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

#создадим пользователей с должностями

class Position(models.Model):
    name = models.CharField(max_length=50)

# Определите модель для пользователей, которая будет связана с моделью должности:
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

#Создайте несколько должностей и сохраните их в базе данных:
position1 = Position(name='Механик')
position1.save()

position2 = Position(name='Главный механик')
position2.save()

#Создайте несколько пользователей и добавьте им должность:
user1 = User.objects.create_user(username='user1', password='password1')
user_profile1 = UserProfile(user=user1, position=position1)
user_profile1.save()

user2 = User.objects.create_user(username='user2', password='password2')
user_profile2 = UserProfile(user=user2, position=position2)
user_profile2.save()
