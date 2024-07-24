# Alfred AI

Alfred AI is a private, secure, and feature-rich tool designed to help you with your documents without sharing your private data with companies like Google or OpenAI. It leverages local AI models to provide various document analysis and interaction capabilities.

## Features

- **General Chat**: Engage in conversations with Alfred AI on a wide range of topics.
- **PDF Analysis**: Upload and analyze PDF documents with the following features:
  - Named Entity Recognition (NER)
  - Text Extraction
  - Keyword Search
  - Sentiment Analysis
  - Chat about PDF content
- **Customizable Settings**: Adjust Alfred AI's response tone and export conversation history.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/alfred-ai.git
   cd alfred-ai
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download the spaCy model:
   ```
   python -m spacy download en_core_web_sm
   ```

4. Install and set up Ollama with the Qwen2:0.5b model.

## Usage

Run the Streamlit app:
```
streamlit run app.py
```

Navigate to the provided local URL in your web browser to start using Alfred AI.

## Privacy and Security

Alfred AI is designed with privacy and security as top priorities:

- **Local Processing**: All data processing occurs locally on your machine. No data is sent to external servers or cloud services.
- **Ollama Integration**: The AI model (Qwen2:0.5b) runs locally through Ollama, ensuring that your queries and document contents never leave your device.
- **No Data Retention**: Conversations and analyzed documents are not permanently stored unless you choose to export them.
- **Open Source**: The codebase is open for inspection, allowing you to verify the privacy and security measures.
- **Customizable Settings**: You can clear chat history and PDF analysis results at any time.

While Alfred AI provides a high level of privacy, always be cautious when working with sensitive documents and information.

## Detailed Feature Descriptions

### Named Entity Recognition (NER)

The Named Entity Recognition feature uses spaCy's pre-trained model to identify and classify named entities in your PDF documents. Entities are categorized into types such as:

- PERSON: Names of people
- ORG: Organizations
- GPE: Geopolitical entities (countries, cities, states)
- DATE: Dates or periods
- CARDINAL: Numerals
- And more...

The NER results are displayed in a color-coded table for easy visualization and can be exported as a CSV file for further analysis.

### Sentiment Analysis

The Sentiment Analysis feature uses TextBlob to analyze the overall sentiment of the text in your PDF documents. It provides two main metrics:

- **Polarity**: A float value between -1 and 1, where -1 indicates very negative sentiment, 0 indicates neutral sentiment, and 1 indicates very positive sentiment.
- **Subjectivity**: A float value between 0 and 1, where 0 indicates very objective text and 1 indicates very subjective text.

This feature can be useful for quickly gauging the overall tone and subjectivity of a document.

### PDF Chat

The PDF Chat feature allows you to ask questions about the content of your uploaded PDF. Alfred AI uses the Qwen2:0.5b model to generate responses based on the extracted text from the PDF. This feature enables interactive exploration of document contents without the need to read through the entire text manually.

## Dependencies

- openai
- streamlit
- spacy
- pandas
- pdfplumber
- textblob
- Ollama (for local AI model hosting)

## Configuration

Alfred AI uses Ollama to run any model you want model locally. Make sure Ollama is properly set up and running before starting the application. Download Ollama from [ here](https://ollama.com/download).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Disclaimer

This tool is for personal use and should not be used as a substitute for professional advice. While we strive for accuracy in our NER and Sentiment Analysis features, results may not always be perfect. Always verify important information from authoritative sources.