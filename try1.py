import requests
from bs4 import BeautifulSoup
import streamlit as st
from textblob import TextBlob

URL = 'https://boakenya.com/treasury/daily-market-update/'

def fetch_page_content():
    """Fetch page content using GET request."""
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)
        return None

def parse_page_content(content):
    """Parse HTML content and extract relevant information."""
    soup = BeautifulSoup(content, 'html.parser')
    
    column_element = soup.find('div', {'class': 'column'})
    if column_element:
        p_element = column_element.find('p')
        if p_element:
            text = p_element.text.strip()
            return text

    return None

def calculate_sentiment(text):
    """Calculate sentiment score of given text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return {"polarity": polarity, "subjectivity": subjectivity}

def main():
    st.set_page_config(page_title="Kenyan Shilling Update")

    st.sidebar.title("About Sentiment Analysis")
    st.sidebar.markdown('''
        **Polarity**: Represents the degree of positivity or negativity conveyed by a piece of text. Ranges from -1 (extremely negative) to 1 (intensely positive) with 0 being neutral.
        
        **Subjectivity**: Measures the level of personal opinions or biases presented in a text. Lower values suggest more objectivity, whereas higher ones represent increased subjectivity.
    ''')

    html_content = fetch_page_content()
    if html_content:
        extracted_data = parse_page_content(html_content)
        if extracted_data:
            sentiment_results = calculate_sentiment(extracted_data)

            st.title("Bank of Africa Kenya - Kenyan Shilling Update")
            st.subheader(extracted_data)
            st.markdown(f"**Sentiment Polarity:** {sentiment_results['polarity']}")
            st.markdown(f"**Sentiment Subjectivity:** {sentiment_results['subjectivity']}")

        else:
            st.write("No data available at the moment...")
    else:
        st.error("Failed to load data. Please check your connection or try again later.")

if __name__ == "__main__":
    main()