# importy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

# ogarnianie rzeczy
driver = webdriver.Edge(executable_path=r'C:\Users\Dawid\Downloads\edgedriver_win64\msedgedriver.exe')

datowanie = {"styczeń": 1, "luty": 2, "marzec": 3 , "kwiecień": 4, "maj": 5, "czerwiec": 6, "lipiec": 7, "sierpień": 8, "wrzesień": 9, "październik": 10, "listopad": 11, "grudzień": 12}




# główny silnik
for a in range(1, 853):

    # pobieramy stronę
    driver.get(f"https://bitwer.pl/wydarzenia/{a}")

    # znajdowanie daty - jeśli nie znajdzie to pisze w konsoli "nie znaleziono daty", zwykle oznacza to, że pod danym linkiem zwyczajnie nie było żadnej bitwy
    try:

        # rzeczy
        data = driver.find_element(By.CLASS_NAME, "caption.grey--text.d-flex.justify-center.justify-md-start")
        data = data.text
        data_lista = data.split(" ")
        data_lista[1] = int(datowanie[data_lista[1]])

        # gówno
        dzień = int(data_lista[0])
        miesiąc = int(data_lista[1])
        rok = int(data_lista[2])
    except:
        print("nie znaleziono daty")

    # próbuje znaleźć organizatora, jak nie znajdzie to do pliku wpisze 'NULL'
    try:
        organizator = driver.find_element(By.CLASS_NAME, "text-decoration-none.font-weight-medium.indigo--text.text--darken-4")
        organizator = organizator.text
    except:
        organizator = "NULL"


    # uzyskuje tablicę wszystkich przegranych z strony (bo algorytm działa tak, że zbiera wszystkich wygranych i przegranych i potem dopasowuje, że pierwszy przegrany musiał przegrać z pierwszym wygranym, to oczywiście nie pozwala na działanie z pojedynkami gdzie jest nieparzysta liczba zawodników)
    temp = []
    przegrani = driver.find_elements(By.CLASS_NAME, "grey--text.text--darken-1.text-truncate")
    for obj in przegrani:
        temp.append(obj.text)
    przegrani = temp.copy()

    # uzyskuje tablicę wszystkich wygranych z strony
    temp = []
    wygrani = driver.find_elements(By.CLASS_NAME, "font-weight-medium.text-truncate.text-grevo")
    for obj in wygrani:
        temp.append(obj.text)
    wygrani = temp.copy()



    if len(przegrani) == len(wygrani):
        # wpisuje wyniki do pliku csv
        with open("wyniki.csv", 'a', encoding="UTF-16") as wyniki:
            for i in range(len(wygrani)):
                wyniki.write(f"{wygrani[i]},{przegrani[i]},1,{dzień},{miesiąc},{rok},{organizator}\n")

    # jeśli nie ma tyle samo przegranych co wygranych to coś jest źle i nie wpisujemy
    else:
        try:
            print(f"Won't process battle no {a} ({wygrani[0]}; {przegrani[0]})")
        except:
            # jak wypisze pustą linijkę, to chyba znaczy, że pod danym linkiem nie było żadnej bitwy ale chuj wie
            print("")

driver.quit()

