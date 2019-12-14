from Deck import Deck
import os
# from cards import Card
deck = Deck()
deck.shuffle()
player_hand = []
dealer_hand = []
won = 0
lost = 0
def clear():
    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')
def deal():
    hand1 = []
    hand2 = []
    for i in range(2):
        deck.shuffle()
        hand1.append(deck.deal())
        hand2.append(deck.deal())
    hands = [hand1 , hand2]
    return hands
def hit():
    return deck.deal()
def play_again():
    global player_hand
    global dealer_hand
    again = input("Do you want to try another hand? (Y/n) :").lower()
    if again != "n":    #if our answer is not 'n' then we default to 'y'
        for i in dealer_hand:
            deck.return_card(i)
        for a in player_hand:
            deck.return_card(a)
        player_hand = []
        dealer_hand = []
        if deck.deck_count() != 52:
            print("Error in Function 'play_again()'. Deck count invalid.")
            exit()
        game();
    else:
        print("Goodbye...")
        exit()
def total(hand):
    total = 0
    for i in hand:
        if i.number == "Jack" or i.number == "Queen" or i.number == "King" :
            total += 10
        elif i.number == "Ace":
            if total >= 11: total +=1
            else: total += 11
        else:
            total += int(i.number)
    return total
def print_results(dealer_hand,  player_hand):
    clear()
    dstr = ""
    pstr = ""
    for i in dealer_hand:
        dstr += i.__repr__()
        dstr += " "
    for a in player_hand:
        pstr += a.__repr__()
        pstr += " "
    print("The Dealer's hand is " + dstr + ". With a total of: " + str(total(dealer_hand)))
    print("Your hand is " + pstr + ". With a total of: " + str(total(player_hand)))
def blackjack(dealer_hand,  player_hand):
    global won
    global lost
    if total(player_hand) == 21:
        print_results(dealer_hand,  player_hand)
        print("Blackjack... Congratulations")
        won += 1
        play_again()
    elif total(dealer_hand) == 21:
        print_results(dealer_hand,  player_hand)
        print("Bad luck... The Dealer has Blackjack!")
        lost += 1
        play_again()
def score(td,  tp):
    global won
    global lost
    if tp <= 21:
        if td <= 21:
            if td < tp:
                won += 1
                print_results(dealer_hand,  player_hand)
                x = 0
                for i in player_hand:
                    x += 1
                if x == 5 and tp == 21:
                    print("5 Card Trick!")
                print("Congratulations... You Win.")
                play_again()
            elif td > tp:
                lost += 1
                print_results(dealer_hand,  player_hand)
                print("Bad luck... The Dealer won.")
                play_again()
            else:
                print_results(dealer_hand,  player_hand)
                print("A Draw...")
                play_again()
        else:
            won += 1
            print_results(dealer_hand, player_hand)
            print("The Dealer is Bust... You Win.")
            play_again()
    else:
        lost += 1
        print("You are Bust...")
        play_again()
def game():
    global won
    global lost
    global dealer_hand
    global player_hand
    choice = 0
    clear()
    print("Welcome to Blackjack")
    print(" Games Won: %s  Games Lost: %s" % (won,  lost))
    hands = deal()
    dealer_hand = hands.pop()
    player_hand = hands.pop()
    print("The Dealer is showing the " + dealer_hand[1].__repr__())
    hstr = ""
    for i in player_hand:
        hstr += i.__repr__()
        hstr += " "
    print ("")
    print("Your hand is: " + hstr + " for a total of " + str(total(player_hand)))
    blackjack(dealer_hand,  player_hand)
    while choice != "q":
        choice = input("Do you want to [H]it, [S]tick, or [Q]uit: ").lower()
        if choice == "q":
            print("Goodbye... See you soon...")
            exit()
        elif choice == "h":
            card = hit()
            player_hand.append(card)
            tp = total(player_hand)
            print(card.__repr__() + "  new total is " + str(tp))
            if tp > 21:
                score(total(dealer_hand),  tp)
        else: #make [S]tick the default option
            while total(dealer_hand) < 17:
                dealer_hand.append(hit())
            score(total(dealer_hand),  total(player_hand))
if __name__ == "__main__":
    game()
