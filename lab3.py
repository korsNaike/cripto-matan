"""
Программный продукт построения всех примитивов заданного поля GF(2n).
Указывает все промежуточные результаты, то есть
- первичный перебор с указанием проверенных элементов поля и поянением, почему они не примитивы;
- вывод всех примитивов с указанием степеней образующего элемента.
"""


def gf_mul(a, b, poly, n):
    """
    Умножение a и b в GF(2^n) с приведением по модулю неприводимого многочлена poly.
    Элементы представлены как целые числа, биты которых являются коэффициентами многочлена.
    """
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        # Если степень a стала равной n (то есть установлен бит с номером n),
        # выполняем редукцию по полиному
        if a & (1 << n):
            a ^= poly
    return result


def gf_pow(a, exponent, poly, n):
    """
    Возведение элемента a в степень exponent в поле GF(2^n)
    """
    result = 1
    for _ in range(exponent):
        result = gf_mul(result, a, poly, n)
    return result


def get_divisors(num):
    """
    Вычисляет все собственные делители числа num (от 1 до num-1)
    """
    divs = []
    for i in range(1, num):
        if num % i == 0:
            divs.append(i)
    return divs


def main():
    # Ввод параметров поля GF(2^n)
    try:
        n = int(input("Введите значение n для поля GF(2^n): "))
    except ValueError:
        print("Ошибка: введите целое число для n.")
        return

    # Запрос ввода неприводимого многочлена в виде строки (например, для x^4+x+1 введите 10011)
    poly_str = input(
        "Введите неприводимый многочлен для GF(2^n) в виде двоичной строки (например, для x^4+x+1 введите 10011): ").strip()
    if len(poly_str) != n + 1:
        print(f"Предупреждение: для неприводимого многочлена степени {n} ожидается {n + 1} символов.")
    try:
        poly = int(poly_str, 2)
    except ValueError:
        print("Ошибка: неверный формат многочлена. Используйте только 0 и 1.")
        return

    order = (1 << n) - 1  # Порядок мультипликативной группы: 2^n - 1
    print("\nПостроение поля GF(2^{}) с неприводимым многочленом {} (в двоичном виде: {})".format(n, poly, poly_str))
    print("Порядок мультипликативной группы: {}".format(order))

    # Вычисляем собственные делители порядка (без учета самого порядка)
    divisors = get_divisors(order)
    print("Собственные делители порядка: {}".format(divisors))
    print("=" * 60)

    primitive_elements = []

    # Перебираем все ненулевые элементы поля (от 1 до 2^n-1)
    for candidate in range(1, order + 1):
        print("\nПроверка элемента: {} (полиномиальное представление: {})".format(candidate,
                                                                                  format(candidate, '0{}b'.format(n))))
        is_primitive = True
        # Для каждого собственного делителя d проверяем, что candidate^d != 1
        for d in divisors:
            power = gf_pow(candidate, d, poly, n)
            print("  Вычисление: {}^{} = {} (в двоичном виде: {})".format(candidate, d, power,
                                                                          format(power, '0{}b'.format(n))), end=' ')
            if power == 1:
                print("=> равен 1")
                print("  Следовательно, элемент {} не является примитивным, т.к. его порядок делится на {}.".format(
                    candidate, d))
                is_primitive = False
                break
            else:
                print("=> не равен 1")
        if is_primitive:
            print("Элемент {} является примитивным.".format(candidate))
            primitive_elements.append(candidate)
        print("-" * 60)

    # Вывод всех найденных примитивных элементов
    print("\nНайденные примитивные элементы:")
    for pe in primitive_elements:
        print("Элемент {} (в двоичном виде: {})".format(pe, format(pe, '0{}b'.format(n))))

    # Если найден хотя бы один примитивный элемент, выбираем первый как генератор
    if primitive_elements:
        generator = primitive_elements[0]
        print("\nВыбран генератор: {} (в двоичном виде: {})".format(generator, format(generator, '0{}b'.format(n))))
        # Вычисляем дискретные логарифмы относительно выбранного генератора
        exp_dict = {}
        current = 1
        for exp in range(order):
            exp_dict[current] = exp
            current = gf_mul(current, generator, poly, n)

        print("\nДискретные логарифмы примитивных элементов относительно генератора:")
        for pe in primitive_elements:
            exponent = exp_dict.get(pe, None)
            if exponent is not None:
                print("Элемент {} равен ({}^{})".format(pe, generator, exponent))
            else:
                print("Элемент {} не найден в последовательности степеней генератора".format(pe))
    else:
        print("Примитивные элементы не найдены.")


if __name__ == "__main__":
    main()
