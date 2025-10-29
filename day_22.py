import sys


def parse(lines):
    return ([int(line.strip()) for line in lines if line.strip()],)


def mix(secret, number):
    return secret ^ number


def prune(secret):
    return secret % 16777216


def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    return prune(mix(secret, secret * 2048))


def part1(keys):
    s = 0
    for k in keys:
        for _ in range(2000):
            k = next_secret(k)
        s += k
    return s


def get_banana_counts(k):
    banana_count: list[None | int] = [None] * (20**4)
    banana_index = 0
    for _ in range(2000):
        prev_price = k % 10
        k = next_secret(k)
        price = k % 10
        price_change = price - prev_price
        assert -9 <= price_change < 10
        banana_index *= 20
        banana_index += price_change + 10  # in [1, 20)
        if banana_index // 20**3:
            if banana_count[banana_index] is None:
                banana_count[banana_index] = price
            banana_index %= 20**3
    return banana_count


def part2(keys):
    banana_count = [0] * (20**4)
    for k in keys:
        for i, c in enumerate(get_banana_counts(k)):
            if c is not None:
                banana_count[i] += c
    return max(banana_count)


if __name__ == "__main__":
    print(part2(*parse(sys.stdin)))
