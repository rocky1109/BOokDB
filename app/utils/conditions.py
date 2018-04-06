
floor = lambda val: 0 if val is None else val
ceil = lambda val: 100000 if val is None else val


class Condition(object):

    @classmethod
    def tariff_range(cls, day_ranges, per_day_tariffs, elapsed_days):
        total = 0
        for index in range(len(day_ranges)):
            min_days, max_days = floor(day_ranges[index][0]), \
                                 ceil(day_ranges[index][1]) - 1
            if max_days >= elapsed_days:
                total += elapsed_days * per_day_tariffs[index]
                break
            else:
                total += max_days * per_day_tariffs[index]
                elapsed_days -= max_days
        return total

    @classmethod
    def min_charges(cls, for_less_than_days, min_tariff, elapsed_days):
        if elapsed_days < for_less_than_days:
            return min_tariff
        return None


if __name__ == "__main__":
    print(Condition.tariff_range(day_ranges=[(None, 3), (3, None)],
                                 per_day_tariffs=[1.0, 1.5],
                                 elapsed_days=5))
    print(Condition.min_charges(for_less_than_days=2, min_tariff=2.0,
                                elapsed_days=4))
    print(Condition.min_charges(for_less_than_days=3, min_tariff=4.5,
                                elapsed_days=2))
