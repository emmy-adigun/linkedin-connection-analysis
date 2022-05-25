import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
# from wordcloud import WordCloud

st.set_page_config(layout="wide")

st.title("Linkedin Connection Analysis")
st.write("Upload the downloaded 'Connections' file and filter using the sidebar dropdown menu")

st.markdown("""
<style>
body{
       background: rgb(0, 23, 43);
       color: rgb(220, 220, 220);
}
.column-style {
    font-size:16px !important;
    text-align:left;
    color: rgb(61, 157, 243);
    border: 1px solid rgba(28, 131, 225, 0.1);
    background-color: rgba(28, 131, 225, 0.1);
    border-radius: 0.25rem;
    padding: 16px;
    opacity: 1;
}
.css-1njf6aq {
    background-color: blue;
    }
</style>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:


     # Can be used wherever a "file-like" object is accepted:
     df = pd.read_csv(uploaded_file, skiprows=list(range(2)))
#      df = df.sort_values(by='Company', ascending=True)
     
    #  st.dataframe(df.head())
    #  st.markdown("## **Use the select feature on the side bar to filter by company**")
     options = df['Company'].unique().tolist()
     selected_options = st.sidebar.multiselect('Select single or multiple company(s)', options)

     filtered_df = df[df["Company"].isin(selected_options)]
     
     st.dataframe(filtered_df)

     group_filtered_company = filtered_df.groupby(by = 'Company').count().reset_index()
     group_filtered_company
     group_filtered_company=group_filtered_company.sort_values(by = 'Connected On',ascending=False).reset_index(drop=True)

     fig = px.bar(group_filtered_company[:50],
            x = 'Company',
            y = 'Connected On',
            labels = {'Connected On':'Number of Connections'},
            width = 1000,
            height = 500,
            title = 'Companies that my Connections are working at')
     st.plotly_chart(fig)

     fig_tree = px.treemap(group_filtered_company[:50], path = ['Company', 'Position'],
                     values = 'Connected On',
                     labels = {'Connected On' : 'Number of Connections'},
                     width = 1000,
                     height = 600,
                     title = 'Tree Map for companies that my connections are working at')
     st.plotly_chart(fig_tree)


     st.markdown("## **Full Connection Analysis**")
     # st.write(df)

     group_company = df.groupby(by = 'Company').count().reset_index()
     group_company=group_company.sort_values(by = 'Connected On',ascending=False).reset_index(drop=True)

     fig = px.bar(group_company[:50],
            x = 'Company',
            y = 'Connected On',
            labels = {'Connected On':'Number of Connections'},
            width = 1000,
            height = 900,
            title = 'Companies that my Connections are working at')
     st.plotly_chart(fig)

     fig_tree = px.treemap(group_company[:50], path = ['Company', 'Position'],
                     values = 'Connected On',
                     labels = {'Connected On' : 'Number of Connections'},
                     width = 1000,
                     height = 900,
                     title = 'Tree Map for companies that my connections are working at')
     st.plotly_chart(fig_tree)

     st.markdown("#### **Number of Positions occupied by my Linkedin Connections**")
     # df['Position'].value_counts()/len(df) * 100 > 0.20
     linkedin_position = pd.DataFrame(df['Position'].value_counts()[df['Position'].value_counts()/len(df) * 100 > 0.20])
     linkedin_position

     fig_position = px.bar(df.groupby(by = 'Position').count().sort_values(by = 'First Name', ascending=False)
            [:50].reset_index(),
            x = 'Position',
            y = 'Connected On',
            width = 1000,
            height = 900,
            labels = {'Connected On': 'Number of Connections'},
            title = 'The various Positions occupied by my LinkedIn Connections')
     st.plotly_chart(fig_position)
