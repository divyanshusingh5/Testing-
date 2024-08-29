import requests
import json

# Replace with your Tavily API key
tavily_api_key = "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"
tavily_url = "https://api.tavily.com/search"

def get_tavily_search_results(url):
    # Create the payload for the Tavily API request
    payload = json.dumps({
        "api_key": tavily_api_key,
        "query": f"site:{url}",
        "search_depth": "advanced",
        "include_raw_content": True,  # Request raw HTML content
        "include_images": True,
        "max_results": 5
    })
    
    headers = {'Content-Type': 'application/json'}
    
    # Send the POST request to the Tavily API
    response = requests.post(tavily_url, headers=headers, data=payload, verify=False)
    
    try:
        # Parse the response data into JSON
        response_data = response.json()
        return response_data
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
        return None

def analyze_html_content(raw_html):
    # Perform analysis on the HTML content
    # For this example, we will just print it out
    # In a real use case, you might parse this HTML with BeautifulSoup, etc.
    print("Extracted HTML Content:")
    print(raw_html)

def main():
    # Get the website URL from the user
    url = input("Enter the website URL you want to analyze: ")
    
    # Fetch the search results from Tavily
    result = get_tavily_search_results(url)
    
    if result and 'results' in result:
        # Combine raw HTML content from all results
        raw_content = " ".join([res.get('raw_content', '') for res in result['results']])
        
        if raw_content:
            # Analyze the raw HTML content
            analyze_html_content(raw_content)
        else:
            print("No HTML content found in the search results.")
    else:
        print("Failed to retrieve data from Tavily or no results found.")

if __name__ == "__main__":
    main()

