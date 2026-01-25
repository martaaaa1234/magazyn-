import streamlit as st
from supabase import create_client
import pandas as pd

# Inicjalizacja połączenia z Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def get_supabase():
    return create_client(url, key)

supabase = get_supabase()

st.set_page_config(page_title="Magazyn Supabase", layout="wide")
st.title("📦 System Zarządzania Magazynem")

# --- ZAKŁADKI ---
tab_stock, tab_cats, tab_prods = st.tabs(["📊 Stan Magazynowy", "📂 Kategorie", "🍎 Dodaj/Usuń"])

# --- TAB 1: STAN MAGAZYNOWY ---
with tab_stock:
    st.header("Aktualny Stan Magazynowy")
    # Pobieranie danych z joinem do kategorii
    response = supabase.table("produkty").select("id, nazwa, liczba, cena, kategorie(nazwa)").execute()
    
    if response.data:
        df = pd.json_normalize(response.data)
        df.columns = ['ID', 'Nazwa Produktu', 'Liczba', 'Cena', 'Kategoria']
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Magazyn jest pusty.")

# --- TAB 2: ZARZĄDZANIE KATEGORIAMI ---
with tab_cats:
    st.header("Kategorie")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nowa Kategoria")
        with st.form("cat_form"):
            c_name = st.text_input("Nazwa")
            c_desc = st.text_area("Opis")
            if st.form_submit_button("Dodaj"):
                supabase.table("kategorie").insert({"nazwa": c_name, "opis": c_desc}).execute()
                st.success("Dodano kategorię!")
                st.rerun()

    with col2:
        st.subheader("Usuń Kategorię")
        res_c = supabase.table("kategorie").select("id, nazwa").execute()
        if res_c.data:
            df_c = pd.DataFrame(res_c.data)
            st.dataframe(df_c, use_container_width=True)
            id_to_del = st.number_input("Wpisz ID do usunięcia", min_value=1, key="del_cat_id")
            if st.button("Usuń"):
                supabase.table("kategorie").delete().eq("id", id_to_del).execute()
                st.rerun()

# --- TAB 3: DODAWANIE/USUWANIE PRODUKTÓW ---
with tab_prods:
    st.header("Zarządzanie Produktami")
    
    # Pobranie kategorii do listy rozwijanej
    cats_data = supabase.table("kategorie").select("id, nazwa").execute()
    
    if cats_data.data:
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Nowy Produkt")
            with st.form("prod_form"):
                p_name = st.text_input("Nazwa produktu")
                p_count = st.number_input("Ilość", min_value=0, step=1)
                p_price = st.number_input("Cena", min_value=0.0)
                
                cat_map = {c['nazwa']: c['id'] for c in cats_data.data}
                p_cat = st.selectbox("Kategoria", options=list(cat_map.keys()))
                
                if st.form_submit_button("Dodaj produkt"):
                    new_prod = {
                        "nazwa": p_name,
                        "liczba": p_count,
                        "cena": p_price,
                        "kategoria_id": cat_map[p_cat]
                    }
                    supabase.table("produkty").insert(new_prod).execute()
                    st.success("Produkt dodany!")
                    st.rerun()
        
        with col4:
            st.subheader("Usuń Produkt")
            prod_id_del = st.number_input("ID produktu do usunięcia", min_value=1)
            if st.button("Usuń produkt"):
                supabase.table("produkty").delete().eq("id", prod_id_del).execute()
                st.rerun()
    else:
        st.warning("Najpierw dodaj przynajmniej jedną kategorię!")

