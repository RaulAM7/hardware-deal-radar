from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

GBP_TO_EUR = Decimal("1.17")


def to_decimal(value: str | int | float | Decimal | None) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def quantize_money(value: Decimal | None) -> Decimal | None:
    if value is None:
        return None
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def convert_to_eur(
    amount: Decimal | None, currency: str | None, rate: float | None = None
) -> Decimal | None:
    if amount is None:
        return None
    if currency is None or currency.upper() == "EUR":
        return quantize_money(amount)
    if currency.upper() == "GBP":
        multiplier = Decimal(str(rate)) if rate is not None else GBP_TO_EUR
        return quantize_money(amount * multiplier)
    return quantize_money(amount)
