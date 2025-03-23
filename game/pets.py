from rich.console import Console
from utils.helpers import load_json

console = Console()

class Pets:
    def __init__(self, game_core):
        self.game = game_core
        self.pets = {}

    def buy_pet(self, name, cost, bonus):
        from ui.ascii_art import get_pet_art
        if self.game.money >= cost:
            self.game.money -= cost
            self.pets[name] = {"cost": cost, "bonus": bonus, "care_cost": cost // 10}
            self.game.comfort += bonus
            console.print(get_pet_art(name))
            console.print(f"[green]Куплен питомец '{name}' за ${cost}. Комфорт +{bonus}%[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для покупки питомца![/]", justify="center")

    def daily_care(self):
        total_care = sum(p["care_cost"] for p in self.pets.values())
        if self.game.money >= total_care:
            self.game.money -= total_care
            console.print(f"[red]Уход за питомцами: ${total_care}[/]", justify="center")
        else:
            self.game.money = 0  # Не уходим в минус
            console.print(f"[red]Недостаточно денег для ухода за питомцами (${total_care})![/]", justify="center")

    def load_pets(self):
        return load_json("data/pets.json")