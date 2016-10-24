from django.db import models

class Workbench(models.Model):
    class Meta:
        db_table = 'sb_workbench'


class FoodRecordWorkbench(Workbench):
    class Meta:
        proxy = True
        verbose_name = 'Food Record'
        verbose_name_plural = 'Food Records'

    def __str__(self):
        return 'Food Record'