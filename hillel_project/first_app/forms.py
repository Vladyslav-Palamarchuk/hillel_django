from datetime import date
import calendar
from django import forms
from django.forms import ChoiceField

from first_app.models import Employee

from common.enums import WorkDayEnum





class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'email', 'position')




class SalaryForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())


    def clean_employee(self):
        employee = self.cleaned_data.get('employee')
        if not employee:
            raise forms.ValidationError("Поле Employee має бути заповнене!")
        return employee

    def clean(self):
        cleaned_data = super().clean()
        sick_days = cleaned_data.get('sick_days')
        holiday_days = cleaned_data.get('holiday_days')

        if sick_days and sick_days > 5:
            raise forms.ValidationError("Кількість лікарняних не має перевищувати 5-ти днів")

        if holiday_days and holiday_days > 3:
            raise forms.ValidationError("Кількість відпочинку не має перевищувати 3-м дням")

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = date.today()


        week_day, num_days = calendar.monthrange(today.year, today.month)
        for day in range(1, num_days + 1):
            day_coord = today.year, today.month, day

            weekday = calendar.weekday(*day_coord)
            weekday_name = calendar.day_name[weekday]
            field_name = f"day_{day}"

            if calendar.weekday(*day_coord) >= 5:
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=[(WorkDayEnum.WEEKEND.name, WorkDayEnum.WEEKEND.value)], # [("WEEKDAY", "working_day")]
                    initial=WorkDayEnum.WEEKEND.name
                )

            else:
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=[(option.name, option.value) for option in WorkDayEnum],
                    initial=WorkDayEnum.WORKING_DAY.name,
                )