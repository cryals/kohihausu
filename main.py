#!/usr/bin/env python3
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from game.core import GameCore
from ui.interface import MainMenu
from data.config import DIFFICULTY_LEVELS

console = Console()

def initialize_game():
    """Инициализация игры с красивым интерфейсом."""
    console.clear()
    console.print(Panel.fit(
        Text("Добро пожаловать в Kohihausu ☕🐾\nТекстовый симулятор кофейного дома!", style="bold magenta", justify="center"),
        border_style="green",
        padding=(2, 4)
    ))
    if not os.path.exists("data"):
        os.makedirs("data")
    return GameCore()

def choose_difficulty(game):
    """Выбор сложности с красивым интерфейсом."""
    console.clear()
    console.print(Panel(
        Text("Выберите сложность игры", style="bold cyan", justify="center"),
        border_style="yellow",
        padding=(1, 2)
    ))
    table = Text()
    for i, level in enumerate(DIFFICULTY_LEVELS.keys(), 1):
        table.append(f"{i}. {level}\n", style="green")
    console.print(table, justify="center")
    choice = console.input("[bold yellow]Введите номер сложности (1-3): [/]").strip()
    difficulties = list(DIFFICULTY_LEVELS.keys())
    game.difficulty = difficulties[int(choice) - 1] if choice in "123" else "Medium"
    console.print(f"[green]Выбрана сложность: {game.difficulty}[/]", justify="center")
    console.input("[yellow]Нажмите Enter для продолжения...[/]")

def main():
    """Основная функция запуска игры."""
    game = initialize_game()
    menu = MainMenu(game, console)
    
    while True:
        console.clear()
        menu.display()
        choice = console.input("[bold yellow]Выберите действие: [/]").strip()
        if choice == "1":
            console.clear()
            console.print(Panel(
                Text("Назови свою кофейню!", style="bold magenta", justify="center"),
                border_style="green",
                padding=(1, 2)
            ))
            game.cafe_name = console.input("[bold yellow]Введите название: [/]").strip() or "Kohihausu"
            game.apply_name_bonuses()
            console.print(f"[green]Кофейня названа '{game.cafe_name}'![/]", justify="center")
            skip = console.input("[bold yellow]Хотите пройти обучение? (да/нет): [/]").strip().lower() == "нет"
            game.skip_tutorial = skip
            choose_difficulty(game)
            game.start_new_game()
        elif choice == "2":
            game.load_game()
        elif choice == "3":
            console.clear()
            game.display_status()
            console.input("[yellow]Нажмите Enter для возврата...[/]")
        elif choice == "4":
            game.shop_menu()
        elif choice == "5":
            game.finance_menu()
        elif choice == "6":
            game.settings_menu()
        elif choice == "7":
            console.clear()
            console.print(Panel(
                Text("До встречи в Kohihausu! ☕🐾", style="italic cyan", justify="center"),
                border_style="blue",
                padding=(1, 2)
            ))
            break
        else:
            console.print("[red]Неверный выбор, попробуйте снова![/]", justify="center")

if __name__ == "__main__":
    main()