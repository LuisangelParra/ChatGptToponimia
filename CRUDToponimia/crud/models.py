from django.db import models
from openai import OpenAI
import os

OpenAI.api_key = os.environ.get( 'OPENAI_API_KEY' )

# Create your models here.
class Person(models.Model):
    DOCUMENT_TYPES = [
        ("CC", "Cédula de Ciudadanía"),
        ("CE", "Cédula de Extranjería"),
        ("PA", "Pasaporte")
    ]
    GENDERS = [
        ("M", "Masculino"),
        ("F", "Femenino")
    ]
    id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES)
    document_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    lasts_names = models.CharField(max_length=30)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    toponimia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.lasts_names
    
    def save(self, *args, **kwargs):
        if not self.toponimia:  # Solo generamos si no hay un valor ya asignado
            self.toponimia = self.generate_toponimia()
        super().save(*args, **kwargs)

    def generate_toponimia(self):
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f'Origen del nombre "{self.first_name}" según la toponimia.'}],
        )
        return response.choices[0].message.content


class Log(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.action}"
