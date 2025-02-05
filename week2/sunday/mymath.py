class Polynomial:
    def __init__(self, x: float):
        self.x = x

    def way1(self, *args) -> float:
        result = 0

        for i, c in enumerate(list(args)):
            result += (self.x**i) * c

        return result

    def way2(self, *args) -> float:
        result = 0

        for c in reversed(list(args)):
            result = result * x + c

        return result

    def __call__(self, *args) -> float:
        return self.way1(*args)


if __name__ == "__main__":
    x = 1
    y = Polynomial(x)(1, 2)  # 1+2x
    y = Polynomial(x)(1, 2, 3)  # 1+2x+3x^2
    y = Polynomial(x)(1, 2, 3, 4, 5, 6, 6, 7, 8)  # 1x^0+2x+3x^2+...
