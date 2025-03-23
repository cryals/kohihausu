from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def start_tutorial(game):
    console.clear()
    console.print(Panel(
        Text.assemble(("Добро пожаловать в туториал ", "bold green"), ("Kohihausu! ☕🐾", "bold magenta")),
        style="bold green",
        border_style="yellow",
        padding=(1, 2)
    ))
    console.print("Ты — новый владелец кофейни в Зверополисе. Давай научимся управлять ей!", justify="center")
    console.input("[yellow]Нажмите Enter, чтобы начать...[/]")

    console.clear()
    console.print(Panel("Шаг 1: Назови свою кофейню", style="cyan", border_style="green", padding=(1, 2)))
    console.print(f"Твоя кофейня уже называется '{game.cafe_name}'. Название даёт бонусы!", justify="center")
    console.input("[yellow]Нажмите Enter...[/]")

    console.clear()
    console.print(Panel("Шаг 2: Первый день работы", style="cyan", border_style="green", padding=(1, 2)))
    console.print("Каждый день ты зарабатываешь деньги от продаж. Нажми '1' в меню, чтобы начать день!", justify="center")
    game.next_day()
    console.input("[yellow]Нажмите Enter...[/]")

    console.clear()
    console.print(Panel("Шаг 3: Магазин", style="cyan", border_style="green", padding=(1, 2)))
    console.print("В магазине можно купить улучшения. Попробуй ввести 'Кофемашина' или 'Диваны'!", justify="center")
    game.shop_menu()
    console.input("[yellow]Нажмите Enter...[/]")

    console.clear()
    console.print(Panel("Шаг 4: Финансы", style="cyan", border_style="green", padding=(1, 2)))
    console.print("Возьми кредит (1) или сделай депозит (3), если нужно больше денег.", justify="center")
    game.finance_menu()
    console.input("[yellow]Нажмите Enter...[/]")

    console.clear()
    console.print(Panel("Шаг 5: Избегай банкротства", style="cyan", border_style="green", padding=(1, 2)))
    console.print("Если деньги закончатся, у тебя будет 3 дня, чтобы их заработать, иначе — банкротство!", justify="center")
    console.input("[yellow]Нажмите Enter...[/]")

    console.clear()
    console.print(Panel(
        Text.assemble(("Ты готов стать кофейным королём ", "bold green"), ("Зверополиса!", "bold magenta")),
        style="bold green",
        border_style="yellow",
        padding=(1, 2)
    ))
    console.print("Исследуй меню, нанимай персонал, покупай питомцев и развивай кофейню!", justify="center")
    console.input("[yellow]Нажмите Enter, чтобы начать игру...[/]")