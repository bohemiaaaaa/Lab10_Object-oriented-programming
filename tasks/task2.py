#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

import click


@dataclass(frozen=True)
class Recipe:
    name: str
    cuisine: str
    time: int


@dataclass
class RecipeCatalog:
    recipes: List[Recipe] = field(default_factory=list)

    def add(self, recipe: Recipe) -> None:
        self.recipes.append(recipe)
        self.recipes.sort(key=lambda r: r.time)

    def select_by_cuisine(self, cuisine: str) -> List[Recipe]:
        return [r for r in self.recipes if r.cuisine.lower() == cuisine.lower()]

    def load(self, filename: str) -> None:
        if not Path(filename).exists():
            return

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.recipes = [Recipe(**item) for item in data]
        self.recipes.sort(key=lambda r: r.time)

    def save(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(r) for r in self.recipes], f, ensure_ascii=False, indent=2
            )

    def __str__(self) -> str:
        if not self.recipes:
            return "Каталог рецептов пуст."

        lines = [
            "+----+------------------------------+--------------------+--------+",
            "| №  | Название                     | Кухня              | Время  |",
            "+----+------------------------------+--------------------+--------+",
        ]

        for i, r in enumerate(self.recipes, 1):
            lines.append(f"| {i:>2} | {r.name:<28} | {r.cuisine:<18} | {r.time:>6} |")

        lines.append(
            "+----+------------------------------+--------------------+--------+"
        )
        return "\n".join(lines)


# ====== CLI (CLICK) ======


@click.group()
@click.option("--file", default="recipes2.json", help="JSON-файл с данными")
@click.pass_context
def cli(ctx, file):
    """Каталог рецептов (CLI на click)"""
    catalog = RecipeCatalog()
    catalog.load(file)
    ctx.obj = {"catalog": catalog, "file": file}


@cli.command()
@click.option("--name", required=True, help="Название рецепта")
@click.option("--cuisine", required=True, help="Кухня")
@click.option("--time", required=True, type=int, help="Время приготовления")
@click.pass_context
def add(ctx, name, cuisine, time):
    """Добавить рецепт"""
    catalog = ctx.obj["catalog"]
    filename = ctx.obj["file"]

    catalog.add(Recipe(name, cuisine, time))
    catalog.save(filename)

    click.echo("Рецепт добавлен.")


@cli.command(name="list")
@click.pass_context
def list_recipes(ctx):
    """Показать все рецепты"""
    catalog = ctx.obj["catalog"]
    click.echo(catalog)


@cli.command()
@click.option("--cuisine", required=True, help="Кухня для выборки")
@click.pass_context
def select(ctx, cuisine):
    """Выборка рецептов по кухне"""
    catalog = ctx.obj["catalog"]
    result = catalog.select_by_cuisine(cuisine)

    if not result:
        click.echo("Ничего не найдено.")
    else:
        for r in result:
            click.echo(f"{r.name} — {r.time} мин")


@cli.command()
@click.pass_context
def save(ctx):
    """Сохранить данные"""
    catalog = ctx.obj["catalog"]
    filename = ctx.obj["file"]

    catalog.save(filename)
    click.echo("Данные сохранены.")


@cli.command()
@click.pass_context
def load(ctx):
    """Загрузить и показать данные"""
    catalog = ctx.obj["catalog"]
    click.echo("Данные загружены.")
    click.echo(catalog)


if __name__ == "__main__":
    cli()
