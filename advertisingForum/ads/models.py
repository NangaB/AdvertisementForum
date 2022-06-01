from django.db import models
from django.contrib.auth.models import User

class Advertisement(models.Model):
    company = models.CharField(max_length=300)
    adress = models.CharField(max_length=400)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=14)
    desc = models.TextField()
    industries = [
        ('', 'Choose industry'),
        ('nr', 'Nieruchomości'),
        ('zd', 'Zdrowie'),
        ('mt', 'Motoryzacja'),
        ('ft', 'Fitness')
    ]
    industry = models.CharField(max_length=2,choices=industries, default='')
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.company

    def display_industry(self):
        for industry in self.industries:
            if self.industry in industry:
                to_Display = industry[1]
        return to_Display
