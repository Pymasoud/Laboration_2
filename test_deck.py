import pytest
from deck import Deck, Card


# Implementera tester ni anser lämpliga här. Motivera gärna varför de behövs (vad de testar och varför).


@pytest.mark.parametrize("test_input_rank, test_input_suite", [(1, "Hearts"), (10, "Spades"),
                                                               (11, "Clubs"), (12, "Diamonds"), (13, "Hearts")])
# Här testar vi att init metoden kan spara kort korrekt
# Vi vill testa specialfallen då rank representeras av en bokstav (A,J,D,K), samt ett vanligt kort
def test_card_init(test_input_rank, test_input_suite):
    c = Card(test_input_rank, test_input_suite)
    assert c.rank == test_input_rank
    assert c.suite == test_input_suite


# Här testar vi om __eq__ ger att 2 kort med olika färger är av samma värde
# Samt att olika kort inte är av samma värde (lika så om de har samma färg)
def test_card_eq():
    c1 = Card(1, "Hearts")
    c2 = Card(1, "Spades")
    c3 = Card(13, "Hearts")
    c4 = Card(13, "Spades")

    assert c1 == c2
    assert c3 == c4
    assert c2 != c3
    assert c1 != c4


# __lt__ låter oss använda < när vi ska jämföra 2 kort.
# Här kontrollerar vi att det är rank som styr att ett kort är mindre än ett annat
def test_card_lt():
    c1 = Card(1, "Hearts")
    c2 = Card(1, "Spades")
    c3 = Card(13, "Hearts")
    c4 = Card(13, "Spades")
    c5 = Card(5, "Clubs")
    c6 = Card(10, "Diamonds")

    assert c1 < c3
    assert c2 < c5
    assert c5 < c6
    assert c6 < c4
    assert not c1 < c2
    assert not c1 < c1
    assert not c3 < c2


# Funktionen gt låter oss jämföra två objekt med >.
# Här kollar vi att det är rank som styr vad som är störst
def test_card_gt():
    c1 = Card(1, "Hearts")
    c2 = Card(1, "Spades")
    c3 = Card(5, "Clubs")
    c4 = Card(10, "Diamonds")
    c5 = Card(13, "Hearts")
    c6 = Card(13, "Spades")

    assert c6 > c4
    assert c6 > c2
    assert c3 > c1
    assert not c1 > c4
    assert not c3 > c6
    assert not c5 > c6


# Här testar vi att längden på våran kortlek är 52, (dvs alla kort)
def test_deck_len():
    d = Deck()
    assert len(d.cards) == 52


# Först skapar vi en kortlek, sedan blandar vi den, sen så använder vi våran sort metod
# Sen kollar vi igenom kortlistan,
# så att föregående kort i listan har likadant eller mindre värde än det nuvarande kortet.
def test_deck_sort():
    d = Deck()
    d.shuffle()
    d.sort()

    prev_card = d.cards[0]
    for card in d.cards:
        card = prev_card or card > prev_card
        prev_card = card


# Vi tar ett kort och kollar att kortet finns i kortleken efter det så kollar vi att kortleken minskar med ett kort.
# Sedan kollar vi att kortet som nu tas är överst i högen.
# Sen tar vi ytterligare 2 kort, eftersom kortleken är sorterad enl nummer så har vi tagit alla kungar,
# så i slutet kollar vi att inga kungar finns kvar i kortleken.
def test_deck_take():
    d = Deck()
    d.sort()

    assert len(d.cards) == 52
    assert d.take() in d.cards
    assert len(d.cards) == 51
    assert d.cards[-1] == d.take()

    d.take()
    picked_card = d.take()
    assert picked_card not in d.cards


# Vi tar ett kort, kontrollerar att kortleken minskar.
# Sedan lägger vi tillbaka kortet och ser att kortleken ökar, samt att kortet ligger överst i högen.
def test_deck_put():
    d = Deck()
    assert len(d.cards) == 52
    assert d.take() in d.cards
    assert len(d.cards) == 51
    picked_card = d.take()
    assert len(d.cards) == 50
    d.put(picked_card)
    assert picked_card == d.cards[-1]
    assert len(d.cards) == 51


# Här lägger vi till kort i en tom lista
# Vi testar de olika delarna i funktionen insert, dels att lägga till i en tom lista.
# Dels att lägga till något sist i listan(när kortet är större än det sista kortet i listan).
# Och dels att gå igenom listan steg för steg och öka våran index räknare tills kortet hittat rätt plats.
def test_deck_insert():
    c1 = Card(1, "Hearts")
    c2 = Card(13, "Hearts")
    c3 = Card(10, "Spades")
    c4 = Card(10, "Diamonds")
    d = Deck()
    sorted_list = []
    sorted_list = d.insert(sorted_list, c1)
    assert sorted_list == [c1]
    sorted_list = d.insert(sorted_list, c2)
    assert sorted_list == [c1, c2]
    assert sorted_list != [c2, c1]
    sorted_list = d.insert(sorted_list, c3)
    assert sorted_list == [c1, c3, c2]
    sorted_list = d.insert(sorted_list, c4)
    assert sorted_list == [c1, c4, c3, c2]


if __name__ == '__main__':
    pytest.main()
