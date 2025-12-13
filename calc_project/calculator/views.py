from django.shortcuts import render

from django.shortcuts import render

def index(request):
    result = None
    error = None

    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1'))
            num2 = float(request.POST.get('num2'))
            operation = request.POST.get('operation')

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                else:
                    error = "Деление на ноль невозможно."
            else:
                error = "Неизвестная операция."
        except ValueError:
            error = "Введите корректные числа."

    return render(request, 'calculator/index.html', {'result': result, 'error': error})

