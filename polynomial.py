from math import sqrt


class Polynomial:

    def __init__(self, *args):  # инициализия
        if isinstance(args[0], list):  # получили список
            coefficients = args[0]
        elif isinstance(args[0], dict):  # получили словарь
            coefficients = [0 for i in range(max(args[0]) + 1)]
            for key in args[0]:
                coefficients[key] = args[0][key]
        elif isinstance(args[0], Polynomial):  # получили многочлен
            coefficients = args[0].coeffs.copy()
        else:
            coefficients = list(args)
        i = len(coefficients) - 1
        while i > 0 and coefficients[i] == 0:  # убираем нули
            i -= 1
        self.coeffs = coefficients[: i + 1]  # определяем coeffs мн-на

    def __repr__(self):    # выводим коэффициенты
        return 'Polynomial ' + str(self.coeffs)

    def __str__(self):  # выводим сам многочлен
        s = ''
        if len(self.coeffs) == 1:  # если мн-н 0 степени
            return str(self.coeffs[0])
        if abs(self.coeffs[-1]) != 1:  # + 1ое слагаемое
            s += str(self.coeffs[-1])
        if self.coeffs[-1] == -1:
            s += '-'
        s += 'x'
        if len(self.coeffs) > 2:
            s += '^' + str(len(self.coeffs) - 1)
        for i in range(len(self.coeffs) - 2, -1, -1):
            if self.coeffs[i] > 0:   # ставим + или -
                s += ' + '
            if self.coeffs[i] < 0:
                s += ' - '
            if self.coeffs[i] != 0:  # добавяем ненулевое слагаемое
                if abs(self.coeffs[i]) != 1 or i == 0:
                    s += str(abs(self.coeffs[i]))
                if i > 0:
                    s += 'x'
                if i > 1:
                    s += '^' + str(i)
        return s

    def __eq__(self, other):  # равенство
        return self.coeffs == Polynomial(other).coeffs  # сравнение коэф-ов

    def __add__(self, other):  # сложение
        other = Polynomial(other)
        a = [0 for i in range(max(len(self.coeffs), len(other.coeffs)))]
        for i in range(len(self.coeffs)):
            a[i] += self.coeffs[i]  # а + коэф-ты 1ого мн-на
        for i in range(len(other.coeffs)):
            a[i] += other.coeffs[i]  # а + коэф-ты 2ого мн-на
        return Polynomial(a)

    def __radd__(self, other):  # правое сложение
        return self + other

    def __neg__(self):  # унарный минус
        return self * (-1)

    def __sub__(self, other):  # вычитание
        return self + (-other)

    def __rsub__(self, other):  # левое вычитание
        return -(self - other)

    def __call__(self, x):  # значение в точке
        res = 0
        for i in range(len((self.coeffs))):
            res += self.coeffs[i] * (x ** i)
        return res

    def degree(self):  # cтепень многочлена
        return len(self.coeffs) - 1

    def der(self, d=1):  # производная порядка d
        a = self.coeffs.copy()
        for i in range(d):
            k = len(a) - 1  # к -- степень дифференцируемого многочлена
            for j in range(k):
                a[j] = a[j + 1] * (j + 1)  # считаем коэффициенты производной
            a[k] = 0   # у производной степень на 1 меньше
            k -= 1
        return Polynomial(a)

    def __mul__(self, other):  # умножение
        other = Polynomial(other)
        a = [0 for i in range(self.degree() + other.degree() + 1)]
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                a[j + i] += self.coeffs[i] * other.coeffs[j]
        return Polynomial(a)

    def __rmul__(self, other):  # правое умножение
        return self * other

    def __iter__(self):  # итератор
        self.n = 0
        return self

    def __next__(self):  # итерирование
        if self.n < len(self.coeffs):
            res = (self.n, self.coeffs[self.n])
            self.n += 1
            return (res)
        else:
            raise StopIteration


class NotOddDegreeException(BaseException):  # класс ошибки
    pass


class RealPolynomial(Polynomial):
    def __init__(self, *args):  # инициализация
        if isinstance(args[0], RealPolynomial):
            self.coeffs = args[0].coeffs
        elif len(args) == 1:
            self.coeffs = Polynomial(args[0]).coeffs
        else:
            self.coeffs = Polynomial(list(args)).coeffs
        if self.degree() % 2 == 0:   # проверяем степень на четность
            raise NotOddDegreeException()

    def find_root(self, eps=1e-8, a=-1e6, b=1e6):
        # поиск корня с точность eps на (a, b)
        while abs(self((a + b) / 2)) > eps:  # бинарный поиск
            x = (a + b) / 2
            if self(b) == 0:
                return b
            if self(a) == 0:
                return a
            if self(x) > 0:
                b = x
            else:
                a = x
        return (a + b) / 2


class DegreeIsTooBigException(BaseException):  # класс ошибки
    pass


class QuadraticPolynomial(Polynomial):
    def __init__(self, *args):  # инициализация
        if isinstance(args[0], QuadraticPolynomial):
            self.coeffs = args[0].coeffs
        elif len(args) == 1:
            self.coeffs = Polynomial(args[0]).coeffs
        else:
            self.coeffs = Polynomial(list(args)).coeffs
        if len(self.coeffs) > 3:  # проверка, что степень меньше 3
            raise DegreeIsTooBigException()

    def solve(self):
        if len(self.coeffs) == 1:  # если мн-н нулевой степени - корней нет
            return []
        if len(self.coeffs) == 2:  # если мн-н линейный - один корень
            return [-self.coeffs[0] / self.coeffs[1]]
        a = self.coeffs[2]
        b = self.coeffs[1]
        c = self.coeffs[0]
        d = b ** 2 - 4 * a * c  # дискриминант
        if d < 0:
            return []
        elif d == 0:
            return [-b / (2 * a)]
        # в остальных случаях возвращаем 2 корня
        return [(-b - sqrt(d)) / (2 * a), (-b + sqrt(d)) / (2 * a)]












