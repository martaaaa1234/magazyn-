import streamlit as st
import time

# Używamy zwykłej listy do przechowywania "towarów".
# WAŻNE: W Streamlit, jeśli nie używasz st.session_state (o co prosiłeś)
# lub trwałego zapisu (plik/baza danych), ta lista będzie resetowana
# za każdym razem, gdy użytkownik wejdzie w interakcję z aplikacją
# (np. kliknie przycisk "Dodaj" lub "Usuń").

# Inicjalizacja listy w kontekście globalnym (lub przynajmniej przed wywołaniem funkcji)
# W tym prostym przypadku, po każdej interakcji lista zostanie zresetowana.
# Aby dane się utrzymały bez użycia st.session_state, trzeba by umieścić
# listę w st.session_state, ale na prośbę użytkownika tego unikamy.
towary_magazynu = ["Laptop Dell", "Monitor LG", "Myszka Logitech", "Klawiatura Mechaniczna"]

## --- Funkcje operacyjne ---

def dodaj_towar(nazwa_towaru):
    """Dodaje towar do listy."""
    if nazwa_towaru and nazwa_towaru not in towary_magazynu:
        towary_magazynu.append(nazwa_towaru)
        st.success(f"Dodano towar: **{nazwa_towaru}**")
        time.sleep(0.5) # Krótka pauza, aby użytkownik zobaczył komunikat
        # st.experimental_rerun() # Opcjonalnie: wymuszenie przeładowania dla natychmiastowej aktualizacji
    elif nazwa_towaru in towary_magazynu:
        st.warning(f"Towar **{nazwa_towaru}** jest już w magazynie.")
    else:
        st.error("Wpisz nazwę towaru do dodania.")

def usun_towar(nazwa_towaru):
    """Usuwa towar z listy."""
    if nazwa_towaru in towary_magazynu:
        towary_magazynu.remove(nazwa_towaru)
        st.success(f"Usunięto towar: **{nazwa_towaru}**")
        time.sleep(0.5)
        # st.experimental_rerun()
    else:
        st.error(f"Nie znaleziono towaru **{nazwa_towaru}** w magazynie.")

## --- Interfejs Streamlit ---

st.set_page_config(page_title="Prosty Magazyn", layout="centered")

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("⚠️ **Uwaga:** Dane w tym magazynie **nie są zapisywane**. Po każdej interakcji lub odświeżeniu strony wracają do wartości początkowych.")

# 1. Sekcja dodawania towaru
st.header("➕ Dodaj Towar")
with st.form("dodaj_formularz", clear_on_submit=True):
    nowy_towar = st.text_input("Nazwa Towaru", key="input_dodaj")
    submitted_add = st.form_submit_button("Dodaj do Magazynu")
    
    if submitted_add:
        dodaj_towar(nowy_towar.strip())

# 2. Sekcja usuwania towaru
st.header("➖ Usuń Towar")
with st.form("usun_formularz", clear_on_submit=True):
    # Używamy selectbox, aby wybrać z listy, która jest aktualnie w pamięci
    towar_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia",
        options=towary_magazynu,
        key="select_usun"
    )
    submitted_delete = st.form_submit_button("Usuń z Magazynu")

    if submitted_delete:
        usun_towar(towar_do_usuniecia)

st.divider()

# 3. Aktualny stan magazynu
st.header("📋 Stan Magazynu")

if towary_magazynu:
    # Wyświetlenie listy towarów jako tabeli dla lepszej czytelności
    st.dataframe(
        {"ID": list(range(1, len(towary_magazynu) + 1)), "Nazwa Towaru": towary_magazynu},
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Magazyn jest pusty.")

st.markdown(f"**Liczba unikalnych towarów:** `{len(towary_magazynu)}`")

# Po każdej interakcji, aplikacja Streamlit przeładowuje się.
# Bez st.session_state lista 'towary_magazynu' zostanie zainicjalizowana
# od nowa na początku pliku, przywracając stan początkowy.
import streamlit as st
# import time # Można usunąć, jeśli nie używamy już time.sleep

# Inicjalizacja listy towarów (pamiętaj: resetuje się przy każdej interakcji)
towary_magazynu = ["Laptop Dell", "Monitor LG", "Myszka Logitech", "Klawiatura Mechaniczna"]

## --- Funkcje operacyjne ---

def dodaj_towar(nazwa_towaru):
    """Dodaje towar do listy i zwraca status operacji."""
    if nazwa_towaru and nazwa_towaru not in towary_magazynu:
        towary_magazynu.append(nazwa_towaru)
        return True, f"Dodano towar: **{nazwa_towaru}**"
    elif nazwa_towaru in towary_magazynu:
        return False, f"Towar **{nazwa_towaru}** jest już w magazynie."
    else:
        return False, "Wpisz nazwę towaru do dodania."

def usun_towar(nazwa_towaru):
    """Usuwa towar z listy i zwraca status operacji."""
    if nazwa_towaru in towary_magazynu:
        towary_magazynu.remove(nazwa_towaru)
        return True, f"Usunięto towar: **{nazwa_towaru}**"
    else:
        return False, f"Nie znaleziono towaru **{nazwa_towaru}** w magazynie."

## --- Interfejs Streamlit ---

st.set_page_config(page_title="Prosty Magazyn", layout="centered")

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("⚠️ **Uwaga:** Dane w tym magazynie **nie są zapisywane**. Po każdej interakcji lub odświeżeniu strony wracają do wartości początkowych.")

# 1. Sekcja dodawania towaru
st.header("➕ Dodaj Towar")
with st.form("dodaj_formularz", clear_on_submit=True):
    nowy_towar = st.text_input("Nazwa Towaru", key="input_dodaj")
    submitted_add = st.form_submit_button("Dodaj do Magazynu")
    
    if submitted_add:
        # Wywołanie funkcji i obsługa wyniku
        sukces, komunikat = dodaj_towar(nowy_towar.strip())
        
        # Wyświetlanie komunikatu o operacji
        if sukces:
            st.success(komunikat)
            st.toast(komunikat, icon="✅") # Dodatkowe powiadomienie na ekranie
        else:
            if "jest już w magazynie" in komunikat:
                 st.warning(komunikat)
            else:
                 st.error(komunikat)

# 2. Sekcja usuwania towaru
st.header("➖ Usuń Towar")
with st.form("usun_formularz", clear_on_submit=False): 
    # clear_on_submit=False, aby wybrany element pozostał widoczny, choć i tak lista się resetuje
    
    # Używamy selectbox, aby wybrać z listy, która jest aktualnie w pamięci
    towar_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia",
        options=towary_magazynu,
        key="select_usun"
    )
    submitted_delete = st.form_submit_button("Usuń z Magazynu")

    if submitted_delete:
        # Wywołanie funkcji i obsługa wyniku
        sukces, komunikat = usun_towar(towar_do_usuniecia)
        
        # Wyświetlanie komunikatu o operacji
        if sukces:
            st.success(komunikat)
            st.toast(komunikat, icon="🗑️") # Dodatkowe powiadomienie na ekranie
        else:
            st.error(komunikat)

st.divider()

# 3. Aktualny stan magazynu
st.header("📋 Stan Magazynu")

if towary_magazynu:
    # Wyświetlenie listy towarów jako tabeli
    st.dataframe(
        {"ID": list(range(1, len(towary_magazynu) + 1)), "Nazwa Towaru": towary_magazynu},
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Magazyn jest pusty.")

st.markdown(f"**Liczba unikalnych towarów:** `{len(towary_magazynu)}`")
import streamlit as st

# --- Definicja Stanu Magazynu (Bez sesji/pliku, więc resetuje się) ---

# Lista towarów, które FAKTYCZNIE są w magazynie
towary_magazynu = ["Laptop Dell", "Monitor LG", "Klawiatura Mechaniczna"]

# Lista towarów, które POWINNY być w magazynie (Stan docelowy/standardowy)
stan_magazynu_docelowy = {
    "Laptop Dell", 
    "Monitor LG", 
    "Myszka Logitech", # <-- Ten towar jest zdefiniowany jako docelowy, ale nie ma go w 'towary_magazynu'
    "Klawiatura Mechaniczna",
    "Podkładka Gamingowa" # <-- Ten też jest zdefiniowany jako docelowy
}

# --- Funkcje operacyjne ---

def dodaj_towar(nazwa_towaru):
    """Dodaje towar do listy i zwraca status operacji."""
    if nazwa_towaru and nazwa_towaru not in towary_magazynu:
        towary_magazynu.append(nazwa_towaru)
        return True, f"Dodano towar: **{nazwa_towaru}**"
    elif nazwa_towaru in towary_magazynu:
        return False, f"Towar **{nazwa_towaru}** jest już w magazynie."
    else:
        return False, "Wpisz nazwę towaru do dodania."

def usun_towar(nazwa_towaru):
    """Usuwa towar z listy i zwraca status operacji."""
    if nazwa_towaru in towary_magazynu:
        towary_magazynu.remove(nazwa_towaru)
        return True, f"Usunięto towar: **{nazwa_towaru}**"
    else:
        return False, f"Nie znaleziono towaru **{nazwa_towaru}** w magazynie."

def sprawdz_braki_magazynowe():
    """Porównuje stan docelowy z faktycznym i zwraca listę braków."""
    # Konwertujemy listę aktualnych towarów na zbiór (set) dla szybszego porównania
    aktualny_stan_set = set(towary_magazynu)
    
    # Odejmowanie zbiorów: docelowy - aktualny = braki
    braki = stan_magazynu_docelowy.difference(aktualny_stan_set)
    
    # Sortujemy dla ładniejszego wyświetlania
    return sorted(list(braki))

# --- Interfejs Streamlit ---

st.set_page_config(page_title="Prosty Magazyn", layout="centered")

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("⚠️ **Uwaga:** Dane w tym magazynie **nie są zapisywane** (resetują się do stanu początkowego).")

# --- 4. Sekcja Analizy Braków Magazynowych (NOWOŚĆ) ---
braki_magazynowe = sprawdz_braki_magazynowe()

st.header("🚨 Braki Magazynowe")

if braki_magazynowe:
    st.error(f"Wykryto **{len(braki_magazynowe)}** braków zgodnie ze stanem docelowym:")
    
    # Wyświetlanie braków jako nieuporządkowanej listy
    braki_lista = "\n".join([f"- **{brak}**" for brak in braki_magazynowe])
    st.markdown(braki_lista)
    
    # Opcjonalnie: Przycisk, który automatycznie dodaje brakujący towar do formularza dodawania
    if st.button("Uzupełnij pierwszy brak: " + braki_magazynowe[0]):
        # W Streamlit to działa głównie jako informacja, 
        # bo musielibyśmy użyć session_state do faktycznej pre-populacji inputa.
        # Bez session_state, to jest tylko demonstracja intencji.
        st.info(f"Teraz możesz dodać **{braki_magazynowe[0]}** w sekcji 'Dodaj Towar'.")
else:
    st.success("Brak braków! Magazyn jest zgodny ze stanem docelowym.")

st.divider()

# --- 1. Sekcja dodawania towaru ---
st.header("➕ Dodaj Towar")
with st.form("dodaj_formularz", clear_on_submit=True):
    nowy_towar = st.text_input("Nazwa Towaru", key="input_dodaj")
    submitted_add = st.form_submit_button("Dodaj do Magazynu")
    
    if submitted_add:
        sukces, komunikat = dodaj_towar(nowy_towar.strip())
        if sukces:
            st.success(komunikat)
            st.toast(komunikat, icon="✅")
        else:
            if "jest już w magazynie" in komunikat:
                 st.warning(komunikat)
            else:
                 st.error(komunikat)

# --- 2. Sekcja usuwania towaru ---
st.header("➖ Usuń Towar")
with st.form("usun_formularz", clear_on_submit=False): 
    # Używamy selectbox, aby wybrać z listy aktualnie w pamięci
    towar_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia",
        options=towary_magazynu,
        key="select_usun"
    )
    submitted_delete = st.form_submit_button("Usuń z Magazynu")

    if submitted_delete:
        sukces, komunikat = usun_towar(towar_do_usuniecia)
        if sukces:
            st.success(komunikat)
            st.toast(komunikat, icon="🗑️")
        else:
            st.error(komunikat)

st.divider()

# --- 3. Aktualny stan magazynu ---
st.header("📋 Stan Magazynu Rzeczywisty")

if towary_magazynu:
    st.dataframe(
        {"ID": list(range(1, len(towary_magazynu) + 1)), "Nazwa Towaru": towary_magazynu},
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Magazyn jest pusty.")

st.markdown(f"**Liczba unikalnych towarów (Rzeczywisty):** `{len(towary_magazynu)}`")
st.markdown(f"**Liczba unikalnych towarów (Docelowy):** `{len(stan_magazynu_docelowy)}`")
Rozumiem. Aby pokazać liczbę sztuk, musimy przejść od prostej listy (list) przechowującej tylko nazwy, do bardziej złożonej struktury danych, która przechowuje zarówno nazwę towaru, jak i jego ilość. Najlepszą strukturą do tego będzie słownik Pythona (dict), gdzie kluczem jest nazwa towaru, a wartością jest jego ilość.

Ponownie, zgodnie z Twoją prośbą, będziemy nadal unikać użycia st.session_state i trwałego zapisu.

✍️ Zmodyfikowany kod aplikacji Streamlit (app.py) z Liczbą Sztuk
Wprowadzam następujące zmiany:

Zmieniam towary_magazynu na słownik: {"nazwa_towaru": ilość_sztuk}.

Zmieniam stan_magazynu_docelowy na słownik, aby mógł określać wymaganą ilość.

Aktualizuję funkcje dodaj_towar i usun_towar, aby przyjmowały i modyfikowały ilość sztuk.

Aktualizuję sekcję "Braki Magazynowe", aby uwzględniała braki ilościowe (brakuje sztuk) i braki towarowe (towar jest potrzebny, ale go nie ma).

Plik app.py (Nowa wersja z ilościami)
Python

import streamlit as st
from collections import defaultdict # Użyjemy do łatwiejszego zarządzania stanem

# --- Definicja Stanu Magazynu (Słowniki przechowujące {Nazwa: Ilość}) ---

# Słownik towarów, które FAKTYCZNIE są w magazynie: {Nazwa Towaru: Ilość Sztuk}
# WAŻNE: W Streamlit, to się resetuje przy każdej interakcji.
towary_magazynu = {
    "Laptop Dell": 5, 
    "Monitor LG": 12, 
    "Klawiatura Mechaniczna": 8
}

# Słownik towarów, które POWINNY być w magazynie (Stan docelowy/standardowy)
stan_magazynu_docelowy = {
    "Laptop Dell": 10,       # Brakuje 5 sztuk
    "Monitor LG": 12,        # Stan OK
    "Myszka Logitech": 15,   # Brakuje 15 sztuk (towar nieobecny)
    "Klawiatura Mechaniczna": 5, # Stan OK (jest 8, a potrzeba 5)
    "Podkładka Gamingowa": 20  # Brakuje 20 sztuk (towar nieobecny)
}

## --- Funkcje operacyjne ---

def dodaj_towar(nazwa_towaru, ilosc):
    """Dodaje lub zwiększa ilość towaru w magazynie."""
    nazwa_towaru = nazwa_towaru.strip()
    
    if not nazwa_towaru or ilosc <= 0:
        return False, "Wpisz poprawną nazwę i ilość (większą niż 0)."

    # Używamy defaultdict, aby tymczasowo pracować na kopii i łatwo dodawać nowe elementy
    temp_magazyn = defaultdict(int, towary_magazynu)
    
    poprzednia_ilosc = temp_magazyn[nazwa_towaru]
    temp_magazyn[nazwa_towaru] += ilosc
    
    # Aktualizujemy globalny słownik
    # W tym prostym modelu, musimy nadpisać globalny słownik
    # Rzeczywisty magazyn nie potrzebuje defaultdict, ale to upraszcza logikę
    towary_magazynu.clear()
    towary_magazynu.update(dict(temp_magazyn))

    if poprzednia_ilosc == 0:
        return True, f"Dodano **{ilosc} szt.** nowego towaru: **{nazwa_towaru}**."
    else:
        return True, f"Zwiększono stan towaru **{nazwa_towaru}** o **{ilosc} szt.** (Nowy stan: {temp_magazyn[nazwa_towaru]})."

def usun_towar(nazwa_towaru, ilosc_do_usuniecia):
    """Usuwa lub zmniejsza ilość towaru w magazynie."""
    nazwa_towaru = nazwa_towaru.strip()
    
    if not nazwa_towaru or ilosc_do_usuniecia <= 0:
        return False, "Wybierz towar i podaj poprawną ilość do usunięcia (większą niż 0)."

    if nazwa_towaru not in towary_magazynu:
        return False, f"Nie znaleziono towaru **{nazwa_towaru}** w magazynie."

    aktualna_ilosc = towary_magazynu[nazwa_towaru]

    if ilosc_do_usuniecia > aktualna_ilosc:
        return False, f"Błąd: Chcesz usunąć {ilosc_do_usuniecia} szt., ale jest tylko {aktualna_ilosc} szt. towaru **{nazwa_towaru}**."
    
    if ilosc_do_usuniecia == aktualna_ilosc:
        # Całkowite usunięcie towaru z magazynu
        del towary_magazynu[nazwa_towaru]
        return True, f"Usunięto **ostatnie {ilosc_do_usuniecia} szt.** towaru: **{nazwa_towaru}** (Usunięto z magazynu)."
    else:
        # Zmniejszenie ilości
        towary_magazynu[nazwa_towaru] -= ilosc_do_usuniecia
        nowa_ilosc = towary_magazynu[nazwa_towaru]
        return True, f"Usunięto **{ilosc_do_usuniecia} szt.** towaru **{nazwa_towaru}** (Pozostało: {nowa_ilosc})."

def sprawdz_braki_magazynowe():
    """Porównuje stan docelowy z faktycznym i zwraca listę braków ilościowych/towarowych."""
    braki = []
    
    for towar, ilosc_docelowa in stan_magazynu_docelowy.items():
        ilosc_aktualna = towary_magazynu.get(towar, 0) # 0 jeśli towaru nie ma w magazynie
        
        if ilosc_aktualna < ilosc_docelowa:
            brakujaca_ilosc = ilosc_docelowa - ilosc_aktualna
            braki.append({
                "Towar": towar,
                "Brak": brakujaca_ilosc,
                "Aktualnie": ilosc_aktualna,
                "Docelowo": ilosc_docelowa
            })
            
    return braki

# --- Interfejs Streamlit ---

st.set_page_config(page_title="Prosty Magazyn", layout="centered")

st.title("📦 Prosty Magazyn (Streamlit) z Ilościami")
st.caption("⚠️ **Uwaga:** Magazyn używa ilości, ale dane **resetują się** do stanu początkowego przy każdej interakcji.")

# --- 4. Sekcja Analizy Braków Magazynowych ---
braki_magazynowe = sprawdz_braki_magazynowe()

st.header("🚨 Braki Magazynowe")

if braki_magazynowe:
    st.error(f"Wykryto **{len(braki_magazynowe)}** rodzajów braków towarowych:")
    
    # Tworzenie DataFrame dla lepszej wizualizacji braków
    import pandas as pd
    df_braki = pd.DataFrame(braki_magazynowe)
    df_braki = df_braki.rename(columns={
        "Brak": "Brakuje Sztuk",
        "Aktualnie": "Stan Rzeczywisty",
        "Docelowo": "Stan Docelowy"
    })
    
    st.dataframe(df_braki, hide_index=True, use_container_width=True)
    
else:
    st.success("Brak braków! Magazyn jest zgodny ze stanem docelowym lub go przewyższa.")

st.divider()

# --- 1. Sekcja dodawania towaru ---
st.header("➕ Dodaj/Uzupełnij Towar")
with st.form("dodaj_formularz", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nowy_towar = st.text_input("Nazwa Towaru", key="input_dodaj")
    with col2:
        ilosc_dodania = st.number_input("Ilość Sztuk do Dodania", min_value=1, value=1, step=1, key="ilosc_dodaj")
        
    submitted_add = st.form_submit_button("Dodaj do Magazynu")
    
    if submitted_add:
        sukces, komunikat = dodaj_towar(nowy_towar, ilosc_dodania)
        if sukces:
            st.success(komunikat)
            st.toast(komunikat, icon="✅")
        else:
            st.error(komunikat)

# --- 2. Sekcja usuwania towaru ---
st.header("➖ Usuń Towar/Zmniejsz Ilość")
with st.form("usun_formularz", clear_on_submit=False): 
    col3, col4 = st.columns(2)
    
    # Lista kluczy (nazw towarów) jest dynamiczna
    towary_keys = list(towary_magazynu.keys())
    
    with col3:
        towar_do_usuniecia = st.selectbox(
            "Wybierz towar do usunięcia/zmniejszenia",
            options=towary_keys,
            key="select_usun"
        )
    
    # Automatyczne ustawienie maksymalnej ilości do usunięcia
    max_ilosc = towary_magazynu.get(towar_do_usuniecia, 0)
    
    with col4:
        ilosc_do_usuniecia = st.number_input(
            "Ilość Sztuk do Usunięcia", 
            min_value=1, 
            max_value=max_ilosc if max_ilosc > 0 else 1, 
            value=1, 
            step=1, 
            key="ilosc_usun"
        )

    submitted_delete = st.form_submit_button("Usuń z Magazynu")

    if submitted_delete:
        sukces, komunikat = usun_towar(towar_do_usuniecia, ilosc_do_usuniecia)
        if sukces:
            st.success(komunikat)
            st.toast(komunikat, icon="🗑️")
        else:
            st.error(komunikat)

st.divider()

# --- 3. Aktualny stan magazynu ---
st.header("📋 Stan Magazynu Rzeczywisty (Ilość Sztuk)")

if towary_magazynu:
    # Przygotowanie danych do wyświetlenia jako DataFrame
    dane_magazynu = [{
        "Nazwa Towaru": nazwa, 
        "Ilość Sztuk": ilosc
    } for nazwa, ilosc in towary_magazynu.items()]
    
    df_magazyn = pd.DataFrame(dane_magazynu)
    
    st.dataframe(
        df_magazyn,
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Magazyn jest pusty.")

st.markdown(f"**Liczba unikalnych towarów:** `{len(towary_magazynu)}`")

