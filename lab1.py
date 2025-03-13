import math

def extended_gcd_with_steps(a, b):
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    steps.append(f"Инициализация: a = {old_r}, b = {r}, коэффициенты x = {old_s}, y = {old_t}")
    while r != 0:
        quotient = old_r // r
        steps.append(f"Делим {old_r} на {r}, получаем частное {quotient}")
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
        steps.append(f"Обновленные значения: a = {old_r}, b = {r}, коэффициенты x = {old_s}, y = {old_t}")
    steps.append(f"НОД({a}, {b}) = {old_r}, коэффициенты x = {old_s}, y = {old_t}")
    return old_r, old_s, old_t, steps

def euler_phi_with_steps(n):
    steps = []
    if n <= 0:
        return 0, steps, {}
    original_n = n
    result = n
    factors = {}
    i = 2
    steps.append(f"Начало вычисления функции Эйлера для n = {n}")
    while i * i <= n:
        if n % i == 0:
            count = 0
            while n % i == 0:
                count += 1
                n = n // i
            factors[i] = count
            steps.append(f"Найден простой делитель {i} степени {count}, новый n = {n}")
        i += 1
    if n > 1:
        factors[n] = 1
        steps.append(f"Найден простой делитель {n} степени 1")
    for p in factors:
        result = result // p * (p - 1)
        steps.append(f"Умножение на (1 - 1/{p}): результат = {result}")
    steps.append(f"Функция Эйлера φ({original_n}) = {result}")
    return result, steps, factors

def modular_exponentiation_with_steps(base, exponent, mod):
    steps = []
    result = 1
    base = base % mod
    steps.append(f"Начальные значения: base = {base}, exponent = {exponent}, mod = {mod}")
    while exponent > 0:
        if exponent % 2 == 1:
            old_result = result
            result = (result * base) % mod
            steps.append(f"exponent = {exponent} нечетное, умножаем результат {old_result} на {base} mod {mod} = {result}")
        else:
            steps.append(f"exponent = {exponent} четное, пропускаем умножение")
        exponent = exponent // 2
        old_base = base
        base = (base * base) % mod
        steps.append(f"Квадратируем base: {old_base}^2 mod {mod} = {base}, новый exponent = {exponent}")
    steps.append(f"Результат возведения в степень: {result}")
    return result, steps

def solve_congruence():
    a = int(input("Введите коэффициент a: "))
    b = int(input("Введите коэффициент b: "))
    m = int(input("Введите модуль m: "))

    if m <= 0:
        print("Модуль m должен быть положительным.")
        return

    d = math.gcd(a, m)

    if (b % d) != 0:
        print(f"\nСравнение {a}x ≡ {b} (mod {m}) не имеет решений, так как НОД({a}, {m}) = {d} не делит {b}.")
        return

    print(f"\nСравнение {a}x ≡ {b} (mod {m}) имеет решения, так как НОД({a}, {m}) = {d} делит {b}.")
    print(f"Количество решений: {d}\n")

    # Метод 1: Расширенный алгоритм Евклида
    print("="*50)
    print("Метод 1: Расширенный алгоритм Евклида")
    gcd_val, x_coeff, y_coeff, euclid_steps = extended_gcd_with_steps(a, m)
    print("\nШаги расширенного алгоритма Евклида:")
    for step in euclid_steps:
        print(step)

    x0 = (x_coeff * (b // d)) % (m // d)
    solutions_euclid = [(x0 + k * (m // d)) % m for k in range(d)]

    print(f"\nРешение с использованием расширенного алгоритма Евклида:")
    print(f"Частное решение x0 = {x_coeff} * ({b} // {d}) mod ({m} // {d}) = {x0} mod {m//d}")
    print(f"Все решения по модулю {m}: {sorted(solutions_euclid)}\n")

    # Метод 2: Формула Эйлера
    print("="*50)
    print("Метод 2: Формула Эйлера")
    a_prime = a // d
    b_prime = b // d
    m_prime = m // d

    print(f"После сокращения на d={d} получаем сравнение: {a_prime}x ≡ {b_prime} (mod {m_prime})")

    # Вычисляем φ(m_prime)
    phi, phi_steps, factors = euler_phi_with_steps(m_prime)
    print("\nШаги вычисления функции Эйлера:")
    for step in phi_steps:
        print(step)

    # Вычисляем a_prime^(phi-1) mod m_prime
    exponent = phi - 1
    pow_result, pow_steps = modular_exponentiation_with_steps(a_prime, exponent, m_prime)
    print("\nШаги возведения в степень по модулю:")
    for step in pow_steps:
        print(step)

    x0_euler = (b_prime * pow_result) % m_prime
    solutions_euler = [(x0_euler + k * m_prime) % m for k in range(d)]

    print(f"\nРешение с использованием формулы Эйлера:")
    print(f"x0 = {b_prime} * {a_prime}^{phi-1} mod {m_prime} = {x0_euler} mod {m_prime}")
    print(f"Все решения по модулю {m}: {sorted(solutions_euler)}\n")

    # Проверка совпадения решений
    if set(solutions_euclid) == set(solutions_euler):
        print("Оба метода дали одинаковые решения.")
    else:
        print("Внимание: методы дали разные решения. Возможна ошибка в вычислениях.")
    print("="*50)

if __name__ == "__main__":
    solve_congruence()