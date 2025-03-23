from rich.console import Console
from utils.helpers import load_json

console = Console()

class Products:
    def __init__(self, game_core):
        self.game = game_core
        self.menu = {}

    def add_product(self, name, price, cost):
        if self.game.money >= cost:
            self.game.money -= cost
            self.menu[name] = {"price": price, "cost": cost}
            console.print(f"[green]Добавлен продукт '{name}' за ${cost}. Цена продажи: ${price}[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для добавления продукта![/]", justify="center")

    def daily_sales(self):
        total_income = 0
        for name, data in self.menu.items():
            sales = int(self.game.clients * (self.game.reputation / 100) * (data["price"] / 10))
            total_income += sales
        self.game.money += total_income
        console.print(f"[green]Продажи за день: ${total_income}[/]", justify="center")

    def load_recipes(self):
        return load_json("data/recipes.json")