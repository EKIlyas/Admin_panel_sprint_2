from django.contrib import admin

from movies.models import FilmWork, Person, Genre, PersonFilmWork, GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 0
    fields = ('person', 'role',)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 0
    fields = ('genre',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')
    fields = ('full_name', 'birth_date',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description',)


@admin.register(FilmWork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating',)
    fields = ('title', 'type', 'description', 'creation_date', 'certificate', 'file_path', 'rating',)
    inlines = [PersonFilmWorkInline, GenreFilmWorkInline]
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id',)
