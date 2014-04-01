from django.contrib import admin
from watson.models import Sessions, State, ArticleTypes, SessionArticles, ArticleData, Type


# Register your models here.


def generate_article_set(modeladmin, request, queryset):
    pass


generate_article_set.short_description = "Generate article set"


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'size')
    actions = [generate_article_set]

    save_plus_action = [generate_article_set]


admin.site.register(Sessions, SessionAdmin)
admin.site.register(State)
admin.site.register(ArticleTypes)
admin.site.register(SessionArticles)
admin.site.register(ArticleData)
admin.site.register(Type)
