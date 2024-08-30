import requests
import json
import streamlit as st
import openai
import pandas as pd

# Replace with your Tavily API key and OpenAI API key
tavily_api_key = ""
openai_api_key = ""

# Setting the OpenAI API key
openai.api_key = openai_api_key

tavily_url = "https://api.tavily.com/search"

def get_tavily_search_results(url):
    payload = json.dumps({
        "api_key": tavily_api_key,
        "query": f"site:{url}",
        "search_depth": "advanced",
        "include_raw_content": True,
        "include_images": False,
        "max_results": 3,
        "max_tokens":10000
    })
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(tavily_url, headers=headers, data=payload, verify=False)
    
  
    response_data = response.json()
    return response_data
   


def analyze_content_with_llm(contents):
    prompt = (
        "Generate a report comparing both the companies which can be used By designer to get more insights on User and what company want to potray "
        f"{contents}\n\n"
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

def display_comparison_results(results):
    st.subheader("Website Content Comparison")

    # Display the results in a text area
    st.text_area("Content Comparison", results, height=400)

def main():
    st.title("Website Content Comparison Tool")

    url_inputs = st.text_area("Enter the website URLs you want to analyze (one per line)").splitlines()

    if st.button("Analyze"):
        all_content = {}
        
        for url in url_inputs:
            result = get_tavily_search_results(url)
            
            if result and 'results' in result:
                combined_content = " ".join([res.get('raw_content') for res in result['results']])
                print(combined_content)
                if combined_content:
                    all_content[url] = combined_content
                else:
                    st.warning(f"No content found in the search results for {url}.")
            else:
                st.error(f"Failed to retrieve data from Tavily for {url} or no results found.")
        
        if all_content:
            contents_for_analysis = "\n\n".join([f"Website: {url}\nContent: {content}" for url, content in all_content.items()])
            comparison_results = analyze_content_with_llm(contents_for_analysis)
            display_comparison_results(comparison_results)
        else:
            st.warning("No valid content retrieved for analysis.")
        
    if st.button("Response"):
        for url in url_inputs:
             answer=get_tavily_search_results(url)
             st.write(answer)

if __name__ == "__main__":
    main()







import requests
import json
import streamlit as st
import openai
import pandas as pd

# Replace with your Tavily API key and OpenAI API key
tavily_api_key = ""
openai_api_key = ""

# Setting the OpenAI API key
openai.api_key = openai_api_key

tavily_url = "https://api.tavily.com/search"

def get_tavily_search_results(url):
    payload = json.dumps({
        "api_key": tavily_api_key,
        "query": f"site:{url}",
        "search_depth": "advanced",
        "include_raw_content": False,
        "include_images": False,
        "max_results": 5
    })
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(tavily_url, headers=headers, data=payload, verify=False)
    
    try:
        response_data = response.json()
        return response_data
    except requests.exceptions.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        st.error(f"Response content: {response.text}")
        return None

def analyze_content_with_llm(contents):
    prompt = (
        f"Compare and analyze the content from the following websites. "
        f"Identify how each site is trying to attract clients, the focus of their content, "
        f"the keywords they emphasize, and any notable differences in user flow or strategy. "
        f"Provide suggestions on how to improve or differentiate the content on another website:\n\n"
        f"{contents}\n\n"
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

def display_comparison_results(results):
    st.subheader("Website Content Comparison")

    # Display the results in a text area
    st.text_area("Content Comparison", results, height=400)

def main():
    st.title("Website Content Comparison Tool")

    url_inputs = st.text_area("Enter the website URLs you want to analyze (one per line)").splitlines()

    if st.button("Analyze"):
        all_content = {}
        
        for url in url_inputs:
            result = get_tavily_search_results(url)
            
            if result and 'results' in result:
                combined_content = " ".join([res.get('raw_content', '') for res in result['results']])
                if combined_content:
                    all_content[url] = combined_content
                else:
                    st.warning(f"No content found in the search results for {url}.")
            else:
                st.error(f"Failed to retrieve data from Tavily for {url} or no results found.")
        
        if all_content:
            contents_for_analysis = "\n\n".join([f"Website: {url}\nContent: {content}" for url, content in all_content.items()])
            comparison_results = analyze_content_with_llm(contents_for_analysis)
            display_comparison_results(comparison_results)
        else:
            st.warning("No valid content retrieved for analysis.")
    if st.button('Response'):
        for url in url_inputs:
            st.write(get_tavily_search_results(url))

if __name__ == "__main__":
    main()
