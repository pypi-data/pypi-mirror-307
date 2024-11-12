from django.db import models


class DdosSettings(models.Model):
    endpoint = models.CharField(max_length=255, unique=True, blank=True, null=True)
    timeout = models.PositiveIntegerField(default=5 * 60)
    max_requests = models.PositiveIntegerField(default=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"Max Requests: {self.max_requests}, Block Time: {self.timeout} seconds"
