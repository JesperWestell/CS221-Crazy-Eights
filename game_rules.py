
CHAIN_RULE = False

class Suit:
    SPADE = 'spade'
    HEART = 'heart'
    CLUB = 'club'
    DIAMOND = 'diamond'


class ClassicGameRules:
    suits = [Suit.HEART,Suit.DIAMOND,Suit.CLUB,Suit.SPADE]
    ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    numStartingCards = 6
    multiplicity = 1

class TinyGameRules:
    suits = [Suit.HEART,Suit.DIAMOND]
    ranks = [1,2,3,4,5,6,7,8]
    numStartingCards = 2
    multiplicity = 1

gameRules = TinyGameRules