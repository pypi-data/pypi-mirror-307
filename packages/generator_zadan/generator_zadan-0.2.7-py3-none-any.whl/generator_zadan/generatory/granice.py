import random

import sympy as sp
from sympy.abc import n, x


def granica_ciagu(typ: int = 0):
    if typ == 0:
        liczby = (-3, -2, -1, 0, 0, 0, 1, 2, 3, 4, 5)
        while True:
            a, b, c, d, e, f, g, h, i, j = [random.choice(liczby) for _ in range(10)]
            if (a != d or b != e or c != f) and (a != 0 or b != 0 or c != 0 or d != 0) and (
                    e != 0 or f != 0 or j != 0):
                break
        granica = sp.limit(
            (a * n ** 3 + b * n ** 2 + c * n + d + i * n ** 5) / (e * n ** 3 + e * n ** 2 + f * n + g + j * n ** 5),
            n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}}'
                f' {sp.latex((a * n ** 3 + b * n ** 2 + c * n + d + i * n ** 5) / (e * n ** 3 + e * n ** 2 + f * n + g + j * n ** 5))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')

    if typ == 1:
        liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
        gora = random.choice((0, 1))
        while True:
            a, b, c, d, e = [random.choice(liczby) for _ in range(5)]
            if gora == 1:
                granica = sp.limit((sp.sqrt(a * n ** 2 + b * n + c) / (d * n + e)), n, sp.oo)
                if granica.is_real:
                    return (f'Obliczyć granicę\n'
                            f'\t\\[\n'
                            f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex((sp.sqrt(a * n ** 2 + b * n + c) / (d * n + e)))} \n'
                            f'\t\\]\n',
                            f'${sp.latex(granica)}$')
            else:
                granica = sp.limit((d * n + e) / (sp.sqrt(a * n ** 2 + b * n + c)), n, sp.oo)
                if granica.is_real:
                    return (f'Obliczyć granicę\n'
                            f'\t\\[\n'
                            f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex((d * n + e) / (sp.sqrt(a * n ** 2 + b * n + c)))} \n'
                            f'\t\\]\n',
                            f'${sp.latex(granica)}$')

    if typ == 2:
        liczby = (-3, -2, -1, 1, 2, 3, 4)
        while True:
            a, b, c, d = [random.choice(liczby) for _ in range(4)]
            e, f, g, h = [random.choice((2, 3, 4, 5)) for _ in range(4)]
            if a != b and c != d and e != f and g != h:
                break
        granica = sp.limit((a * e ** n + b * f ** n) / (d * g ** n + e * h ** n), n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex((a * e ** n + b * f ** n) / (d * g ** n + e * h ** n))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')

    if typ == 3:
        liczby = (-3, -2, -1, 0, 1, 2, 3, 4, 5)
        while True:
            a, b, c, d, e, f = [random.choice(liczby) for _ in range(6)]
            if a == b > 0 and (c != d or e != f):
                break
        granica = sp.limit(sp.sqrt(a * n ** 2 + c * n + e) - sp.sqrt(b * n ** 2 + d * n + f), n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} \\left({sp.latex(sp.sqrt(a * n ** 2 + c * n + e) - sp.sqrt(b * n ** 2 + d * n + f))} \\right) \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 4:
        liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
        while True:
            a, b, d, e, f = [random.choice(liczby) for _ in range(5)]
            c = a
            if b != d and e != 0:
                break
        granica = sp.limit(((a * n + b) / (c * n + d)) ** (e * n + f), n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex(((a * n + b) / (c * n + d)) ** (e * n + f))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
def granica_funkcji(typ: int = 0):
    if typ == 0:
        a, b, c = [random.choice((-2, -1, 1, 2, 3, 4)) for _ in range(3)]
        a = sp.Abs(a)
        granica = sp.limit((a - sp.sqrt(a ** 2 - b * x)) / (c * x), x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f' {sp.latex((a - sp.sqrt(a**2-b*x))/(c*x))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')

if __name__ == "__main__":
    polecenie, rozwiazanie = granica_funkcji(typ=0)
    print(polecenie, '\n', rozwiazanie)

    res2 = sp.limit(1 / x ** 2 - 1 / (x * sp.sin(x)), x, 0)

    print(res2)

    for i in range(1):
        granica = sp.limit(((sp.E ** (-2 / x ** 2)) ** (sp.sin(x ** 2))), x, 0)
        print(sp.latex(granica))
