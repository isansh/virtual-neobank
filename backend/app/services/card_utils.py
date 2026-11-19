import random


def _luhn_check_digit(number_without_check: str) -> int:
    total = 0
    for i, ch in enumerate(reversed(number_without_check)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10


def generate_card_number(card_type: str) -> str:
    prefix = "4" if card_type == "visa" else "5"
    body = prefix + "".join(random.choices("0123456789", k=14))
    return body + str(_luhn_check_digit(body))


def generate_iban(bank_code: str = "320478") -> str:
    account = "".join(random.choices("0123456789", k=19))
    bban = bank_code + account
    check = 98 - (int(bban + "301000") % 97)
    return f"UA{check:02d}{bban}"
    
