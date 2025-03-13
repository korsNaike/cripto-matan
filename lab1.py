"""
Программный продукт решения сравнения первой степени двумя способами с указанием всех промежуточных шагов вычисления
(текущее значение коэффициентов расширенном алгоритме Евклида и текущее значение степеней в формуле Эйлера).
"""

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида с выводом шагов."""
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    steps.append(f"Начальные значения: r={old_r}, s={old_s}, t={old_t}")
    steps.append(f"Обновляем: r={r}, s={s}, t={t}")

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

        steps.append(
            f"Шаг: q={quotient}, r={old_r}, s={old_s}, t={old_t}\n"
            f"Обновляем: r={r if r != 0 else 'Stop'}, s={s}, t={t}"
        )

    return old_r, old_s, old_t, steps


def euler_phi(n):
    """Вычисление функции Эйлера φ(n) с выводом шагов."""
    if n < 1:
        return 0, []
    steps = []
    result = n
    i = 2
    steps.append(f"Начальное значение φ({n}) = {n}")
    while i * i <= n:
        if n % i == 0:
            steps.append(f"Делитель {i} найден")
            while n % i == 0:
                n = n // i
                steps.append(f"Делим {n * i} на {i} → {n}")
            result -= result // i
            steps.append(f"Обновляем φ = {result}")
        i += 1
    if n > 1:
        result -= result // n
        steps.append(f"Учитываем оставшийся делитель {n} → φ = {result}")
    return result, steps


def solve_congruence():
    a = int(input("Введите коэффициент a: "))
    b = int(input("Введите коэффициент b: "))
    m = int(input("Введите модуль m: "))

    # Проверка на m > 0
    if m <= 0:
        print("Ошибка: модуль m должен быть положительным числом!")
        return

    # Шаг 1: Проверка существования решений
    d, x_egcd, y_egcd, steps_egcd = extended_gcd(a, m)
    print("\n[Расширенный алгоритм Евклида]")
    print("\n".join(steps_egcd))

    if b % d != 0:
        print(f"\nРешений нет: {d} (НОД) не делит {b}")
        return

    # Преобразование уравнения
    a //= d
    b //= d
    m_new = m // d

    # Метод 1: Расширенный алгоритм Евклида
    x0 = (x_egcd * (b // d)) % m_new
    solutions_egcd = [(x0 + k * m_new) % m for k in range(d)]

    # Метод 2: Формула Эйлера
    phi, steps_phi = euler_phi(m_new)
    print("\n[Функция Эйлера]")
    print("\n".join(steps_phi))

    if phi == 0:
        print("Невозможно применить формулу Эйлера")
        return

    a_inv = pow(a, phi - 1, m_new)
    x_euler = (b * a_inv) % m_new
    solutions_euler = [(x_euler + k * m_new) % m for k in range(d)]

    # Вывод результатов
    print("\nРешения:")
    print(f"1. Метод расширенного алгоритма Евклида: {solutions_egcd}")
    print(f"2. Метод формулы Эйлера: {solutions_euler}")


if __name__ == "__main__":
    solve_congruence()