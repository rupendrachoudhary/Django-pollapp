from django.contrib import admin
from .models import PollQuestion, PollAnswer


admin.site.site_header = "Polling Admin"
admin.site.site_title = "Polling project Admin"
admin.site.index_title = "Welcome to the Polling Admin Section"

class PollAnswerInline(admin.TabularInline):
    model = PollAnswer
    extra = 3


class PollQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_date', 'was_published_recently')
    list_filter = ['question_date']
    search_fields = ['question']
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Date Information', {'fields': ['question_date'], 'classes': ['collapse']}),

    ]
    inlines = [PollAnswerInline]


admin.site.register(PollQuestion, PollQuestionAdmin)
admin.site.register(PollAnswer)

