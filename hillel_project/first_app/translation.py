from modeltranslation.translator import TranslationOptions, register

from first_app.models import Department

from first_app.models import Position


@register(Position)
class PositionTranslationOption(TranslationOptions):
    fields = ("title", "description")

@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)
