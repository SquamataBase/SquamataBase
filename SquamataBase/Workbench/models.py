from django.db import models

class Workbench(models.Model):
    class Meta:
        db_table = 'sb_workbench'


class FoodRecordWorkbench(Workbench):
    class Meta:
        proxy = True
        verbose_name = 'food record'
        verbose_name_plural = 'food records'

    def __str__(self):
        from SquamataBase.FoodRecord.models import FoodRecord
        return str(FoodRecord.objects.get(wb=self.pk))
