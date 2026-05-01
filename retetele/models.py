from django.contrib.auth.models import User
from django.db import models
from prieteni.models import CustomUser
from django.conf import settings
from django.utils import timezone

class Retete(models.Model):
    class Categorie(models.TextChoices):
        MIC_DEJUN = "MD", "Mic dejun"
        PRAJITURI = "PR", "Prăjituri"
        TORTURI = "TO", "Torturi"
        SUPE = "SU", "Supe și ciorbe"
        GARNITURI = "GA", "Garnituri"
        CARNE = "CA", "Carne"
        PESTE = "PE", "Pește"
    nume = models.CharField(max_length=200)
    categorie = models.CharField(
        max_length=30,
        choices=Categorie.choices,
        default="mic_dejun"
    )
    ingrediente = models.TextField()
    preparare = models.TextField()
    data_creare = models.DateTimeField(default=timezone.now)

    timp_pregatire = models.TextField(null=True, blank=True)
    timp_gatire = models.TextField(null=True, blank=True)



    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="retete",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    poza = models.ImageField(upload_to="poze_retete/", null=True, blank=True)

    def __str__(self):
        return self.nume


class Comment(models.Model):
    reteta = models.ForeignKey(Retete, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    reteta = models.ForeignKey(Retete, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("reteta", "user")