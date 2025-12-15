from django.shortcuts import render, redirect

def calculator_view(request):
    result = None
    error = None

    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1'))
            num2_raw = request.POST.get('num2')
            num2 = float(num2_raw) if num2_raw else 0
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
            elif operation == 'power':
                result = num1 ** num2
            elif operation == 'sqrt':
                if num1 >= 0:
                    result = num1 ** 0.5
                else:
                    error = "Невозможно извлечь корень из отрицательного числа."
            else:
                error = "Неизвестная операция."

            if result is not None:
                history = request.session.get('history', [])
                # сохраняем числа, операцию и результат
                history.insert(0, {
                    'num1': num1,
                    'num2': num2,
                    'operation': operation,
                    'result': result
                })
                request.session['history'] = history[:10]

        except ValueError:
            error = "Введите корректные числа."

    return render(request, 'calculator/calculator.html', {'result': result, 'error': error})


def history_view(request):
    history = request.session.get('history', [])

    # Формируем список строк для отображения с математическими знаками
    history_display = []
    for item in history:
        op = item['operation']
        if op == 'add':
            s = f"{item['num1']} + {item['num2']} = {item['result']}"
        elif op == 'subtract':
            s = f"{item['num1']} - {item['num2']} = {item['result']}"
        elif op == 'multiply':
            s = f"{item['num1']} * {item['num2']} = {item['result']}"
        elif op == 'divide':
            s = f"{item['num1']} / {item['num2']} = {item['result']}"
        elif op == 'power':
            s = f"{item['num1']} ^ {item['num2']} = {item['result']}"
        elif op == 'sqrt':
            s = f"√{item['num1']} = {item['result']}"
        history_display.append(s)

    if request.method == 'POST' and request.POST.get('clear'):
        request.session['history'] = []
        return redirect('history')

    return render(request, 'calculator/history.html', {'history_display': history_display})
