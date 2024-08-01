from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', '_genre', 'category',)
    search_fields = ('name', '_genre', 'category',)
    list_filter = ('name', 'category',)

    def _genre(self, row):
        return ','.join([x.name for x in row.meta.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date',)
    list_editable = ('title',)
    search_fields = ('author', 'title', 'score', 'pub_date',)
    list_filter = ('author', 'title', 'score', 'pub_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date',)
    list_editable = ('review',)
    search_fields = ('author', 'review', 'pub_date',)
    list_filter = ('author', 'review', 'pub_date',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
