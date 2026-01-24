#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List


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


# ====== CLI ======


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Каталог рецептов (CLI, dataclass, JSON)"
    )

    parser.add_argument("--file", default="recipes.json", help="JSON-файл с данными")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="Добавить рецепт")
    add.add_argument("--name", required=True)
    add.add_argument("--cuisine", required=True)
    add.add_argument("--time", required=True, type=int)

    subparsers.add_parser("list", help="Показать все рецепты")

    select = subparsers.add_parser("select", help="Выборка по кухне")
    select.add_argument("--cuisine", required=True)

    subparsers.add_parser("save", help="Сохранить данные")

    subparsers.add_parser("load", help="Загрузить данные")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    catalog = RecipeCatalog()
    catalog.load(args.file)

    if args.command == "add":
        catalog.add(Recipe(args.name, args.cuisine, args.time))
        catalog.save(args.file)
        print("Рецепт добавлен.")

    elif args.command == "list":
        print(catalog)

    elif args.command == "select":
        result = catalog.select_by_cuisine(args.cuisine)
        if not result:
            print("Ничего не найдено.")
        else:
            for r in result:
                print(f"{r.name} — {r.time} мин")

    elif args.command == "save":
        catalog.save(args.file)
        print("Данные сохранены.")

    elif args.command == "load":
        print("Данные загружены.")
        print(catalog)


if __name__ == "__main__":
    main()
