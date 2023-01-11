from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_at', 'updated_at']


class Business(TimeStampedModel):
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_to_business'
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f'{self.user} {self.name}'

class Income(TimeStampedModel):
    income = models.PositiveIntegerField()
    customer_count = models.PositiveIntegerField()
    month = models.CharField(max_length=50)
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        related_name='business_income'
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f'{self.business} {self.income}'

class Outcome(TimeStampedModel):
    salary = models.PositiveIntegerField()
    marketing = models.PositiveIntegerField()
    month = models.CharField(max_length=50)
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        related_name='business_outcome'
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f'{self.business} {self.salary}'