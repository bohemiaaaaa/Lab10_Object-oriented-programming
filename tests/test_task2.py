#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

import pytest
from task2 import Recipe, RecipeCatalog


@pytest.fixture
def filled_catalog():
    catalog = RecipeCatalog()
    catalog.add(Recipe("Рамен", "Японская", 40))
    catalog.add(Recipe("Суши", "Японская", 50))
    catalog.add(Recipe("Борщ", "Украинская", 60))
    return catalog


def test_recipe_fields():
    recipe = Recipe("Тако", "Мексиканская", 20)
    assert recipe.name == "Тако"
    assert recipe.cuisine == "Мексиканская"
    assert recipe.time == 20


def test_invalid_time_type():
    with pytest.raises(TypeError):
        Recipe("Паста", "Итальянская", None)


def test_filter_japanese_recipes(filled_catalog):
    result = filled_catalog.select_by_cuisine("японская")
    assert len(result) == 2


def test_sorting_by_time():
    catalog = RecipeCatalog()
    catalog.add(Recipe("Долгое", "Тест", 100))
    catalog.add(Recipe("Быстрое", "Тест", 5))

    assert catalog.recipes[0].time == 5


def test_json_roundtrip(tmp_path: Path):
    file = tmp_path / "data.json"

    catalog = RecipeCatalog()
    catalog.add(Recipe("Лапша", "Китайская", 25))
    catalog.save(file)

    loaded = RecipeCatalog()
    loaded.load(file)

    assert len(loaded.recipes) == 1
    assert loaded.recipes[0].cuisine == "Китайская"


def test_empty_catalog_str():
    catalog = RecipeCatalog()
    assert "пуст" in str(catalog).lower()
