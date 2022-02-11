from django.db import models

from userApp.models import User, Organization


class DNA(models.Model):
    gene_sequence = models.CharField(max_length=5001)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.organization}'


class Order(models.Model):  
    STATUS_UNDER_REVIEW = 'R'
    STATUS_IN_PRODUCTION = 'P'  
    STATUS_CHOICES = [
        (STATUS_UNDER_REVIEW, 'Under Review'),
        (STATUS_IN_PRODUCTION, 'In Production'),
    ]


    dna = models.ForeignKey(DNA, on_delete=models.PROTECT, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=.09)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_UNDER_REVIEW)
