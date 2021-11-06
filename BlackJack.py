#Black Jack

#rules:
#full 52 card deck
#Dealer hits on <14 and stays on >16. 21 is a win, over 21 is a loss. player with higher numer wins otherwise. 
#wait for and take user input of hit or stay

import random

DECK_KEY={
'cA':1,'c2':2,'c3':3,'c4':4,'c5':5,'c6':6,'c7':7,'c8':8,'c9':9,'c10':10,'cJ':10,'cQ':10,'cK':10,
'sA':1,'s2':2,'s3':3,'s4':4,'s5':5,'s6':6,'s7':7,'s8':8,'s9':9,'s10':10,'sJ':10,'sQ':10,'sK':10,
'hA':1,'h2':2,'h3':3,'h4':4,'h5':5,'h6':6,'h7':7,'h8':8,'h9':9,'h10':10,'hJ':10,'hQ':10,'hK':10,
'dA':1,'d2':2,'d3':3,'d4':4,'d5':5,'d6':6,'d7':7,'d8':8,'d9':9,'d10':10,'dJ':10,'dQ':10,'dK':10}

def deal_hands(deck_pointer, dealer_hand, player_hand, DECK):
    for i in range(2):
        dealer_hand.append(DECK[deck_pointer])
        player_hand.append(DECK[deck_pointer+1])
        deck_pointer+=2
    return deck_pointer

def sum_hand(hand):
    summ, ace = 0, 0
    for i in hand:
        if DECK_KEY[i]==1:
            ace+=1
        else:
            summ+=DECK_KEY[i]
    for a in range(ace):
        if summ+11 > 21:
            summ+=1
        else:
            summ+=11
    return summ

def check_win(hand):
    if hand == 21: return 1 #win state
    if hand > 21: return -1 #loss state
    else: return 0 #continue state


def play(deck_pointer, dealer_hand, player_hand, DECK):
    winner=False
    deck_pointer = deal_hands(deck_pointer, dealer_hand, player_hand, DECK)
    print('Dealer Hand: ' + str(dealer_hand) + ' Value: ' + str(sum_hand(dealer_hand)))
    print('Player Hand: ' + str(player_hand) + ' Value: ' + str(sum_hand(player_hand)))

    #TO DO: Check if either player wins after first deal

    while not winner:
        print('Discard Pile: ' + str(deck_pointer))
        dealer_val=sum_hand(dealer_hand)
        player_val=sum_hand(player_hand)
        turn_start = deck_pointer
        if dealer_val < 17:
            dealer_hand.append(DECK[deck_pointer])
            deck_pointer+=1
        player_input = input("Enter Stay: 's' or Hit: 'h': \n")
        if player_input == 'h':
            player_hand.append(DECK[deck_pointer])
            deck_pointer+=1
        
        dealer_state = check_win(sum_hand(dealer_hand))
        player_state = check_win(sum_hand(player_hand))
        print('Dealer Hand: ' + str(dealer_hand) + ' Value: ' + str(sum_hand(dealer_hand)))
        print('Player Hand: ' + str(player_hand) + ' Value: ' + str(sum_hand(player_hand)))

        if dealer_state == 1 and player_state==1:
            print('both win')
            return [deck_pointer, 1, 0]
        if dealer_state == 1 or player_state==-1:
            print('dealer wins')
            return [deck_pointer, 0, 1]
        if player_state == 1 or dealer_state==-1:
            print('player wins')
            return [deck_pointer, 1, 0]
        
        if turn_start == deck_pointer:
            #if neither party hit this turn, end the turn and determine winner
            if sum_hand(dealer_hand) > sum_hand(player_hand): return [deck_pointer, 0, 1]
            else: return [deck_pointer, 1, 0]

def main():
    DECK=[
    'cA','c2','c3','c4','c5','c6','c7','c8','c9','c10','cJ','cQ','cK',
    'sA','s2','s3','s4','s5','s6','s7','s8','s9','s10','sJ','sQ','sK',
    'hA','h2','h3','h4','h5','h6','h7','h8','h9','h10','hJ','hQ','hK',
    'dA','d2','d3','d4','d5','d6','d7','d8','d9','d10','dJ','dQ','dK']
    random.shuffle(DECK)
    #print(DECK)
    #main game loop of 6 rounds
    deck_pointer, wins, losses = 0, 0, 0
    for i in range(6):
        dealer_hand=[]
        player_hand=[]
        results = play(deck_pointer, dealer_hand, player_hand, DECK)
        deck_pointer = results[0]
        wins += results[1]
        losses += results[2]
        print('wins: ' + str(wins) + ' losses: ' + str(losses))

if __name__ == '__main__':
    main()

