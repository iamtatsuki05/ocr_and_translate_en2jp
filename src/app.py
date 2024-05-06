from io import BytesIO
import shutil
import tempfile
from pathlib import Path

import streamlit as st

from ocr_and_translate_en2jp.genarate_tranrate_df import df_generator

st.title('OCR and Translation App')

uploaded_file = st.file_uploader('Choose a file')
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=Path(uploaded_file.name).suffix
    ) as tmpfile:
        shutil.copyfileobj(uploaded_file, tmpfile)
        uploaded_file_path = tmpfile.name

    max_words = st.number_input(
        'Maximum number of words to process', min_value=1, value=50
    )
    do_shuffle = st.checkbox('Shuffle output')
    seed = (
        st.number_input('Seed for shuffling', min_value=0, value=42)
        if do_shuffle
        else None
    )
    do_clean_noise_data = st.checkbox('Clean noise data', value=True)

    if st.button('Process'):
        df = df_generator(
            uploaded_file_path, max_words, do_shuffle, seed, do_clean_noise_data
        )
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Download data as CSV',
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv',
        )

        # REF: https://qiita.com/nyakiri_0726/items/2ae8cfb926c48072b190
        df.to_excel(buf := BytesIO(), index=False)

        st.download_button(
            label="Download data as Excel",
            data=buf.getvalue(),
            file_name='processed_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
