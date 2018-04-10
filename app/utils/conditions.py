
class ConditionHelper(object):

    @staticmethod
    def less_than(days, price, elapsed_days):
        return price * days

    @staticmethod
    def less_than_or_equal(days, price, elapsed_days):
        return price * days

    @staticmethod
    def greater_than(days, price, elapsed_days):
        if elapsed_days > days:
            return price * (elapsed_days - days)
        return 0

    @staticmethod
    def greater_than_or_equal(days, price, elapsed_days):
        if elapsed_days >= days:
            return price * (elapsed_days - days)
        return 0


class RuleHelper(object):

    @staticmethod
    def tariff_range(conditions):
        return sum(conditions.values())

    @staticmethod
    def min_charges(conditions):
        return sum(conditions.values())
