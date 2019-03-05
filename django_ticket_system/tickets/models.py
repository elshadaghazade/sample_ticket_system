from django.db import models

class Tickets(models.Model):
    name = models.CharField(max_length=255)
    satilib = models.BooleanField(default=False)
    alici = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.satilib}"

    class Meta:
        verbose_name = 'Bilet'
        verbose_name_plural = 'Biletlər'