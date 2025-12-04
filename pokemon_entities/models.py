from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200,verbose_name='название')
    photo = models.ImageField (upload_to="pokemon_photo/",verbose_name='изображение')
    description = models.TextField(blank=True,verbose_name='описание')
    title_en = models.CharField(max_length=200,blank=True,verbose_name='английское название')
    title_jp = models.CharField(max_length=200,blank=True,verbose_name='японское название')
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_evolutions",
        verbose_name='предыдущая эволюция'
        )

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="pokemon_entities",
        verbose_name='покемон'
        )    
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='появился')
    disappeared_at = models.DateTimeField(verbose_name='пропал')
    level = models.IntegerField(null=True,blank=True,verbose_name='уровень')
    health = models.IntegerField(null=True,blank=True,verbose_name='здоровье')
    attack = models.IntegerField(null=True,blank=True,verbose_name='атака')
    defense = models.IntegerField(null=True,blank=True,verbose_name='защита')
    stamina = models.IntegerField(null=True,blank=True,verbose_name='выносливость')