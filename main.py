# To install: pip install tavily-python
from tavily import TavilyClient
import streamlit as st
import os
import pandas as pd
import dotenv

dotenv.load_dotenv()

st.sidebar.header("API Key Input")
st.sidebar.markdown("""
To get your Tavily API key:
1. Go to [Tavily](https://tavily.com/)
2. Create your free account
3. You will get 1000 API requests per month
4. One request is one click of the generate button
5. Even if you use 20 requests per day, you will still be left with 400 more requests
""")
api_key = st.sidebar.text_input("Enter your Tavily API Key")

if api_key:
    client = TavilyClient(api_key)
else:
    st.sidebar.error("Please enter your Tavily API Key")

st.title("Tavily Search")
job_role = st.text_input("Enter the job role")
time_range = st.selectbox("Select the time range", ["day", "week"])
generate_btn = st.button("Generate")

def tavily_run(time_range, prompt):
    response = client.search(
    query=prompt,
    search_depth="advanced",
    max_results=20,
    time_range=time_range,
    include_answer="advanced",
    include_domains=["dice.com"],
   
)
    return response

if generate_btn:
    prompt = f"I want you to extract job postings for the role of {job_role} from the provided domains in United States of America. Do not include blog posts"
    response = tavily_run(time_range, prompt)
    results = response['results']
    st.write(results)
    data = [{'title': result['title'], 'url': result['url']} for result in results]
    
    job_list = pd.DataFrame(data)
    job_list['url'] = job_list['url'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    
    # Display the DataFrame with hyperlinks
    st.markdown(job_list.to_html(escape=False), unsafe_allow_html=True)




    
