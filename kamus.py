import streamlit as st
import sqlite3
import pandas as pd

# Koneksi ke database SQLite
conn = sqlite3.connect('vocab.db')
cursor = conn.cursor()

# Cek apakah kolom jenis_kata sudah ada di tabel
cursor.execute("PRAGMA table_info(vocab)")
columns = cursor.fetchall()
jenis_kata_exists = any("jenis_kata" in column for column in columns)

# Tambahkan kolom jenis_kata jika belum ada
if not jenis_kata_exists:
    cursor.execute('ALTER TABLE vocab ADD COLUMN jenis_kata TEXT')
    conn.commit()

# Fungsi untuk menambah vocab ke database
def tambah_vocab(kata, arti, jenis_kata, contoh_1, contoh_2, contoh_3):
    cursor.execute('''
    INSERT INTO vocab (kata, arti, jenis_kata, contoh_1, contoh_2, contoh_3)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (kata, arti, jenis_kata, contoh_1, contoh_2, contoh_3))
    conn.commit()

# Fungsi untuk menampilkan tabel vocab
def tampilkan_tabel_vocab(filter_jenis_kata=None):
    cursor.execute('SELECT * FROM vocab')
    data = cursor.fetchall()

    # Cek apakah kolom jenis_kata sudah ada di hasil query
    jenis_kata_exists = any("jenis_kata" in column for column in cursor.description)

    # Jika belum ada, tambahkan kolom jenis_kata ke hasil query
    if not jenis_kata_exists:
        data = [item + ('',) for item in data]

    # Buat DataFrame
    df_columns = ['ID', 'Kata', 'Arti', 'Contoh 1', 'Contoh 2', 'Contoh 3', 'Jenis Kata']
    if not jenis_kata_exists:
        df_columns.remove('Jenis Kata')

    df = pd.DataFrame(data, columns=df_columns)
    df['Arti'] = df['Arti'].apply(lambda x: f"<span style='color:red'>{x}</span>")

    # Filter berdasarkan jenis kata
    if filter_jenis_kata and jenis_kata_exists:
        df = df[df['Jenis Kata'] == filter_jenis_kata]

    # Menggunakan st.markdown() untuk mengizinkan HTML
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

# Page 1: Form Input Vocab
def page_input_vocab():
    st.title("Input Vocab 📄")

    kata = st.text_input("Kata:")
    arti = st.text_input("Arti:")
    contoh_1 = st.text_input("Contoh Kalimat 1:")
    contoh_2 = st.text_input("Contoh Kalimat 2:")
    contoh_3 = st.text_input("Contoh Kalimat 3:")
    jenis_kata = st.selectbox("Jenis Kata:", ["Noun", "Adjektiva", "Verb", "Lainnya"])

    if st.button("Tambah Vocab"):
        tambah_vocab(kata, arti, jenis_kata, contoh_1, contoh_2, contoh_3)
        st.success("Vocab berhasil ditambahkan!")

# Page 2: Tabel Vocab
def page_tabel_vocab():
    st.title("Tabel Vocab 📋")

    # Fitur filter berdasarkan jenis kata
    filter_jenis_kata = st.selectbox("Filter Jenis Kata:", ["Semua", "Noun", "Adjektiva", "Verb", "Lainnya"])

    if filter_jenis_kata != "Semua":
        tampilkan_tabel_vocab(filter_jenis_kata)
    else:
        tampilkan_tabel_vocab()


# Page 2: Tabel Vocab
def page_tabel_vocab():
    st.title("Tabel Vocab 📋")

    # Fitur filter berdasarkan jenis kata
    filter_jenis_kata = st.selectbox("Filter Jenis Kata:", ["Semua", "Noun", "Adjektiva", "Verb", "Lainnya"])

    if filter_jenis_kata != "Semua":
        tampilkan_tabel_vocab(filter_jenis_kata)
    else:
        tampilkan_tabel_vocab()

# Main App
def main():
    st.sidebar.title("Menu🧩")
    page = st.sidebar.radio("Go to", ["Input Vocab", "Tabel Vocab"])

    if page == "Input Vocab":
        page_input_vocab()
    elif page == "Tabel Vocab":
        page_tabel_vocab()

# Menjalankan aplikasi
if __name__ == "__main__":
    main()
