from django.shortcuts import render, redirect  # для отображения и редиректа берем необходимые классы
from django.http import HttpResponse
from .models import TodoList, Category  # не забываем наши модели


def redirect_view(request):
    return redirect("/category")  # редирект с главной на категории

def todo(request):
    todos = TodoList.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        if "Add" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save()
            return redirect("/todo")
        if "Delete" in request.POST:
            checkedlist = request.POST.getlist('checkedbox')
            for i in range(len(checkedlist)):
                todo = TodoList.objects.filter(id=int(checkedlist[i]))
                todo.delete()
    return render(request, "todo.html", {"todos": todos, "categories": categories})

def category(request):
    categories = Category.objects.all()
    if request.method == "POST":
        if "Add" in request.POST:
            name = request.POST["name"]
            category = Category(name=name)
            category.save()
            return redirect("/category")
        if "Delete" in request.POST:
            check = request.POST.getlist('check')
            for i in range(len(check)):
                try:
                    сateg = Category.objects.filter(id=int(check[i]))
                    сateg.delete()
                except BaseException:
                    return HttpResponse('<h1>Сначала удалите карточки с этими категориями)</h1>')
    return render(request, "category.html", {"categories": categories})


###работа с ТО
import pandas as pd
from django.shortcuts import render
from .models import MyModel

def equipment_list(request):
    if request.method == 'POST':
        brand = request.POST.get('brand', '')
        inventory_number = request.POST.get('inventory_number', '')
        quantity = request.POST.get('quantity', '')  # получаем значение кол-ва факт

        if 'action' in request.POST and request.POST['action'] == 'send': # проверяем, что была нажата кнопка "Передать"
            # Добавить код для передачи данных другому пользователю
            pass
        df = pd.read_excel('Excel_dir/Регламент_инструкции.xlsx', sheet_name='Регламент')
        print(df.head())  # проверяем, что данные загрузились корректно

        # проверяем, что имена столбцов соответствуют ожидаемым
        print(df.columns)

        # фильтруем DataFrame
        queryset = df[(df['Марка техники'] == brand) & (df['Вид ТО'] == inventory_number)]
        print(queryset.head())  # проверяем, что фильтрация прошла корректно
        queryset['Кол-во факт'] = quantity  # добавляем колонку с кол-вом факт
        print(queryset.head())  # проверяем, что фильтрация прошла корректно
    else:
        queryset = pd.DataFrame()

    context = {
        'object_list': queryset.to_dict(orient='records'),
    }
    return render(request, 'MyModel.html', context)

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Request

class RequestCreateView(CreateView):
    model = Request
    fields = ['title', 'description', 'created_by']
    template_name = 'request_create.html'
    success_url = reverse_lazy('request_created')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
