import random
from app.models import Group


def generate_groups() -> list[Group]:
    group_names = [''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(2)]) + '-' + ''.join(
        [random.choice('0123456789') for _ in range(2)]) for _ in range(10)]
    groups = [Group(name=name) for name in group_names]

    return groups


if __name__ == '__main__':
    groups = generate_groups()
