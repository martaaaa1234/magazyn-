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
