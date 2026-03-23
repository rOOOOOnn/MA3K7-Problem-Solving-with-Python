def spiral_info(n: int):
    """Return coordinates and Manhattan distance of n."""
    if n < 1:
        raise ValueError("n must be a positive integer")

    x, y = 0, 0
    current = 1

    if n == 1:
        return (x, y), abs(x) + abs(y)

    step_length = 1
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    d = 0

    while current < n:
        dx, dy = directions[d % 4]

        for _ in range(step_length):
            x += dx
            y += dy
            current += 1

            if current == n:
                return (x, y), abs(x) + abs(y)

        d += 1

        if d % 2 == 0:
            step_length += 1

def main():
    n = int(input("Enter n: "))
    coord, dist = spiral_info(n)
    print("coordinate =", coord)
    print("Manhattan distance =", dist)


if __name__ == "__main__":
    main()




'''
Enter n: 9
coordinate = (1, -1)
Manhattan distance = 2

Enter n: 99
coordinate = (-3, 5)
Manhattan distance = 8

Enter n: 999
coordinate = (10, 16)
Manhattan distance = 26
'''