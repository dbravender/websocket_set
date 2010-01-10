class Card(object):
    def __init__(self, number, shape, color, shade):
        self.number = number
        self.shape = shape
        self.color = color
        self.shade = shade

    def image(self):
        return 'static/%s%s%s%s.png' % (self.number, self.shade, self.color, self.shape)

Cards = []

for number in (1, 2, 3):
    for shape in ('s', 'd', 'o'):
        for color in ('r', 'g', 'b'):
            for shade in ('s', 'f', 'e'):
                Cards.append(Card(number, shape, color, shade))

def same_or_different(l):
    a, b, c = l
    return a == b and b == c or a != b and b != c and c != a

def is_set(cards):
    return same_or_different((card.number for card in cards)) and \
           same_or_different((card.shape for card in cards)) and \
           same_or_different((card.color for card in cards)) and \
           same_or_different((card.shade for card in cards))
