from django.contrib import admin

from .models import DdosSettings

admin.site.register(DdosSettings)


@admin.register(DdosSettings)
class RateLimitAdmin(admin.ModelAdmin):
    list_display = ("endpoint", "timeout", "max_requests", "is_default")
    search_fields = ("endpoint",)

    def save_model(self, request, obj, form, change):
        if obj.is_default:
            if (
                change
                and DdosSettings.objects.filter(id=obj.id, is_default=True).exists()
            ):
                super().save_model(request, obj, form, change)
                return

            DdosSettings.objects.exclude(id=obj.id).update(is_default=False)

        super().save_model(request, obj, form, change)
