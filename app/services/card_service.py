import random


class CardService:

    COLUMN_RANGES = {
        "B": range(1, 16),
        "I": range(16, 31),
        "N": range(31, 46),
        "G": range(46, 61),
        "O": range(61, 76)
    }

    @classmethod
    def generate_card(
        cls,
        card_number: int
    ):

        card = []

        for column, number_range in cls.COLUMN_RANGES.items():

            numbers = sorted(
                random.sample(
                    list(number_range),
                    5
                )
            )

            card.append(numbers)

        card[2][2] = "FREE"

        return {
            "id": f"{card_number:04}",
            "numbers": card
        }

    @classmethod
    def generate_unique_cards(
        cls,
        quantity: int
    ):

        unique_cards = []

        generated = set()

        card_number = 1

        while len(unique_cards) < quantity:

            card = cls.generate_card(
                card_number
            )

            signature = str(
                card["numbers"]
            )

            if signature in generated:
                continue

            generated.add(signature)

            unique_cards.append(card)

            card_number += 1

        return unique_cards