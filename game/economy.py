from rich.console import Console
from data.config import DIFFICULTY_LEVELS
import math

console = Console()

class Economy:
    def __init__(self, game_core):
        self.game = game_core
        self.base_income = DIFFICULTY_LEVELS[self.game.difficulty]["base_income"]
        self.base_expenses = DIFFICULTY_LEVELS[self.game.difficulty]["base_expenses"]
        self.tax_rate = DIFFICULTY_LEVELS[self.game.difficulty]["tax_rate"]
        self.franchises = 0
        self.seasonal_bonus = 0
        self.equipment_condition = 100

    def calculate_income(self):
        income = self.base_income * (1 + self.game.reputation / 100) * \
                 (1 + self.game.comfort / 100) * (math.log(self.game.day + 1)) * \
                 self.game.staff_efficiency * (1 + self.franchises * 0.75) * \
                 (1 + self.seasonal_bonus / 100) * (self.game.clients / 10) * \
                 (self.equipment_condition / 100) * (1 + self.game.prestige_level * 0.1)
        tips = self.calculate_tips(income)
        return int(income + tips)

    def calculate_tips(self, income):
        tips = income * (0.1 + self.game.comfort / 200 + sum(p["bonus"] / 100 for p in self.game.pets.pets.values()) + self.game.prestige_level * 0.05)
        return int(tips)

    def calculate_expenses(self):
        expenses = self.base_expenses * (1 + self.game.day / 30) * \
                   (1 + self.game.staff_count / 5) * (1 + self.franchises) * \
                   (1 + (100 - self.equipment_condition) / 150) * (1 + self.game.prestige_level * 0.2)
        taxes = self.calculate_taxes()
        repair_cost = (100 - self.equipment_condition) * 15
        return int(expenses + taxes + repair_cost)

    def calculate_taxes(self):
        income = self.calculate_income()
        taxes = income * (self.tax_rate + self.game.day / 300 + self.game.prestige_level * 0.01)
        return int(taxes)

    def daily_summary(self):
        self.equipment_condition -= 1 + self.game.day / 100
        if self.equipment_condition < 0:
            self.equipment_condition = 0
        income = self.calculate_income()
        expenses = self.calculate_expenses()
        profit = income - expenses
        if self.game.money + profit < 0:
            self.game.money = 0
        else:
            self.game.money += profit
        console.print(
            f"[green]Доход: ${income}[/] | [red]Расходы: ${expenses}[/] | "
            f"[bold]Прибыль: ${profit}[/] | Баланс: ${self.game.money}",
            justify="center"
        )
        console.print(f"[yellow]Состояние оборудования: {self.equipment_condition}%[/]", justify="center")

    def add_franchise(self):
        cost = 10000 * (self.franchises + 1) * (1 + self.game.day / 50) * (1 + self.game.prestige_level * 0.5)
        if self.game.money >= cost:
            self.game.money -= cost
            self.franchises += 1
            console.print(f"[green]Открыт новый филиал за ${cost}! Всего филиалов: {self.franchises}[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для открытия филиала![/]", justify="center")

    def repair_equipment(self, amount):
        cost = amount * 20 * (1 + self.game.day / 100)
        if self.game.money >= cost:
            self.game.money -= cost
            self.equipment_condition = min(100, self.equipment_condition + amount)
            console.print(f"[green]Оборудование отремонтировано на {amount}% за ${cost}. Состояние: {self.equipment_condition}%[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для ремонта![/]", justify="center")

    def set_seasonal_event(self):
        if self.game.day % 30 == 0:
            self.seasonal_bonus = 25 + self.game.prestige_level * 5
            console.print(f"[green]Сезонное событие: 'Лесной карнавал' — +{self.seasonal_bonus}% дохода на 5 дней![/]", justify="center")
        elif self.game.day % 30 == 5:
            self.seasonal_bonus = 0