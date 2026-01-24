#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

from task2 import Recipe, RecipeCatalog


def test_recipe_dataclass():
    recipe = Recipe("Рамен", "Японская", 40)
    assert recipe.name == "Рамен"
    assert recipe.cuisine == "Японская"
    assert recipe.time == 40


def test_catalog_add():
    catalog = RecipeCatalog()
    catalog.add(Recipe("Бургер", "Американская", 15))

    assert len(catalog.recipes) == 1
    assert catalog.recipes[0].name == "Бургер"


def test_catalog_sorting():
    catalog = RecipeCatalog()
    catalog.add(Recipe("Суп", "Русская", 45))
    catalog.add(Recipe("Салат", "Европейская", 10))

    assert catalog.recipes[0].time == 10


def test_catalog_filter():
    catalog = RecipeCatalog()
    catalog.add(Recipe("Тако", "Мексиканская", 20))
    catalog.add(Recipe("Буррито", "Мексиканская", 30))
    catalog.add(Recipe("Плов", "Узбекская", 90))

    result = catalog.select_by_cuisine("мексиканская")
    assert len(result) == 2


def test_json_persistence(tmp_path: Path):
    file = tmp_path / "data.json"

    catalog = RecipeCatalog()
    catalog.add(Recipe("Лапша", "Китайская", 25))
    catalog.save(file)

    new_catalog = RecipeCatalog()
    new_catalog.load(file)

    assert len(new_catalog.recipes) == 1
    assert new_catalog.recipes[0].cuisine == "Китайская"


def test_empty_catalog_str():
    catalog = RecipeCatalog()
    assert "пуст" in str(catalog).lower()
