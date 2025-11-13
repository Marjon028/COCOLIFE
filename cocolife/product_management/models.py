from django.db import models

# Create your models here.
class Policy_Owner(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    decription = models.TextField()
    label = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Policy_Owner_Fields(models.Model):
    field_type_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
    ]
    id = models.BigAutoField(primary_key=True)
    policy_owner = models.ForeignKey(Policy_Owner, related_name='fields', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=field_type_CHOICES)
    field_type_list = models.TextField(blank=True, null=True)  # Comma-separated values for list type
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.field_name}"

class Policy_Owner_Values(models.Model):
    id = models.BigAutoField(primary_key=True)
    policy_owner = models.ForeignKey(Policy_Owner, related_name='values', on_delete=models.CASCADE)
    field = models.ForeignKey(Policy_Owner_Fields, related_name='values', on_delete=models.CASCADE)
    value = models.TextField()
    row_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    

   



