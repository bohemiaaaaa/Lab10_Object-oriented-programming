#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date

@dataclass(frozen=True)
class Worker:
    name: str
    post: str
    year: int

@dataclass
class Staff:
    workers: list[Worker] = field(default_factory=lambda: [])

    def add(self, name: str, post: str, year: int) -> None:
        self.workers.append(Worker(name=name, post=post, year=year))
        self.workers.sort(key=lambda worker: worker.name)

    def __str__(self) -> str:
        table = []
        line = '+{}+{}+{}+{}+'.format('-'*4, '-'*30, '-'*20, '-'*8)
        table.append(line)
        table.append('{:^4} | {:^30} | {:^20} | {:^8} | '.format("№", "Ф.И.О.", "Должность", "Год"))
        table.append(line)

        for idx, worker in enumerate(self.workers, 1):
            table.append('{:>4} | {:<30} | {:<20} | {:>8} | '.format(idx, worker.name, worker.post, worker.year))
        table.append(line)
        return '\n'.join(table)

    def select(self, period: int) -> list[Worker]:
        today = date.today()
        return [worker for worker in self.workers if today.year - worker.year >= period]

    def load(self, filename: str) -> None:
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.workers = []
        for worker_element in tree:
            name = post = year = None
            for element in worker_element:
                if element.tag == 'name': name = element.text
                elif element.tag == 'post': post = element.text
                elif element.tag == 'year': year = int(element.text)

            if name and post and year is not None:
                self.workers.append(Worker(name=name, post=post, year=year))

    def save(self, filename: str) -> None:
        root = ET.Element('workers')
        for worker in self.workers:
            worker_element = ET.Element('worker')
            ET.SubElement(worker_element, 'name').text = worker.name
            ET.SubElement(worker_element, 'post').text = worker.post
            ET.SubElement(worker_element, 'year').text = str(worker.year)
            root.append(worker_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fout:
            tree.write(fout, encoding='utf8', xml_declaration=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Система учёта сотрудников (dataclass + XML + argparse)")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Добавить сотрудника")
    add_parser.add_argument("--name", required=True, help="Фамилия и инициалы")
    add_parser.add_argument("--post", required=True, help="Должность")
    add_parser.add_argument("--year", required=True, type=int, help="Год поступления")

    subparsers.add_parser("list", help="Показать всех сотрудников")

    select_parser = subparsers.add_parser("select", help="Выбрать по стажу")
    select_parser.add_argument("--period", required=True, type=int, help="Стаж (годы)")

    load_parser = subparsers.add_parser("load", help="Загрузить из XML")
    load_parser.add_argument("filename", help="Имя XML файла")

    save_parser = subparsers.add_parser("save", help="Сохранить в XML")
    save_parser.add_argument("filename", help="Имя XML файла")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    staff = Staff()

    if args.command == "add":
        staff.add(args.name, args.post, args.year)
        print("Сотрудник добавлен.")
    elif args.command == "list":
        print(staff)
    elif args.command == "select":
        selected = staff.select(args.period)
        if selected:
            for idx, worker in enumerate(selected, 1):
                print(f"{idx}: {worker.name}")
        else:
            print("Работники с заданным стажем не найдены.")
    elif args.command == "load":
        staff.load(args.filename)
        print(f"Данные загружены из {args.filename}")
    elif args.command == "save":
        staff.save(args.filename)
        print(f"Данные сохранены в {args.filename}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()