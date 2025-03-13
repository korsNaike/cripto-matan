"""
Программный продукт нахождения множества
квадратичных вычетов и множества квадратичных невычетов по заданному
простому модулю с пояснением всех промежуточных шагов решения задачи.
"""


def is_prime(n):
    """Проверяет, является ли число n простым."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def calculate_residues_with_steps(p):
    """Вычисляет квадратичные вычеты по модулю p и возвращает шаги вычислений."""
    residues = set()
    steps = []
    for x in range(1, p):
        square = x ** 2
        mod = square % p
        steps.append(f"x = {x}: {x}² mod {p} = {square} mod {p} = {mod}")
        residues.add(mod)
    return sorted(residues), steps


def find_set_quadra():
    # Ввод данных
    p = int(input("Введите простое число p: "))

    if not is_prime(p):
        print("Ошибка: p должно быть простым числом.")
    else:
        residues, steps = calculate_residues_with_steps(p)
        non_residues = sorted(set(range(1, p)) - set(residues))

        print("\nПромежуточные шаги вычисления квадратов по модулю p:")
        for step in steps:
            print(step)

        print("\nМножество квадратичных вычетов по модулю", p, ":", residues)
        print("Множество квадратичных невычетов по модулю", p, ":", non_residues)


if __name__ == "__main__":
    find_set_quadra()