import streamlit as st
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

load_dotenv('.env')

service_endpoint = os.getenv('ENDPOINT')
index_name = os.getenv('INDEX')
key = os.getenv('KEY')

# search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(str(key)))


# def search_content(search_text):
#     contents = []
#     results = search_client.search(search_text=search_text, top=10)
#     for result in results:
#         contents.append(result)
#     return contents


def main():
    keyword = st.text_input('Cari konten')
    search = st.button('Cari', type='primary')
    # if search:
    #     contents = search_content(keyword)
    #     st.session_state['contents'] = contents

    # contents = st.session_state.get('contents', [])
    # if 'id' in st.query_params:
    #     id = st.query_params["id"][0]
    #     st.text(f'id: {id}')

    # else:
    #     if contents:
    #         df = pd.DataFrame(contents)
    #         df = df[['id', 'title', 'image', 'url', 'video', 'content']]

    #         for i, row in df.iterrows():
    #             st.header(row['title'])
    #             col_img, col_content = st.columns([2, 8])
    #             col_img.image(row['image'])
    #             col_content.markdown(' '.join(str(row['content']).split()[:64]))
    #             st.link_button('Baca lebih lengkap', row['url'])

    #             st.divider()


if __name__ == "__main__":
    main()
