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
from django.shortcuts import render
from .models import MyModel

def equipment_list(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        inventory_number = request.POST['inventory_number']
        queryset = MyModel.objects.filter(
            brand__icontains=brand,
            inventory_number__icontains=inventory_number,
        )
    else:
        queryset = MyModel.objects.all()

    context = {
        'object_list': queryset,
    }
    return render(request, 'myapp/MyModel.html', context)


