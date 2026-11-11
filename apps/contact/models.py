from django.db import models
class Entry(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    time_of_entry = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_of_entry']
        verbose_name = 'Contact Entry'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
