import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision"
    "/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832"
    "&fill=transparent"
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in PokemonEntity.objects.filter(
        disappeared_at__gt=localtime(), appeared_at__lt=localtime()
    ):
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.photo.url),
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append(
            {
                "pokemon_id": pokemon.id,
                "img_url": request.build_absolute_uri(pokemon.photo.url),
                "title_ru": pokemon.title,
            }
        )

    return render(
        request,
        "mainpage.html",
        context={
            "map": folium_map._repr_html_(),
            "pokemons": pokemons_on_page,
        },
    )


def show_pokemon(request, pokemon_id):
    if Pokemon.objects.get(id=int(pokemon_id)):
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    else:
        return HttpResponseNotFound("<h1>Такой покемон не найден</h1>")

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon.pokemon_entities.all():
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url),
        )
    pokemon = {
        "pokemon_id": requested_pokemon.id,
        "img_url": request.build_absolute_uri(requested_pokemon.photo.url),
        "title_ru": requested_pokemon.title,
        "description": requested_pokemon.description,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "previous_evolution": "",
        "next_evolution": "",
    }
    if requested_pokemon.previous_evolution:
        pokemon["previous_evolution"] = {
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(
                requested_pokemon.previous_evolution.photo.url
            ),
            "title_ru": requested_pokemon.previous_evolution.title,
        }
    next_pokemon = requested_pokemon.next_evolution.first()
    if requested_pokemon.next_evolution.first():
        pokemon["next_evolution"] = {
            "pokemon_id": next_pokemon.id,
            "img_url": request.build_absolute_uri(next_pokemon.photo.url),
            "title_ru": next_pokemon.title,
        }

    return render(
        request,
        "pokemon.html",
        context={"map": folium_map._repr_html_(), "pokemon": pokemon},
    )
