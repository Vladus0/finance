import json
import argparse


def add_expense(budget, expenses, description, amount):
    if budget < amount:
        print("Не можем добавить эту трату, кол-во ваших денег не хватает, сначала укажите ваш точный бюджет")
        return budget
    else:
        expenses[description] = amount
        budget -= amount
        return budget


def show_budget_details(first_budget, budget, expenses, added_to_balance):
    print(f"Изначально было деняг: {first_budget}")
    for expense in expenses:
        print(f'{expense}: {expenses[expense]}')
    print(f'Сумма трат: {get_total_expenses(expenses)}')
    print(f'Добавлено на баланс: {added_to_balance}')
    print(f'У вас осталось {budget}')


def get_total_expenses(expenses):
    return sum(expenses.values())


def save_budget_details(first_budget, budget, expenses, filepath):
    budget_statistic = {
        "first_budget": first_budget,
        "initial_budget": budget,
        "expenses": expenses
    }
    with open(filepath, 'w') as file:
        json.dump(budget_statistic, file, ensure_ascii=False)


def load_budget_data(filepath):
    with open(filepath, "r") as file:
        budget_statistic = json.load(file)
        return budget_statistic


def update_budget(budget):
    inital_budget = float(input("Пожалуйста введите кол-во деняг, которое вы хотите добавить: "))
    budget = budget + inital_budget
    return inital_budget, budget


def main():
    parser = argparse.ArgumentParser(description='Эта консольная программа позволяет подсчитывать финансы')
    parser.add_argument(
        '--filepath',
        type=str,
        default="budget_statistic.json",
        help='укажите название файла (default: budget_statistic.json)'
    )
    pars_arg = parser.parse_args()
    filepath = pars_arg.filepath
    print("Добро пожаловать, здесь вы сможете отслеживать ваши финансы")
    added_to_balance = 0
    try:
        budget_statistic = load_budget_data(filepath)
        first_budget = budget_statistic['first_budget']
        budget = budget_statistic['initial_budget']
        expenses = budget_statistic['expenses']
    except (FileNotFoundError, json.JSONDecodeError):
        inital_budget = float(input("Пожалуйста введите имеющиеся у вас кол-во деняг: "))
        budget = inital_budget
        expenses = {}
        first_budget = budget


    while True: 
        print("Что бы вы хотели сделать?\n 1. Добавить траты\n 2. Показать кол-во оставшихся деняг\n 3. Обновить бюджет\n 4. Выйти")
        choose = int(input("Ваш выбор 1/2/3/4: "))
        if choose == 1:
            description = input("Введите описание траты (на что вы потратили деньги): ")
            amount = float(input("Введите кол-во потраченных деняг: "))
            budget = add_expense(budget, expenses, description, amount)
        
        elif choose == 2:
            show_budget_details(first_budget, budget, expenses, added_to_balance)

        elif choose == 3:
            update_budget = update_budget(budget)
            budget = update_budget[1]
            added_to_balance = update_budget[0]

        elif choose == 4:
            save_budget_details(first_budget, budget, expenses, filepath)
            break

if __name__ == "__main__":
    main()