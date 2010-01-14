from random import shuffle

class GameException(Exception): pass
class GameOver(GameException): pass

class Game(object):
    def __init__(self):
        self.start()

    def start(self):
        # Copy the global deck - the list is new so it can be shuffled for each
        # game without affecting the state of other games but for each card
        # there is only one card object to save memory
        self.cards = Deck.cards[:]
        shuffle(self.cards)
        self.table_cards = []
        self.check_table()
        self.players = []

    def check_table(self):
        while True:
            if self.is_game_over():
                raise GameOver('Game Over')
            if self.sets_on_table() and \
               (len(self.table_cards) >= 12 or len(self.cards) == 0):
                return
            for card in self.cards[-3:]:
                self.cards.remove(card)
                self.table_cards.append(card)

    def sets_on_table(self):
        sets = []
        for a in xrange(0, len(self.table_cards) - 2):
            for b in xrange(a + 1, len(self.table_cards) - 1):
                for c in xrange(b + 1, len(self.table_cards)):
                    card_a = self.table_cards[a]
                    card_b = self.table_cards[b]
                    card_c = self.table_cards[c]
                    potential_set = [card_a, card_b, card_c]
                    if is_set(potential_set):
                        sets.append(potential_set)
        if not len(sets):
            return None
        return sets

    def found_set(self, player, cards):
        if not is_set(cards):
            raise GameException('Not a set')
        for card in cards:
            if not card in self.table_cards:
                raise GameException('Some cards no longer on the table')
        for card in cards:
            self.table_cards.remove(card)
        self.check_table()
        player.sets += 1

    def is_game_over(self):
        if len(self.cards) == 0 and not self.sets_on_table():
            self.start()
            return True
        return False

class Player(object):
    def __init__(self, game, name='New Player'):
        self.game = game
        self.game.players.append(self)
        self.name = name
        self.sets = 0

    def found_set(self, cards):
        self.game.found_set(self, cards)

class Card(object):
    def __init__(self, number, shape, color, shade):
        self.number = number
        self.shape = shape
        self.color = color
        self.shade = shade

    def __repr__(self):
        return '%s%s%s%s' % (self.number, self.shade, self.color, self.shape)

    def image(self):
        return '/static/cards/%s.png' % (self)

class Deck(object):
    def __init__(self):
        self.cards = []
        self.id_to_card = {}
        for number in (1, 2, 3):
            for shape in ('s', 'd', 'o'):
                for color in ('r', 'g', 'b'):
                    for shade in ('s', 'f', 'e'):
                        card = Card(number, shape, color, shade)
                        self.cards.append(card)
                        self.id_to_card[str(id(card))] = card

Deck = Deck()

def same_or_different(l):
    a, b, c = l
    return (a == b and b == c) or (a != b and b != c and c != a)

def is_set(cards):
    return same_or_different((card.number for card in cards)) and \
           same_or_different((card.shape  for card in cards)) and \
           same_or_different((card.color  for card in cards)) and \
           same_or_different((card.shade  for card in cards))
