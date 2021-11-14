from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Role(models.TextChoices):
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
    ACTOR = 'actor', _('actor')


class Person(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True)
    full_name = models.CharField(_('full name'), max_length=255)
    birth_date = models.DateField(_('birth date'), null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = 'content\".\"person'


class Genre(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = 'content\".\"genre'


class FilmWork(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    creation_date = models.DateField(_('creation date'), null=True)
    certificate = models.CharField(_('certificate'), max_length=255)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        db_table = 'content\".\"film_work'


class PersonFilmWork(models.Model):
    id = models.UUIDField('id', primary_key=True)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE, verbose_name=_('film work'))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('person'))
    role = models.CharField(_('role'), max_length=10, choices=Role.choices, default=Role.ACTOR)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = [
            models.UniqueConstraint(fields=['person', 'film_work', 'role'], name='person_role_film')
        ]


class GenreFilmWork(models.Model):
    id = models.UUIDField('id', primary_key=True)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='genre_film')
        ]
