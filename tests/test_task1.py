#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

from task1 import Recipe, RecipeCatalog


def test_recipe_creation():
    recipe = Recipe("Борщ", "Украинская", 60)
    assert recipe.name == "Борщ"
    assert recipe.cuisine == "Украинская"
    assert recipe.time == 60


def test_add_recipe_and_sort():
    catalog = RecipeCatalog()

    catalog.add(Recipe("Долма", "Кавказская", 90))
    catalog.add(Recipe("Паста", "Итальянская", 20))

    assert len(catalog.recipes) == 2
    assert catalog.recipes[0].name == "Паста"  # сортировка по времени


def test_select_by_cuisine():
    catalog = RecipeCatalog()
    catalog.add(Recipe("Суши", "Японская", 50))
    catalog.add(Recipe("Рамен", "Японская", 40))
    catalog.add(Recipe("Борщ", "Украинская", 60))

    result = catalog.select_by_cuisine("японская")
    assert len(result) == 2
    assert all(r.cuisine == "Японская" for r in result)


def test_save_and_load_json(tmp_path: Path):
    file = tmp_path / "recipes.json"

    catalog = RecipeCatalog()
    catalog.add(Recipe("Пицца", "Итальянская", 30))
    catalog.save(file)

    assert file.exists()

    new_catalog = RecipeCatalog()
    new_catalog.load(file)

    assert len(new_catalog.recipes) == 1
    assert new_catalog.recipes[0].name == "Пицца"


def test_load_nonexistent_file():
    catalog = RecipeCatalog()
    catalog.load("nonexistent.json")
    assert catalog.recipes == []
