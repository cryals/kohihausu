from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from ui.themes import Themes

class MainMenu:
    def __init__(self, game, console: Console):
        self.game = game
        self.console = console
        self.themes = Themes()

    def display(self):
        menu_text = Text.assemble(
            ("1. ", "bold yellow"), ("Новая игра\n", "green"),
            ("2. ", "bold yellow"), ("Загрузить игру\n", "green"),
            ("3. ", "bold yellow"), ("Статистика\n", "cyan"),
            ("4. ", "bold yellow"), ("Магазин\n", "cyan"),
            ("5. ", "bold yellow"), ("Финансы\n", "cyan"),
            ("6. ", "bold yellow"), ("Настройки\n", "cyan"),
            ("7. ", "bold yellow"), ("Выход\n", "red")
        )
        panel = Panel(
            menu_text,
            title=Text("Kohihausu ☕🐾", style="bold magenta"),
            subtitle="Выберите действие",
            border_style="bright_green",
            style="white",
            padding=(1, 2),
            width=50
        )
        self.console.print(panel, justify="center")

class GameMenu:
    def __init__(self, game, console: Console):
        self.game = game
        self.console = console
        self.themes = Themes()

    def display(self):
        menu_text = Text.assemble(
            ("1. ", "bold yellow"), ("Следующий день\n", "green"),
            ("2. ", "bold yellow"), ("Сохранить игру\n", "green"),
            ("3. ", "bold yellow"), ("Магазин\n", "cyan"),
            ("4. ", "bold yellow"), ("Финансы\n", "cyan"),
            ("5. ", "bold yellow"), ("Персонал\n", "cyan"),
            ("6. ", "bold yellow"), ("Питомцы\n", "cyan"),
            ("7. ", "bold yellow"), ("Ассортимент\n", "cyan"),
            ("8. ", "bold yellow"), ("Улучшения\n", "cyan"),
            ("9. ", "bold yellow"), ("Смена локации\n", "cyan"),
            ("10. ", "bold yellow"), ("Франшизы\n", "cyan"),
            ("11. ", "bold yellow"), ("Маркетинг\n", "cyan"),
            ("12. ", "bold yellow"), ("Престиж\n", "cyan"),
            ("13. ", "bold yellow"), ("Выйти в главное меню\n", "red")
        )
        panel = Panel(
            menu_text,
            title=Text(f"Кофейный дом '{self.game.cafe_name}' ☕", style="bold magenta"),
            subtitle=Text(f"День {self.game.day}", style="italic cyan"),
            border_style="bright_green",
            style="white",
            padding=(1, 2),
            width=50
        )
        self.console.print(panel, justify="center")

    def display_shop(self):
        table = Table(title=Text("Магазин ☕", style="bold magenta"), box=None, show_header=True, header_style="bold cyan")
        table.add_column("Категория", style="cyan", width=15)
        table.add_column("Название", style="magenta", width=20)
        table.add_column("Цена", style="yellow", justify="right", width=10)
        table.add_column("Эффект", style="green", width=25)
        items = self.game.upgrades.load_items()
        for category, items_dict in items.items():
            for name, data in items_dict.items():
                cost = self.game.calculate_dynamic_cost(data["base_cost"])
                table.add_row(category, name, f"${cost}", f"{data['bonus_type']} +{data['bonus_value']}")
        panel = Panel(
            table,
            border_style="bright_green",
            padding=(1, 1),
            width=75
        )
        self.console.print(panel, justify="center")