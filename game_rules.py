
CHAIN_RULE = False

class Actions:
    PASS = 'pass'
    TAKE = 'take'
    PLAY = 'play'
    AllActions = [PASS,TAKE,PLAY]

class Suit:
    SPADE = 'spade'
    HEART = 'heart'
    CLUB = 'club'
    DIAMOND = 'diamond'

class ClassicGameRules:
    suits = [Suit.DIAMOND,Suit.HEART,Suit.SPADE,Suit.CLUB]
    ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    numStartingCards = 7
    multiplicity = 1

class TinyGameRules:
    suits = [Suit.HEART,Suit.DIAMOND]
    ranks = [1,2,3,4,5,6,7,8]
    numStartingCards = 2
    multiplicity = 1

class VeryTinyGameRules:
    suits = [Suit.HEART,Suit.DIAMOND]
    ranks = [1,2]
    numStartingCards = 2
    multiplicity = 1

gameRules = VeryTinyGameRules

