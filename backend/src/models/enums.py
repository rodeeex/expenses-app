from enum import Enum


class ExpenseCategory(str, Enum):
    food = "food"
    transport = "transport"
    subscriptions = "subscriptions"
    health = "health"
    entertainment = "entertainment"
    utilities = "utilities"
    other = "other"


class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    other = "other"
