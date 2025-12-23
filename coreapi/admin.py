from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html
import json
from .models import SiteVisitReport


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user_name", "email", "role", "created_at","password")

@admin.register(SiteVisitReport)
class SiteVisitReportAdmin(admin.ModelAdmin):
    list_display = ('office_file_no', 'applicant_name', 'created_at', 'sketch_preview')
    search_fields = ('office_file_no', 'applicant_name')
    readonly_fields = ('formatted_data', 'sketch_preview')

    def sketch_preview(self, obj):
        if obj.sketch:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.sketch.url)
        return "No Sketch"
    sketch_preview.short_description = "Sketch"

    def formatted_data(self, obj):
        # Pretty print the JSON
        return format_html('<pre>{}</pre>', json.dumps(obj.form_data, indent=4))
    formatted_data.short_description = "Full Form Data"

    # Show the formatted data in the detail view
    fieldsets = (
        ("Meta Info", {
            "fields": ("user", "office_file_no", "applicant_name", "created_at")
        }),
        ("Sketch", {
            "fields": ("sketch", "sketch_preview")
        }),
        ("Form Data", {
            "fields": ("formatted_data",)
        }),
    )