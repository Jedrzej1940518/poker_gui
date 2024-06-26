from pokerkit import Automation, NoLimitTexasHoldem, State
from game_logic.game_state import SimpleState

from enum import IntEnum, unique


@unique
class Action(IntEnum):
    CHECK_OR_CALL = 0
    RAISE = 1


class PokerGame:
    def __init__(self, simple_state: SimpleState):
        self.simple_state = simple_state

    def action(self, act: Action):
        if act == Action.CHECK_OR_CALL:
            self.pokerkit_state.check_or_call()
        elif act == Action.RAISE:
            self.pokerkit_state.complete_bet_or_raise_to()

        self.simple_state.update_state(self.pokerkit_state)

    def init_hand(self):
        if len(self.simple_state.players_data) != 2:
            print("[TODO] error bro")

        self.pokerkit_state = NoLimitTexasHoldem.create_state(
            # Automations
            (
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
                Automation.HOLE_DEALING,
                Automation.CARD_BURNING,
                Automation.BOARD_DEALING,
            ),
            True,  # Uniform antes?
            500,  # Antes
            (1000, 2000),  # Blinds or straddles
            2000,  # Min-bet
            self.stacks(),  # Starting stacks
            len(self.simple_state.players_data),  # Number of players
        )
        self.simple_state.update_state(self.pokerkit_state)

    def stacks(self):
        return [player.stack for player in self.simple_state.players_data]


if __name__ == "__main__":
    PokerGame()
