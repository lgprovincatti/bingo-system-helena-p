import random

from app.core.game_state import game_state


class BingoService:

    BINGO_RANGES = {
        "B": range(1, 16),
        "I": range(16, 31),
        "N": range(31, 46),
        "G": range(46, 61),
        "O": range(61, 76)
    }

    @classmethod
    def draw_number(cls):

        available_numbers = [
            number
            for number in range(1, 76)
            if number not in game_state["drawn_numbers"]
        ]

        if not available_numbers:

            game_state["game_finished"] = True

            return None

        number = random.choice(available_numbers)

        result = {
            "number": number,
            "letter": cls.get_letter(number)
        }

        game_state["drawn_numbers"].append(number)

        game_state["current_number"] = result

        return result

    @classmethod
    def get_letter(cls, number):

        for letter, number_range in cls.BINGO_RANGES.items():

            if number in number_range:
                return letter

        return ""

    @classmethod
    def get_drawn_numbers(cls):

        return game_state["drawn_numbers"]

    @classmethod
    def reset_game(cls):

        game_state["drawn_numbers"] = []

        game_state["current_number"] = None

        game_state["automatic_mode"] = False

        game_state["paused"] = False

        game_state["game_finished"] = False