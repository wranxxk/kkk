﻿#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <iomanip>

using namespace std;

enum Difficulty { EASY = 1, MEDIUM, HARD };

struct Cell {
    bool hasMine = false;
    bool revealed = false;
    bool flagged = false;
    int adjacentMines = 0;
};

class Minesweeper {
private:
    int width, height, mineCount;
    vector<vector<Cell>> board;
    bool gameOver = false;

public:
    Minesweeper(int w, int h, int mines) : width(w), height(h), mineCount(mines) {
        board.resize(height, vector<Cell>(width));
        placeMines();
        calculateAdjacents();
    }

    void placeMines() {
        srand(time(nullptr));
        int placed = 0;
        while (placed < mineCount) {
            int x = rand() % width;
            int y = rand() % height;
            if (!board[y][x].hasMine) {
                board[y][x].hasMine = true;
                placed++;
            }
        }
    }

    void calculateAdjacents() {
        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                if (board[y][x].hasMine) continue;
                int count = 0;
                for (int dy = -1; dy <= 1; ++dy)
                    for (int dx = -1; dx <= 1; ++dx) {
                        int ny = y + dy, nx = x + dx;
                        if (ny >= 0 && ny < height && nx >= 0 && nx < width)
                            if (board[ny][nx].hasMine) count++;
                    }
                board[y][x].adjacentMines = count;
            }
        }
    }

    void reveal(int x, int y) {
        if (x < 0 || x >= width || y < 0 || y >= height || board[y][x].revealed || board[y][x].flagged)
            return;

        board[y][x].revealed = true;
        if (board[y][x].hasMine) {
            gameOver = true;
            return;
        }

        if (board[y][x].adjacentMines == 0) {
            for (int dy = -1; dy <= 1; ++dy)
                for (int dx = -1; dx <= 1; ++dx)
                    if (!(dx == 0 && dy == 0))
                        reveal(x + dx, y + dy);
        }
    }

    void toggleFlag(int x, int y) {
        if (x < 0 || x >= width || y < 0 || y >= height || board[y][x].revealed)
            return;
        board[y][x].flagged = !board[y][x].flagged;
    }

    void printBoard(bool revealAll = false) {
        cout << "   ";
        for (int x = 0; x < width; ++x)
            cout << setw(2) << x;
        cout << "\n";

        for (int y = 0; y < height; ++y) {
            cout << setw(2) << y << " ";
            for (int x = 0; x < width; ++x) {
                const Cell& cell = board[y][x];
                if (revealAll || cell.revealed) {
                    if (cell.hasMine) cout << " *";
                    else cout << " " << cell.adjacentMines;
                }
                else if (cell.flagged) {
                    cout << " F";
                }
                else {
                    cout << " .";
                }
            }
            cout << "\n";
        }
    }

    bool isGameOver() const { return gameOver; }

    bool isWin() const {
        for (int y = 0; y < height; ++y)
            for (int x = 0; x < width; ++x)
                if (!board[y][x].hasMine && !board[y][x].revealed)
                    return false;
        return true;
    }
};

int main() {
    setlocale(LC_ALL, "");
    int choice;
    cout << "Выберите уровень сложности:\n";
    cout << "1. Легкий (8x8, 10 мин)\n";
    cout << "2. Средний (16x16, 40 мин)\n";
    cout << "3. Сложный (24x24, 99 мин)\n";
    cin >> choice;

    int width, height, mines;
    switch (choice) {
    case EASY: width = height = 8; mines = 10; break;
    case MEDIUM: width = height = 16; mines = 40; break;
    case HARD: width = height = 24; mines = 99; break;
    default: cout << "Неверный выбор.\n"; return 1;
    }

    Minesweeper game(width, height, mines);

    while (!game.isGameOver() && !game.isWin()) {
        game.printBoard();
        char cmd;
        int x, y;
        cout << "Введите команду (r x y - открыть, f x y - флаг): ";
        cin >> cmd >> x >> y;

        if (cin.fail()) {
            cin.clear();
            cin.ignore(10000, '\n');
            cout << "Некорректный ввод. Пример: r 3 4 или f 3 4\n";
            continue;
        }

        if (cmd == 'r' || cmd == 'R') {
            game.reveal(x, y);
        }
        else if (cmd == 'f' || cmd == 'F') {
            game.toggleFlag(x, y);
        }
        else {
            cout << "Неизвестная команда. Используйте 'r' или 'f'.\n";
        }
    }

    game.printBoard(true);
    if (game.isWin())
        cout << "Поздравляем! Вы выиграли!\n";
    else
        cout << "Вы попали на мину. Игра окончена.\n";

    return 0;
}

