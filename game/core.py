from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from game.economy import Economy
from game.bank import Bank
from game.cafe import Cafe
from game.products import Products
from game.staff import Staff
from game.pets import Pets
from game.events import Events
from game.upgrades import Upgrades
from game.save_load import save_game_encrypted, load_game_encrypted
from ui.interface import GameMenu
from tutorials.tutorial import start_tutorial
from data.config import LOCATIONS
from utils.helpers import load_json

console = Console()

class GameCore:
    def __init__(self):
        self.day = 1
        self.money = 1000
        self.reputation = 50
        self.comfort = 50
        self.staff_count = 1
        self.staff_efficiency = 1.0
        self.cafe_name = "Kohihausu"
        self.clients = 10
        self.is_running = False
        self.difficulty = "Medium"
        self.bankruptcy_days = 0
        self.prestige_level = 0
        self.economy = Economy(self)
        self.bank = Bank(self)
        self.cafe = Cafe(self)
        self.products = Products(self)
        self.staff = Staff(self)
        self.pets = Pets(self)
        self.events = Events(self)
        self.upgrades = Upgrades(self)
        self.menu = GameMenu(self, console)

    def start_new_game(self):
        self.day = 1
        self.money = 1000
        self.reputation = 50
        self.comfort = 50
        self.staff_count = 1
        self.staff_efficiency = 1.0
        self.clients = 10
        self.bankruptcy_days = 0
        self.prestige_level = 0
        if not hasattr(self, 'skip_tutorial') or not self.skip_tutorial:
            start_tutorial(self)
        console.print(Panel(
            f"Добро пожаловать в '{self.cafe_name}'! День {self.day} начинается ☕🐾",
            style="bold magenta",
            border_style="green",
            padding=(1, 2)
        ))
        self.is_running = True
        self.game_loop()

    def load_game(self):
        console.clear()
        console.print(Panel(
            Text("Загрузка игры", style="bold magenta"),
            border_style="bright_green",
            padding=(1, 2),
            width=40
        ), justify="center")
        state = load_game_encrypted()
        if state:
            self.day = state.get("day", 1)
            self.money = state.get("money", 1000)
            self.reputation = state.get("reputation", 50)
            self.comfort = state.get("comfort", 50)
            self.staff_count = state.get("staff_count", 1)
            self.staff_efficiency = state.get("staff_efficiency", 1.0)
            self.cafe_name = state.get("cafe_name", "Kohihausu")
            self.clients = state.get("clients", 10)
            self.difficulty = state.get("difficulty", "Medium")
            self.bankruptcy_days = state.get("bankruptcy_days", 0)
            self.prestige_level = state.get("prestige_level", 0)
            self.apply_name_bonuses()
            console.print(Panel(
                Text.assemble(("Добро пожаловать обратно в ", "green"), (f"'{self.cafe_name}'! ", "bold magenta"), (f"День {self.day} ☕🐾", "cyan")),
                style="white",
                border_style="bright_green",
                padding=(1, 2),
                width=50
            ), justify="center")
            self.is_running = True
            self.game_loop()
        else:
            console.print(Panel(
                Text("Не удалось загрузить игру. Начните новую!", style="red"),
                border_style="bright_red",
                padding=(1, 2),
                width=40
            ), justify="center")
            console.input("[yellow]Нажмите Enter для возврата...[/]")

    def save_game(self):
        state = {
            "day": self.day,
            "money": self.money,
            "reputation": self.reputation,
            "comfort": self.comfort,
            "staff_count": self.staff_count,
            "staff_efficiency": self.staff_efficiency,
            "cafe_name": self.cafe_name,
            "clients": self.clients,
            "difficulty": self.difficulty,
            "bankruptcy_days": self.bankruptcy_days,
            "prestige_level": self.prestige_level
        }
        save_game_encrypted(state)
        console.print(f"[green]Игра сохранена на день {self.day}.[/]", justify="center")

    def game_loop(self):
        while self.is_running:
            console.clear()
            self.display_status()
            self.menu.display()
            action = console.input("[bold yellow]Что делать?[/] (1-13): ").strip()
            if action == "1":
                self.next_day()
            elif action == "2":
                self.save_game()
            elif action == "3":
                self.shop_menu()
            elif action == "4":
                self.finance_menu()
            elif action == "5":
                self.staff_menu()
            elif action == "6":
                self.pets_menu()
            elif action == "7":
                self.products_menu()
            elif action == "8":
                self.upgrades_menu()
            elif action == "9":
                self.location_menu()
            elif action == "10":
                self.franchise_menu()
            elif action == "11":
                self.marketing_menu()
            elif action == "12":
                self.prestige_menu()
            elif action == "13":
                self.is_running = False
                console.clear()
                console.print("[italic cyan]Выход в главное меню.[/]", justify="center")
            else:
                console.print("[red]Неверный выбор![/]", justify="center")

    def next_day(self):
        self.day += 1
        console.print("[cyan]Утро: Кофейня открывается![/]", justify="center")
        console.print("[cyan]Обед: Пик заказов![/]", justify="center")
        self.products.daily_sales()
        console.print("[cyan]Вечер: Подсчёт дня.[/]", justify="center")
        self.economy.daily_summary()
        self.bank.daily_update()
        self.cafe.daily_cost()
        self.staff.daily_salary()
        self.pets.daily_care()
        self.events.trigger_event()
        console.print("[cyan]Ночь: Время для улучшений.[/]", justify="center")
        self.economy.set_seasonal_event()
        self.check_bankruptcy()

    def display_status(self):
        from ui.ascii_art import get_cafe_art
        console.print(get_cafe_art(self.cafe_name, self.day), justify="center")
        table = Table(box=None, show_header=True, header_style="bold cyan")
        table.add_column("Показатель", style="cyan", width=15)
        table.add_column("Значение", style="magenta", justify="right", width=15)
        table.add_row("День", f"{self.day}")
        table.add_row("Деньги", f"${self.money} 💰")
        table.add_row("Репутация", f"{self.reputation}%")
        table.add_row("Комфорт", f"{self.comfort}%")
        table.add_row("Клиенты", f"{self.clients}")
        table.add_row("Персонал", f"{self.staff_count} 🐾")
        table.add_row("Эффективность", f"{self.staff_efficiency:.1f}")
        table.add_row("Филиалы", f"{self.economy.franchises}")
        table.add_row("Сложность", f"{self.difficulty}")
        table.add_row("Престиж", f"{self.prestige_level}")
        if self.bankruptcy_days > 0:
            table.add_row("До банкротства", f"{3 - self.bankruptcy_days} дней", style="red")
        panel = Panel(
            table,
            title=Text(f"Кофейный дом '{self.cafe_name}' ☕", style="bold magenta"),
            subtitle=Text(f"Локация: {self.cafe.location}", style="italic cyan"),
            border_style="bright_green",
            style="white",
            padding=(1, 2),
            width=40
        )
        console.print(panel, justify="center")

    def check_bankruptcy(self):
        if self.money < 0:
            self.bankruptcy_days += 1
            self.money = 0
            console.print(f"[red]Ваши финансы исчерпаны! Осталось {3 - self.bankruptcy_days} дней до банкротства.[/]", justify="center")
            if self.bankruptcy_days >= 3:
                console.clear()
                console.print(Panel(
                    f"Кофейня '{self.cafe_name}' обанкротилась на {self.day}-й день. Игра окончена!",
                    style="bold red",
                    border_style="red",
                    padding=(1, 2)
                ))
                self.is_running = False
        else:
            if self.bankruptcy_days > 0:
                console.print("[green]Финансы восстановлены! Статус предбанкротства снят.[/]", justify="center")
            self.bankruptcy_days = 0

    def shop_menu(self):
        console.clear()
        self.menu.display_shop()
        choice = console.input("[bold yellow]Введите название товара для покупки (или 'назад'): [/]").strip()
        if choice.lower() != "назад":
            items = self.upgrades.load_items()
            for category, items_dict in items.items():
                if choice in items_dict:
                    item = items_dict[choice]
                    cost = self.calculate_dynamic_cost(item["base_cost"])
                    self.upgrades.buy_upgrade(choice, cost, item["bonus_type"], item["bonus_value"])
                    break
            else:
                console.print("[red]Товар не найден![/]", justify="center")

    def finance_menu(self):
        console.clear()
        table = Table(title="Финансы 💰", box=None)
        table.add_column("Действие", style="cyan")
        table.add_column("Сумма", style="yellow")
        table.add_row("Текущий баланс", f"${self.money}")
        table.add_row("Кредит", f"${self.bank.loan}")
        table.add_row("Депозит", f"${int(self.bank.deposit)}")
        console.print(table)
        action = console.input(
            "[bold yellow]Выберите: [/]1 - Взять кредит, 2 - Погасить кредит, 3 - Сделать депозит, 4 - Снять депозит, 5 - Назад: "
        ).strip()
        if action == "1":
            amount = int(console.input("[yellow]Сумма кредита: [/]").strip())
            self.bank.take_loan(amount)
        elif action == "2":
            amount = int(console.input("[yellow]Сумма погашения: [/]").strip())
            self.bank.repay_loan(amount)
        elif action == "3":
            amount = int(console.input("[yellow]Сумма депозита: [/]").strip())
            self.bank.make_deposit(amount)
        elif action == "4":
            self.bank.withdraw_deposit()
        elif action == "5":
            pass

    def staff_menu(self):
        console.clear()
        table = Table(title="Персонал 🐾", box=None)
        table.add_column("Роль", style="cyan")
        table.add_column("Количество", style="yellow")
        table.add_column("Навык", style="green")
        table.add_column("Мораль", style="magenta")
        for role, data in self.staff.staff.items():
            table.add_row(role, str(data["count"]), f"{data['skill']:.1f}", f"{data['morale']}%")
        console.print(table)
        action = console.input(
            "[bold yellow]Выберите: [/]1 - Нанять, 2 - Уволить, 3 - Повысить мораль, 4 - Назад: "
        ).strip()
        if action == "1":
            role = console.input("[yellow]Роль: [/]").strip()
            count = int(console.input("[yellow]Количество: [/]").strip())
            staff_data = self.staff.load_staff()
            if role in staff_data:
                cost = self.calculate_staff_cost(staff_data[role]["base_salary"], count)
                self.staff.hire(role, count, cost, staff_data[role]["skill"])
        elif action == "2":
            role = console.input("[yellow]Роль: [/]").strip()
            count = int(console.input("[yellow]Количество: [/]").strip())
            self.staff.fire(role, count)
        elif action == "3":
            amount = int(console.input("[yellow]На сколько повысить мораль (в %)? [/]").strip())
            self.staff.boost_morale(amount)
        elif action == "4":
            pass

    def pets_menu(self):
        console.clear()
        table = Table(title="Питомцы 🐾", box=None)
        table.add_column("Имя", style="cyan")
        table.add_column("Бонус", style="green")
        for name, data in self.pets.pets.items():
            table.add_row(name, f"{data['bonus_type']} +{data['bonus']}")
        console.print(table)
        action = console.input("[bold yellow]Купить питомца (введите имя или 'назад'): [/]").strip()
        if action.lower() != "назад":
            pets_data = self.pets.load_pets()
            if action in pets_data:
                pet = pets_data[action]
                cost = self.calculate_dynamic_cost(pet["base_cost"])
                self.pets.buy_pet(action, cost, pet["bonus_value"])
        else:
            pass

    def products_menu(self):
        console.clear()
        table = Table(title="Ассортимент ☕", box=None)
        table.add_column("Название", style="cyan")
        table.add_column("Цена", style="yellow")
        for name, data in self.products.menu.items():
            table.add_row(name, f"${data['price']}")
        console.print(table)
        action = console.input("[bold yellow]Добавить продукт (введите название или 'назад'): [/]").strip()
        if action.lower() != "назад":
            recipes = self.products.load_recipes()
            if action in recipes["drinks"]:
                recipe = recipes["drinks"][action]
                cost = self.calculate_product_cost(recipe["base_cost"])
                self.products.add_product(action, recipe["base_price"] * (1 + self.day / 100), cost)
            elif action in recipes["desserts"]:
                recipe = recipes["desserts"][action]
                cost = self.calculate_product_cost(recipe["base_cost"])
                self.products.add_product(action, recipe["base_price"] * (1 + self.day / 100), cost)
        else:
            pass

    def upgrades_menu(self):
        console.clear()
        self.menu.display_shop()
        choice = console.input("[bold yellow]Введите название улучшения или 'ремонт' (или 'назад'): [/]").strip()
        if choice.lower() == "ремонт":
            amount = int(console.input("[yellow]На сколько % отремонтировать оборудование? [/]").strip())
            self.economy.repair_equipment(amount)
        elif choice.lower() != "назад":
            items = self.upgrades.load_items()
            for category, items_dict in items.items():
                if choice in items_dict:
                    item = items_dict[choice]
                    cost = self.calculate_dynamic_cost(item["base_cost"])
                    self.upgrades.buy_upgrade(choice, cost, item["bonus_type"], item["bonus_value"])
                    break
            else:
                console.print("[red]Улучшение не найдено![/]", justify="center")

    def location_menu(self):
        console.clear()
        table = Table(title="Локации 🌍", box=None)
        table.add_column("Название", style="cyan")
        table.add_column("Стоимость", style="yellow")
        for loc, data in LOCATIONS.items():
            cost = self.calculate_dynamic_cost(data["base_cost"])
            table.add_row(loc, f"${cost}")
        console.print(table)
        choice = console.input("[bold yellow]Выберите локацию (или 'назад'): [/]").strip()
        if choice.lower() != "назад" and choice in LOCATIONS:
            cost = self.calculate_dynamic_cost(LOCATIONS[choice]["base_cost"])
            self.cafe.change_location(choice, cost)

    def franchise_menu(self):
        console.clear()
        console.print(f"[cyan]Текущие филиалы: {self.economy.franchises}[/]", justify="center")
        action = console.input("[bold yellow]1 - Открыть филиал, 2 - Назад: [/]").strip()
        if action == "1":
            self.economy.add_franchise()
        elif action == "2":
            pass

    def marketing_menu(self):
        console.clear()
        table = Table(title="Маркетинг 📣", box=None)
        table.add_column("Кампания", style="cyan")
        table.add_column("Стоимость", style="yellow")
        table.add_column("Эффект", style="green")
        marketing = self.upgrades.load_marketing()
        for name, data in marketing.items():
            cost = self.calculate_dynamic_cost(data["base_cost"])
            table.add_row(name, f"${cost}", f"{data['bonus_type']} +{data['bonus_value']}")
        console.print(table)
        choice = console.input("[bold yellow]Выберите кампанию (или 'назад'): [/]").strip()
        if choice.lower() != "назад":
            marketing = self.upgrades.load_marketing()
            if choice in marketing:
                item = marketing[choice]
                cost = self.calculate_dynamic_cost(item["base_cost"])
                self.upgrades.buy_upgrade(choice, cost, item["bonus_type"], item["bonus_value"])

    def prestige_menu(self):
        console.clear()
        console.print(f"[cyan]Текущий уровень престижа: {self.prestige_level}[/]", justify="center")
        console.print(f"[yellow]Престиж позволяет начать игру заново с бонусом к доходу (+{self.prestige_level * 10}%).[/]", justify="center")
        if self.day >= 100 and self.money >= 100000:
            action = console.input("[bold yellow]1 - Совершить престиж, 2 - Назад: [/]").strip()
            if action == "1":
                self.prestige_level += 1
                self.money = 1000 * (1 + self.prestige_level * 0.1)
                self.day = 1
                self.reputation = 50
                self.comfort = 50
                self.clients = 10
                self.staff_count = 1
                self.staff_efficiency = 1.0
                self.economy.franchises = 0
                self.bank.loan = 0
                self.bank.deposit = 0
                self.products.menu = {}
                self.pets.pets = {}
                self.staff.staff = {"Бариста": {"count": 1, "skill": 1.0, "salary": 100, "morale": 100}}
                console.print(f"[green]Престиж совершён! Новый уровень: {self.prestige_level}. Игра перезапущена с бонусом.[/]", justify="center")
            elif action == "2":
                pass
        else:
            console.print("[red]Для престижа нужно: День >= 100 и Деньги >= $100,000[/]", justify="center")
            console.input("[yellow]Нажмите Enter для возврата...[/]")

    def calculate_dynamic_cost(self, base_cost):
        """Динамическая цена для улучшений, локаций и т.д."""
        return int(base_cost * (1 + self.day / 50) * (1 + self.reputation / 100) * (1 + self.economy.franchises * 0.2) * (1 + self.prestige_level * 0.5))

    def calculate_staff_cost(self, base_salary, count):
        """Динамическая цена найма персонала."""
        return int(base_salary * count * (1 + self.day / 100) * (1 + self.staff_count / 10) * (1 + self.prestige_level * 0.3))

    def calculate_product_cost(self, base_cost):
        """Динамическая цена добавления продуктов."""
        return int(base_cost * (1 + self.day / 75) * (1 + self.clients / 50) * (1 + self.prestige_level * 0.2))

    def apply_name_bonuses(self):
        name = self.cafe_name.lower()
        bad_names = load_json("data/bad_name.json").get("bad_names", [])
        if name in bad_names:
            self.clients = int(self.clients * 0.8)
            self.reputation -= 10
            console.print("[red]Ой! Это название слишком известное. Клиенты и репутация пострадали (-20% клиентов, -10% репутации).[/]", justify="center")
        else:
            if 3 <= len(name) <= 5:
                self.clients = int(self.clients * 1.1)
                console.print("[green]Отличное короткое название! +10% клиентов[/]", justify="center")
            elif len(name) < 3:
                self.clients = int(self.clients * 0.85)
                console.print("[red]Слишком короткое название. -15% клиентов[/]", justify="center")
            elif len(name) > 10:
                self.clients = int(self.clients * 0.75)
                console.print("[red]Слишком длинное название. -25% клиентов[/]", justify="center")
            if "кофе" in name or "кот" in name:
                self.reputation += 5
                console.print("[green]'Кофе' или 'кот' в названии! +5% репутации[/]", justify="center")
            console.print("[green]Уникальное название! +10% чаевых[/]", justify="center")