import pygame
import random

MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_values = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class SlotMachineGame:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Slot Machine")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)

        self.balance = 1000
        self.lines = 1
        self.bet = 1

        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.spin()
                    elif event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_RETURN:
                        self.lines = self.get_number_of_lines()
                    elif event.key == pygame.K_BACKSPACE:
                        self.bet = self.get_bet()

            self.screen.fill((255, 255, 255))

            self.draw_text(f"Balance: ${self.balance}", (20, 20))
            self.draw_text("Press SPACE to spin, Q to quit", (20, 60))

            self.draw_lines_selection()
            self.draw_bet_selection()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_text(self, text, pos):
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, pos)

    def draw_lines_selection(self):
        lines_text = self.font.render(f"Lines to bet on: {self.lines}", True, (0, 0, 0))
        self.screen.blit(lines_text, (20, 100))

    def draw_bet_selection(self):
        bet_text = self.font.render(f"Betting amount per line: {self.bet}", True, (0, 0, 0))
        self.screen.blit(bet_text, (20, 150))

    def spin(self):
        total_bet = self.lines * self.bet
        if total_bet > self.balance:
            print(f"Not enough balance. Your balance is ${self.balance}.")
            return

        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)

        winnings, winning_lines = self.check_winnings(slots, self.lines, self.bet, symbol_values)
        self.balance += winnings - total_bet

        print(f"You won ${winnings}.{' You won on line(s): ' + ', '.join(map(str, winning_lines)) if winning_lines else ''}")

    def get_number_of_lines(self):
        while True:
            lines_input = self.show_input_dialog("Enter the number of lines to bet on (1-3):")
            if lines_input.isdigit():
                lines = int(lines_input)
                if 1 <= lines <= MAX_LINES:
                    return lines
            else:
                print("Please enter a valid number of lines")

    def get_bet(self):
        while True:
            bet_input = self.show_input_dialog("Enter bet amount per line ($1-$1000):")
            if bet_input.isdigit():
                bet = int(bet_input)
                if MIN_BET <= bet <= MAX_BET:
                    return bet
            else:
                print("Please enter a valid bet amount")

    def show_input_dialog(self, prompt):
        user_input = ""
        input_rect = pygame.Rect(0, 0, 200, 30)
        input_rect.center = (self.screen_width // 2, self.screen_height // 2)

        active = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

            self.screen.fill((255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2)
            self.draw_text(prompt, (input_rect.x, input_rect.y - 40))
            self.draw_text(user_input, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.flip()
            self.clock.tick(60)

        return user_input

    def get_slot_machine_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)

            columns.append(column)

        return columns

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

def main():
    game = SlotMachineGame()
    game.run()

if __name__ == "__main__":
    main()
