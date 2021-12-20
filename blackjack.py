import random
import tkinter

def load_images(card_images):
    suits = ['heart', 'club', 'spade', 'diamond']
    face_cards = ['jack', 'queen', 'king']
    extension = 'png'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = "cards\\{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image))

        # next the face cards
        for card in face_cards:
            name = "cards\\{}_{}.{}".format(card, suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image))


def deal_cards(frame):
    # pop the next card of the top of the deck
    next_card = deck.pop(0)
    # and add it to back of the pack
    deck.append(next_card)
    # add the image to the Label and Display
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the cards face value
    return next_card[0]


def score_hand(hand):
    # Calculate the total score of all the cards in the list
    # Only one ace can have the value of 11
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there is a n ace and subtract 10
        if score > 21 and (ace in hand):
            score -= 10
            ace = False
    return score


def deal_dealer():
    global dealer_win
    global player_win
    a = dealer_win.get()
    b = player_win.get()
    dealer_score = score_hand(dealer_hand)
    player_score = score_hand(player_hand)
    while 0 < dealer_score < 17 and dealer_score <= player_score <= 21:
        dealer_hand.append(deal_cards(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)
        if dealer_score >= 17 or dealer_score >= player_score:
            if dealer_score > 21 or dealer_score < player_score:
                result_text.set("Player Wins!")
                b += 1
            elif dealer_score > player_score:
                result_text.set("Computer Wins!")
                a += 1
            else:
                result_text.set("Draw!")
    dealer_win.set(a)
    player_win.set(b)


def deal_player():
    global dealer_win
    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    if player_score <= 21 and result_text.get() == "":
        player_hand.append(deal_cards(player_card_frame))
        player_score = score_hand(player_hand)
        if player_score > 21:
            b = dealer_win.get()
            b += 1
            dealer_win.set(b)
            result_text.set("Computer Wins!")

    player_score_label.set(player_score)


def new_game():
    global dealer_card_frame
    global dealer_hand
    global player_hand
    global player_card_frame
    global card_frame
    global deck
    global cards
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(column=1, row=0, sticky='ew', rowspan=2)
    # embedded frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(column=1, row=2, sticky='ew', rowspan=2)
    result_text.set('')
    # Create a list to store dealer's and player's hand
    dealer_hand = []
    player_hand = []

    deal_player()
    dealer_hand.append(deal_cards(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def shuffle():
    global deck
    random.shuffle(deck)


def play():
    deal_player()
    dealer_hand.append(deal_cards(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()

    new_game()

    mainWindow.mainloop()


mainWindow = tkinter.Tk()

# Set up the screen and frames for the dealer and the player
mainWindow.title("Blackjack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text, background='green', fg="white")
result.grid(row=0, column=0, columnspan=3)

dealer_win = tkinter.IntVar(value=0)
dealer_win_result = tkinter.Label(mainWindow, text="Computer Wins:", background='sky blue')
dealer_win_result.grid(row=0, column=5)
tkinter.Label(mainWindow, textvariable=dealer_win, background='green', fg='white').grid(row=0, column=6)

player_win = tkinter.IntVar(value=0)
player_win_result = tkinter.Label(mainWindow, text="Player Wins:", background='sky blue')
player_win_result.grid(row=0, column=8)
tkinter.Label(mainWindow, textvariable=player_win, background='green', fg='white').grid(row=0, column=9)


card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=2, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Computer", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(column=1, row=0, sticky='ew', rowspan=2)

player_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Player", background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)
# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(column=1, row=2, sticky='ew', rowspan=2)

button_frame = tkinter.Frame(mainWindow, background='green')
button_frame.grid(row=3, column=0, columnspan=3, sticky='w', padx=5, pady=5)

dealer_button = tkinter.Button(button_frame, background='yellow', text='Computer', relief='raised', borderwidth=1,
                               command=deal_dealer)
dealer_button.grid(row=0, column=0, padx=5, pady=5)
player_button = tkinter.Button(button_frame, text='Player', background='orange', relief='raised', borderwidth=1, command=deal_player)
player_button.grid(row=0, column=1, padx=5, pady=5)
new_game_button = tkinter.Button(button_frame, text='New Game', relief='raised', background='light green', borderwidth=1, command=new_game)
new_game_button.grid(row=0, column=2, padx=5, pady=5)
shuffle_button = tkinter.Button(button_frame, text='Shuffle',background='red', relief='raised', borderwidth=1, command=shuffle)
shuffle_button.grid(row=0, column=3, padx=5, pady=5)

player_hand = []
dealer_hand = []

cards = []
load_images(cards)

# Create a new deck of cards and shuffle them
deck = list(cards)
shuffle()

if __name__ == "__main__":
    play()
