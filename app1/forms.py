from django import forms


class Task(forms.Form):
    summary = forms.CharField(label="Тема")
    priority = forms.ChoiceField(choices=((1, "Низкий"), (2, "Средний"), (3, "Высокий")), label="Приоритет")
    description = forms.CharField(widget=forms.Textarea, label="Описание")
    # created_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                   label="Срок исполнения")
