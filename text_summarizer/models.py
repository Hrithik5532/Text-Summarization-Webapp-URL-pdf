from django.db import models

# Create your models here.

class PDFModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='pdfs/')
