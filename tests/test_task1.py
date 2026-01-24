#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

import pytest
from task1 import Recipe, RecipeCatalog


@pytest.fixture
def catalog():
    return RecipeCatalog()


def test_recipe_creation():
    recipe = Recipe("Борщ", "Украинская", 60)
    assert recipe.name == "Борщ"
    assert recipe.cuisine == "Украинская"
    assert recipe.time == 60


def test_recipe_time_must_be_int():
    with pytest.raises(TypeError):
        Recipe("Борщ", "Украинская", "час")


def test_add_and_sort(catalog):
    catalog.add(Recipe("Долма", "Кавказская", 90))
    catalog.add(Recipe("Паста", "Итальянская", 20))

    assert len(catalog.recipes) == 2
    assert catalog.recipes[0].name == "Паста"
    assert catalog.recipes[1].name == "Долма"


@pytest.mark.parametrize(
    "cuisine, expected",
    [
        ("японская", 2),
        ("Украинская", 1),
        ("Французская", 0),
    ],
)
def test_select_by_cuisine(cuisine, expected):
    catalog = RecipeCatalog()
    catalog.add(Recipe("Суши", "Японская", 50))
    catalog.add(Recipe("Рамен", "Японская", 40))
    catalog.add(Recipe("Борщ", "Украинская", 60))

    result = catalog.select_by_cuisine(cuisine)
    assert len(result) == expected


def test_save_and_load_json(tmp_path: Path):
    file = tmp_path / "recipes.json"

    catalog = RecipeCatalog()
    catalog.add(Recipe("Пицца", "Итальянская", 30))
    catalog.save(file)

    new_catalog = RecipeCatalog()
    new_catalog.load(file)

    assert len(new_catalog.recipes) == 1
    assert new_catalog.recipes[0].name == "Пицца"


def test_load_nonexistent_file_does_not_fail():
    catalog = RecipeCatalog()
    catalog.load("no_such_file.json")
    assert catalog.recipes == []
