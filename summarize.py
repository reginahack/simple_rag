import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# This example requires environment variables named "AI_KEY" and "LANG_ENDPOINT"
key = os.environ.get('AI_KEY')
endpoint = os.environ.get('LANG_ENDPOINT')

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential
    )
    return text_analytics_client

client = authenticate_client()

# Function for summarizing text
def extractive_summarization(client, document, max_sentences=1):
    """
    Summarizes the given document using Azure Text Analytics.

    Args:
        client: The authenticated TextAnalyticsClient.
        document (list): A list of strings to summarize.
        max_sentences (int): The maximum number of sentences in the summary.

    Returns:
        str: The extracted summary.
    """
    from azure.ai.textanalytics import ExtractiveSummaryAction

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=max_sentences)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            return f"Error: Code '{extract_summary_result.code}', Message '{extract_summary_result.message}'"
        else:
            return " ".join([sentence.text for sentence in extract_summary_result.sentences])

