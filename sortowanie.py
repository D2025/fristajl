# importy
import csv, sqlite3

# ogarnianie SQL
con = sqlite3.connect('bitwer.db')

cur = con.cursor()


# stworzona tablica
cur.execute("DROP TABLE IF EXISTS wyniki")
cur.execute("CREATE TABLE IF NOT EXISTS wyniki (ksywa_1 text, ksywa_2 text, wynik int, dzień int, miesiąc int, rok int, organizator text)")
con.commit()


# przepisuje dane z pliku csv do bazy danych sqlite
with open('wyniki.csv', 'r', encoding="UTF-16") as file:
  csvFile = csv.reader(file)

  next(csvFile)

  for line in csvFile:
    cur.execute("INSERT INTO wyniki VALUES(?, ?, 1, ?, ?, ?, ?)", [line[0], line[1], int(line[3]), int(line[4]), int(line[5]), line[6]])
    con.commit()


# sortuje dane i przepisuje je z powrotem do plliku csc
with open("wyniki_sorted.csv", 'a', encoding="UTF-16") as file:
  cur.execute("SELECT * FROM wyniki ORDER BY rok ASC, miesiąc ASC, dzień ASC")
  fetched = cur.fetchall()
  for line in fetched:
    file.write(f"{line[0]},{line[1]},1,{line[3]},{line[4]},{line[5]},{line[6]}\n")
