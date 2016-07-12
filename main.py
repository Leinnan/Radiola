#!/usr/bin/python3

#-*- coding: utf-8 -*-
from datetime import datetime 
import time
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Program zarządzający odtwarzaniem muzyki w radioli w CKZiU Więcbork',
                                   epilog='Program stworzony przez Piotra Siuszko.')
parser.add_argument('-d', '--debug', dest='current_only',
                     help='Testowa wersja',
                     action='store_true')
args = parser.parse_args()

debug = parser.parse_args().current_only

# rozmiar terminala
rows, columns = os.popen('stty size', 'r').read().split()

debug = True
current_time = datetime.now();
jest_aktualnie_przerwa = False    


# ascii text
trwa_lekcja_tekst = """\033[31m __         ______     __  __     ______       __     ______    
/\ \       /\  ___\   /\ \/ /    /\  ___\     /\ \   /\  __ \   
\ \ \____  \ \  __\   \ \  _"-.  \ \ \____   _\_\ \  \ \  __ \  
 \ \_____\  \ \_____\  \ \_\ \_\  \ \_____\ /\_____\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/\/_/   \/_____/ \/_____/   \/_/\/_/ 
                                                                \033[0m"""
trwa_przerwa_tekst = """\033[32m
 ______   ______     ______     ______     ______     __     __     ______    
/\  == \ /\  == \   /\___  \   /\  ___\   /\  == \   /\ \  _ \ \   /\  __ \   
\ \  _-/ \ \  __<   \/_/  /__  \ \  __\   \ \  __<   \ \ \/ ".\ \  \ \  __ \  
 \ \_\    \ \_\ \_\   /\_____\  \ \_____\  \ \_\ \_\  \ \__/".~\_\  \ \_\ \_\ 
  \/_/     \/_/ /_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_/   \/_/\/_/ 
                                                                              
\033[0m"""
po_lekcjach_tekst = """\033[32m
 __     __     ______     __         __   __     ______    
/\ \  _ \ \   /\  __ \   /\ \       /\ "-.\ \   /\  ___\   
\ \ \/ ".\ \  \ \ \/\ \  \ \ \____  \ \ \-.  \  \ \  __\   
 \ \__/".~\_\  \ \_____\  \ \_____\  \ \_\\"\_\  \ \_____\ 
  \/_/   \/_/   \/_____/   \/_____/   \/_/ \/_/   \/_____/ 
\033[0m"""
                                                           



# klasa lekcji
class lesson:
    def __init__(self, start_lekcji, koniec_lekcji):
        self.start_lekcji = start_lekcji
        self.koniec_lekcji = koniec_lekcji


# rozpiska lekcji
lekcje = []
lekcje.append(lesson("08:00","08:45"))
lekcje.append(lesson("08:55","09:40"))
lekcje.append(lesson("09:50","10:35"))
lekcje.append(lesson("10:50","11:35"))
lekcje.append(lesson("11:45","12:30"))
lekcje.append(lesson("12:40","13:25"))
lekcje.append(lesson("13:30","14:15"))
lekcje.append(lesson("14:20","15:05"))

# koniec rozpiski lekcji
def leciMuzyka():
    isPlayingMusic = True;
    deadbeef_output = str(os.popen("deadbeef --nowplaying-tf \"%ispaused%\"").read())
    if "1" in deadbeef_output:
        isPlayingMusic = False;
    return isPlayingMusic

def przelaczOdtwarzanie():
    os.system("deadbeef  --toggle-pause")
    
def jestUruchomionyOdtwarzacz():
    uruchomiony = True;
    if not os.popen("ps cax | grep deadbeef").read():
        uruchomiony = False
    return uruchomiony
	
def uruchomOdtwarzacz():
    subprocess.Popen(["deadbeef", ""])

def jestPrzerwa(lekcje_w_funkcji):
    przerwa = True
    for lekcja in lekcje_w_funkcji:

        poczatek_lekcji = current_time.replace(
                                    hour=int(lekcja.start_lekcji[:2]), 
                                    minute=int(lekcja.start_lekcji[3:]), 
                                    second=0, microsecond=0)
        koniec_lekcji = current_time.replace(
                                    hour=int(lekcja.koniec_lekcji[:2]), 
                                    minute=int(lekcja.koniec_lekcji[3:]), 
                                    second=0, microsecond=0)
        if current_time > poczatek_lekcji:
            if current_time < koniec_lekcji:
                for i in lekcje:
                    if i == lekcja:
                        przerwa = False
                        if debug:
                            print("Lekcja nr", end=" ")
                            print(lekcje.index(i) + 1)
    if current_time.hour > 14 or current_time.hour < 7:
        przerwa = False
    return przerwa

# uruchamia odtwarzacz jesli nie jest wlaczony
if not jestUruchomionyOdtwarzacz():
    uruchomOdtwarzacz()

byla_poprzednio_przerwa = not jestPrzerwa(lekcje)
jest_aktualnie_przerwa = True
wpis_do_pliku = '\nPoczatek wpisow od godziny {}:{}\n'.format(str(current_time.hour).zfill(2),str(current_time.minute).zfill(2))
with open('rozpiska.txt', 'a') as plik_tekstowy:
    plik_tekstowy.write(wpis_do_pliku)


while True:
    # czysci ekran
    os.system('cls' if os.name == 'nt' else 'clear')
    byla_poprzednio_przerwa = jest_aktualnie_przerwa
    jest_aktualnie_przerwa = jestPrzerwa(lekcje)
    if byla_poprzednio_przerwa is not jest_aktualnie_przerwa:
        wpis_do_pliku = '{}:{} zmiana na {}\n'.format(str(current_time.hour).zfill(2),str(current_time.minute).zfill(2),jest_aktualnie_przerwa)
        with open('rozpiska.txt', 'a') as plik_tekstowy:
            plik_tekstowy.write(wpis_do_pliku)
    
    tytulowy_tekst = '\033[93m{: <1} dzień tygodnia\t\033[0m{0:02d}:{0:02d}'.format(
                            current_time.weekday() + 1,
                            current_time.hour,
                            current_time.minute)
    print('{: ^{dlugosc}}'.format(tytulowy_tekst, dlugosc = columns))
    if jest_aktualnie_przerwa:
        print("\n\n")
        print('{: ^{dlugosc}}'.format(trwa_przerwa_tekst, dlugosc = columns))
    elif current_time.hour > 15:
        print("\n\n")
        print('{: ^{dlugosc}}'.format(po_lekcjach_tekst, dlugosc = columns))
    else:
        print("\n\n")
        print('{: ^{dlugosc}}'.format(trwa_lekcja_tekst, dlugosc = columns))
    
    # sprawdzamy czy gra muzyka
    if leciMuzyka():
        print('{: ^{dlugosc}}'.format("\033[92mMuzyka jest odtwarzana\033[0m", dlugosc = columns))
        # jesli jest odtwarzana, a nie jest przerwa to zatrzymaj
        if not jest_aktualnie_przerwa or current_time.hour > 14 or current_time.hour < 8:
            przelaczOdtwarzanie()
            print("zatrzymujemy")
    else:
        print('{: ^{dlugosc}}'.format("\033[33mMuzyka jest zatrzymana\033[0m", dlugosc = columns))
        # jesli jest zatrzymana, a jest przerwa to odtwarzaj
        if jest_aktualnie_przerwa and 7 < current_time.hour < 15:
            przelaczOdtwarzanie()
            print("odtwarzamy")
    time.sleep(1)
    current_time = datetime.now();
    if debug:
        current_time = current_time.replace(
                                    hour=current_time.hour-8, 
                                    minute=current_time.minute, 
                                    second=current_time.second, microsecond=0)
