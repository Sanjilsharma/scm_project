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

        self.balance = 0
        self.lines = 1
        self.bet = 1
        self.total_spins = 0
        self.total_winnings = 0
        self.symbol_matrix = []

        self.running = True

        self.choose_lines_window = True
        self.spin_window = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.choose_lines_window:
                        if event.key == pygame.K_RETURN:
                            self.choose_lines_window = False
                            self.lines = self.get_number_of_lines()
                            self.spin_window = True
                    elif self.spin_window:
                        if event.key == pygame.K_q:
                            self.spin()
                        elif event.key == pygame.K_a:
                            self.add_money()

            self.screen.fill((255, 255, 255))

            if self.choose_lines_window:
                self.draw_text("Press ENTER to start", (20, 20))
            elif self.spin_window:
                self.draw_text("Press Q to spin, A to add money", (20, 20))
                self.draw_symbol_matrix()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_text(self, text, pos):
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, pos)

    def draw_symbol_matrix(self):
        if self.symbol_matrix:
            for row_index, row in enumerate(self.symbol_matrix):
                for col_index, symbol in enumerate(row):
                    x = 200 + col_index * 100
                    y = 200 + row_index * 100
                    symbol_text = self.font.render(symbol, True, (0, 0, 0))
                    self.screen.blit(symbol_text, (x, y))

    def spin(self):
        total_bet = self.lines * self.bet
        if total_bet > self.balance:
            print(f"Not enough balance. Your balance is ${self.balance}.")
            return

        self.total_spins += 1
        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)

        winnings, winning_lines, symbols_matrix = self.check_winnings(slots, self.lines, self.bet, symbol_values)
        self.total_winnings += winnings
        self.balance += winnings - total_bet

        self.symbol_matrix = symbols_matrix

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

    def add_money(self):
        money_input = self.show_input_dialog("Enter amount to add:")
        if money_input.isdigit():
            money = int(money_input)
            if money > 0:
                self.balance += money

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
        columns = []
        for _ in range(cols):
            column = []
            for _ in range(rows):
                symbol = random.choice(list(symbols.keys()))
                column.append(symbol)
            columns.append(column)

        return columns

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        symbols_matrix = []
        for line in range(lines):
            symbol = columns[0][line]
            symbols_row = []
            for column in columns:
                symbol_to_check = column[line]
                symbols_row.append(symbol_to_check)
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)
            symbols_matrix.append(symbols_row)

        return winnings, winning_lines, symbols_matrix

def main():
    game = SlotMachineGame()
    game.run()

if __name__ == "__main__":
    main()
