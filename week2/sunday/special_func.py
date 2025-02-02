"""
This is a special func
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Person:
    name: str
    surname: str
    age: int


class PersonStandard:
    """
    # Heading 1

    Hello I am a paragraph

    >>> a.speak()
    "Hi ..."

    """

    name: str
    surname: str
    age: int

    def __init__(self, name, surname, age) -> None:
        self.name = name
        self.surname = surname
        self.age = age

    def __str__(self) -> str:
        return f"{self.name} {self.surname} is at age {self.age}"
        # return f"{self.__class__.__name__}(name='{self.name}', surname={self.surname}, age={self.age})"

    def speak(self):
        print(f"Hi !!! This is {self.name} {self.surname}")
        print(self.__doc__)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.speak()


if __name__ == "__main__":
    p = Person("Husnu", "Sensoy", 42)
    p_clone = Person("Husnu", "Sensoy", 42)

    p2 = PersonStandard("Husnu", "Sensoy", 42)
    p2_clone = PersonStandard("Husnu", "Sensoy", 42)

    print(p)
    print(p2)

    print(p == p_clone)
    print(p2 == p2_clone)

    p2.speak()

    print(__doc__)  # rich

    # PersonStandard(name='Husnu', surname='Sensoy',age=42)()()()()()()

    # TODO: Nasıl print(p > p_clone)
