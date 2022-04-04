from puzzleSolver import *
import time

print("------ Selamat datang ke Permaiann 15-Puzzle ------")

print("\nMasukkan nama fle puzzle yang akan dijalankan: (contoh: puzzle.txt)")

fileName = input("Nama File : ")
path = "../test/" + fileName
puzzle = getPuzzle(path)
print("\nPuzzle : \n")
printPuzzle(puzzle)
print("\nNilai KURANG(i) dalam setiap sel yang tidak kosong:\n")
solvable = isCrackable(puzzle)
if solvable:
    print("\nLangkah-langkah untuk menyelesaikan puzzle: ")
    print("\nState awal : ")
    printPuzzle(puzzle)
    start = time.time()
    solvePuzzle(puzzle)
    stop = time.time()
    print("Waktu yang dibutuhkan = ", stop - start, "detik")
    print("---------------------------------------")
else:
    print("---------------------------------------")