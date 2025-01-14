# Identitas
''' 
Kelas Dasar Pemrograman 9 - Kelompok 7
Nama anggota : 
- Juan Christopher Santoso (16521098) 
- Raymond As Mikhael Hutabarat (16521143) 
- Ferindya Aulia Berlianty (16521188) 
- Hanif Al Falih (16521332) 

'''
# PROGRAM TOKO BINOMO
# Deskripsi
'''
Program memiliki fungsi selayaknya sebuah program toko jual-beli game. 
Untuk menjalankan program, pengguna perlu menggunakan modul argparse dan menginputkan suatu folder tempat menyimpanan data.
Setelah suatu folder berhasil dibaca, maka program akan mulai untuk bekerja.
Pertama-tama, pengguna harus login terlebih dahulu untuk memiliki akses ke fungsi-fungsi yang lebih beragam.
Tanpa login, pengguna akan berada pada mode 'guest' dan dapat mengakses fungsi bonus seperti 'kerangajaib' dan 'tictactoe'.
Secara gambaran besar, akun terbagi menjadi 2 jenis yaitu user dan admin.
Setiap jenis akun memiliki akses ke fungsi yang berbeda-beda.
Program akan terus melakukan pengulangan (loop) selama pengguna masih menggunakan program.
Selama program terus berjalan, segala perubahan pada data belum disave pada file csv, kecuali pengguna menggunakan fungsi 'save'.
Program akan berhenti apabila pengguna menggunakan fungsi 'exit'.
'''
# Kamus
'''
    parser : argparse.ArgumentParser
    args   : argparse.Namespace
    dfuser, dfgame, dfriwayat, dfkepemilikan : matrix of string
    action : string
    role   : string
    inputFolder : string
    folder : string
    index  : int
    id     : int
    program, logged, result : bool
'''

# Algoritma
import argparse

from pkg_resources import require
from kerangajaib import kerangajaib
from tictactoe import *
from F2_F7 import *
from F8_F13 import *
from F14_F17 import *


# Program Utama
program = False                 # variabel program adalah syarat untuk menjalankan program

parser = argparse.ArgumentParser(description="Program Binomo")
parser.add_argument('folder', default = "", type=str, help="Nama folder yang ingin dibuka.")
args = parser.parse_args()

# $python main.py main_save

if __name__ == '__main__':
    # Menjalankan fungsi load terlebih dahulu
    # Dilakukan cek apakah terdapat nama folder yang diinputkan atau tidak
    inputFolder = args.folder

    folder = load(inputFolder)
    if (folder != None):
        program = True              # Program akan dimulai bila terdapat folder yang akan digunakan

        # Program dibawha ini hanya dijalankan apabila folder != None
        # Inisasi Data yang akan dipakai
        # Saat pertama kali pembacaan, program akan membaca save data pada folder 'main save'
        dfuser = csvtolist("user",6,folder)
        dfgame = csvtolist("game",6,folder)
        dfriwayat = csvtolist("riwayat",5,folder)
        dfkepemilikan = csvtolist("kepemilikan", 2,folder)

        while (program == True):            # Pengaktifan cara kerja program
            print("========================================================================================")
            print("Ketik 'help' untuk melihat perintah yang dapat dilakukan.")
            action = input("Silahkan ketikkan perintah: ").lower()
            logged = False              # Variabel yang menjelaskan apakah pengguna sudah login atau belum
            role = 'guest'                # Jika belum melakukan login, role yang diberikan adalah 'guest'
            if (action == 'login'):
                index = login(dfuser)
                if (index == None):
                    logged = False
                else :
                    logged = True

                while(logged == True):      # Pengguna sudah masuk ke suatu akun
                    print("========================================================================================")
                    id = dfuser[index][0]                                               # Kolom index 0 adalah kolom dimana id disimpan
                    role = dfuser[index][4]                                             # Kolom index 4 adalah kolom dimana role disimpan
                    print("User ID  :", id)
                    print("Nama     :", dfuser[index][2])                               # Kolom index 2 adalah kolom dimana nama disimpan
                    print("Role     :", role)
                    print("Saldo    :", dfuser[index][5])
                    

                    # Menanyakan kembali pengguna, tindakan yang akan dilakukan
                    action = input("Tindakan apa yang akan dilakukan: ").lower()

                    # F02 Jika input adalah register
                    if (action == 'register'):
                        if (role == 'admin'):   
                            dfuser = register(dfuser)                       # List dfuser diubah dengan dfuser gabungan yang baru
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")

                    # F03 Jika action adalah login
                    elif (action == 'login'):
                        print("Anda sedang menggunakan akun dengan username '"+dfuser[index][1]+"'.")         # username disimpan pada data kolom index 1
                        print("Silakan logout terlebih dahulu untuk melakukan login menggunakan akun lain.")

                    # F03 Jika action adalah logout
                    elif (action == 'logout'):
                        result = logout(dfuser, index)      
                        if (result == True):            # Jika pengguna ingin keluar dari akunnya, maka variabel logged menjadi False
                            logged = False

                    # F04 Jika action adalah tambah_game
                    elif (action == "tambah_game"):
                        if (role == 'admin'):
                            dfgame = tambah_game(dfgame)
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")

                    # F05 Jika action adalah ubah_game
                    elif (action == "ubah_game"):
                        if (role == 'admin'):
                            dfgame = ubah_game(dfgame)
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")

                    # F06 Jika action adalah ubah stock game
                    elif (action == 'ubah_stok'):
                        if (role == 'admin'):
                            ubah_stok(dfgame)
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")
                    
                    # F07 Jika action adalah list_game_toko
                    elif (action == 'list_game_toko'):
                        list_game_toko(dfgame)
                        
                    # F08 Jika action adalah buy game
                    elif (action == 'buy_game'):
                        if (role == 'admin'):
                            print("Maaf, anda harus menjadi user untuk melakukan hal tersebut.")
                        else:
                            dfuser, dfkepemilikan, dfriwayat = buy_game(dfuser, dfgame, dfkepemilikan, dfriwayat, id, index)
                    
                    # F09 Jika action adalah list_game
                    elif (action == 'list_game'):
                        if (role == 'admin'):
                            print("Maaf, anda harus menjadi user untuk melakukan hal tersebut.")
                        else:
                            list_game(dfgame, dfkepemilikan, id)
                            
                    # F10 Jika action adalah search_my_game
                    elif (action == 'search_my_game'):
                        if (role == 'admin'):
                            print("Maaf, anda harus menjadi user untuk melakukan hal tersebut.")
                        else:
                            search_my_game(dfgame , dfkepemilikan, id)
                    
                    # F11 Jika action adalah search_game_at_store search_game_at_store(dfgame)
                    elif (action == 'search_game_at_store'):
                        search_game_at_store(dfgame)
                    
                    # F12 Jika action adalah topup
                    elif (action == 'topup'):
                        if (role == 'admin'):
                            dfuser = topup(dfuser)
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")
                        
                    # F13 Jika action adalah riwayat
                    elif (action == 'riwayat'):
                        if (role == 'admin'):
                            print("Maaf, anda harus menjadi user untuk melakukan hal tersebut.")
                        else:
                            riwayat(id, dfriwayat)
                    
                    # F14 Jika action adalah help
                    elif (action == 'help'):
                        help(role)

                    # F16 Jika action adalah save:
                    elif (action == 'save'):
                        save(dfuser, dfgame, dfriwayat, dfkepemilikan)

                    # F17 Jika action adalah exit
                    elif (action == 'exit'):
                        if (exitprogram() == 'y'):
                            save(dfuser, dfgame, dfriwayat, dfkepemilikan)
                            program = False
                            logged = False
                        else :
                            program = False
                            logged = False
                    
                    # Jika action adalah print
                    elif (action == 'print'):
                        if (role == 'admin'):
                            printdataframe(dfuser,dfgame,dfriwayat,dfkepemilikan)
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")
                    
                    # Jika action adalah sort
                    elif (action == 'sort'):
                        if (role == 'admin'):
                            dfuser, dfgame, dfriwayat, dfkepemilikan = sortdataframe(dfuser, dfgame, dfriwayat, dfkepemilikan)
                        else:
                            print("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.")

                    # B02 Memainkan permainan kerang ajaib
                    elif(action == 'kerangajaib'):
                        kerangajaib()

                    # B03 Memainkan permainan tictactoe
                    elif(action == 'tictactoe'):
                        tictactoe()

                    # Input pengguna merupakan fungsi yang tidak dapat diproses
                    else:
                        print("Maaf perintah tersebut tidak dapat diproses.")

            # F14 Jika action adalah help
            elif (action == 'help'):
                help(role)

            # B02 Melakukan permainan kerang ajaib tanpa melakukan login
            elif (action == 'kerangajaib'):
                    kerangajaib()
            # B03 Melakukan permainan tictactoe tanpa melakukan login
            elif (action == 'tictactoe'):
                    tictactoe()
            # F17 Jika action adalah exit
            elif (action == 'exit'):
                    program = False
            else :                              # pengguna tidak menginputkan 'login'
                print('Maaf, anda harus login terlebih dahulu untuk mengirim perintah selain "login".')





