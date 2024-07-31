from django.db import models

LENGTH_LIMIT = 50


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год',)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name[:LENGTH_LIMIT]
