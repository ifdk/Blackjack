from player import Player
from dealer import Dealer


class BlackjackGame:
    def __init__(self, player_list):
        self.dealer = Dealer()
        self.player_list = []
        for player_name in player_list:
            self.player_list.append(Player(player_name, self.dealer))
        

    def play_rounds(self, num_rounds=1):
        """
        >>> import random; random.seed(1)
        >>> game = BlackjackGame(["Lawrence","Melissa"])
        >>> print(game.play_rounds(2))
        Round 1
        Dealer: [10, 9] 0/0/0
        Lawrence: [10, 6, 3] 0/1/0
        Melissa: [8, 8] 0/0/1
        Round 2
        Dealer: [10, 10] 0/0/0
        Lawrence: [10, 3] 0/1/1
        Melissa: [9, 10] 0/0/2
        """
        
        game_results = []
        for round_num in range(0, num_rounds):
            self.dealer.shuffle_deck()
            
            self.dealer.deal_2_cards(self.player_list)
            
            is_round_over = False
            
            players_out_of_the_game = set()
            if self.dealer.card_sum == 21:
                self.dealer.record_win()
                for player in self.player_list:
                    if player.card_sum == 21:
                        player.record_tie()
                    else:
                        player.record_loss()
                is_round_over = True
            else:
                for player in self.player_list:
                    if player.card_sum == 21:
                        player.record_win()
                        players_out_of_the_game.add(player)
            if is_round_over:
                
                round_results = self.calculate_round_results(round_num, players_out_of_the_game)
                game_results.append(round_results)
                self.discard_hands()
                continue 
            
            for player in self.player_list:
                
                if player in players_out_of_the_game:
                    continue
                player.play_round()
                if player.card_sum > 21:
                    player.record_loss()

            self.dealer.play_round()
            round_results = self.calculate_round_results(round_num, players_out_of_the_game)
            game_results.append(round_results)
            self.discard_hands()
        
        return "".join(game_results)[:-1]

    
    def discard_hands(self):
        
        for player in self.player_list:
            player.discard_hand()
        self.dealer.discard_hand()

    def calculate_round_results(self, round_num, players_out_of_the_game):
        
        if self.dealer.card_sum > 21:
            for player in self.player_list:
                if player in players_out_of_the_game:
                    continue
                if player.card_sum <= 21:
                    player.record_win()
                else:
                    player.record_loss()
        else:
            for player in self.player_list:
                if player in players_out_of_the_game:
                    continue
                if player.card_sum > self.dealer.card_sum:
                    player.record_win()
                elif player.card_sum == self.dealer.card_sum:
                    player.record_tie()
                else:
                    player.record_loss()
        round_result = "Round " + str(round_num+1) + "\n"
        round_result += str(self.dealer) + "\n"
        
        for player in self.player_list:
            round_result += str(player) + "\n"
        return round_result

    def reset_game(self):
        """
        >>> game = BlackjackGame(["Lawrence", "Melissa"])
        >>> _ = game.play_rounds()
        >>> game.reset_game()
        >>> game.player_list[0]
        Lawrence: [] 0/0/0
        >>> game.player_list[1]
        Melissa: [] 0/0/0
        """
        for player in self.player_list:
            player.reset_stats()
        self.dealer.reset_stats()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
