from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    address = models.CharField(max_length=255, verbose_name=_('address'))
    email = models.EmailField(verbose_name=_('email'))
    tax_code = models.CharField(max_length=255, verbose_name=_('tax_code'))

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and Company.objects.exists():
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



