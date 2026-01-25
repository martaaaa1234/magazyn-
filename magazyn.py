import streamlit as st
from supabase import create_client
import pandas as pd

# Bezpieczne pobieranie kluczy
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("Błąd: Brak kluczy konfiguracyjnych w Secrets!")
    st.stop()

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_connection():
    return create_client(url, key)

supabase = init_connection()

st.title("📦 Manager Magazynu")

# --- ZAKŁADKI ---
tab1, tab2, tab3 = st.tabs(["📊 Stan", "➕ Dodaj", "🗑️ Usuń"])

# 1. STAN MAGAZYNOWY (Zgodnie ze schematem: produkty + kategorie)
with tab1:
    st.header("Aktualne zapasy")
    # Pobieramy produkty i nazwę kategorii przez relację kategoria_id
    res = supabase.table("produkty").select("id, nazwa, liczba, cena, kategorie(nazwa)").execute()
    if res.data:
        df = pd.json_normalize(res.data)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Brak produktów.")

# 2. DODAWANIE (Produkty i Kategorie)
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nowa Kategoria")
        with st.form("cat_form"):
            n_kat = st.text_input("Nazwa kategorii")
            o_kat = st.text_input("Opis")
            if st.form_submit_button("Dodaj kategorię"):
                supabase.table("kategorie").insert({"nazwa": n_kat, "opis": o_kat}).execute()
                st.success("Dodano!")
                st.rerun()

    with col2:
        st.subheader("Nowy Produkt")
        cats = supabase.table("kategorie").select("id, nazwa").execute()
        if cats.data:
            cat_dict = {c['nazwa']: c['id'] for c in cats.data}
            with st.form("prod_form"):
                p_nazwa = st.text_input("Nazwa produktu")
                p_liczba = st.number_input("Ilość", min_value=0)
                p_cena = st.number_input("Cena", min_value=0.0)
                p_kat = st.selectbox("Kategoria", options=list(cat_dict.keys()))
                if st.form_submit_button("Dodaj produkt"):
                    supabase.table("produkty").insert({
                        "nazwa": p_nazwa, 
                        "liczba": p_liczba, 
                        "cena": p_cena, 
                        "kategoria_id": cat_dict[p_kat]
                    }).execute()
                    st.success("Produkt dodany!")
                    st.rerun()

# 3. USUWANIE
with tab3:
    st.subheader("Usuń element")
    del_type = st.radio("Co chcesz usunąć?", ["Produkt", "Kategoria"])
    id_to_del = st.number_input("ID do usunięcia", min_value=1)
    if st.button("Potwierdź usunięcie"):
        table = "produkty" if del_type == "Produkt" else "kategorie"
        supabase.table(table).delete().eq("id", id_to_del).execute()
        st.warning(f"Usunięto z tabeli {table}")
        st.rerun()
