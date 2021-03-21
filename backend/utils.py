import re

from PIL import Image
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from pytesseract import pytesseract
from tika import parser

credential = AzureKeyCredential("c02c15f9208d42c38e60c88a41a991f0")


def get_entities(text):
    endpoint = "https://westeurope.api.cognitive.microsoft.com/"

    # # client
    # text_analytics_client = TextAnalyticsClient(endpoint, credential)
    #
    # # analyse text from image/pdf
    # documents = [text[:-1]]
    #
    # response = text_analytics_client.extract_key_phrases(documents, language="en")
    # result = [doc for doc in response if not doc.is_error]

    text_analytics_client = TextAnalyticsClient(endpoint, credential)

    documents = [text[:-1]]
    response = text_analytics_client.recognize_entities(documents=documents)

    prepared_entities = [("presctiption", "main")]
    for document in response:
        for entity in document.entities:
            prepared_entities.append((entity.text, entity.category))

    print(prepared_entities)
    return prepared_entities


def custom_analysis(text):
    txt = " ".join(re.findall(r"[a-zA-Z0-9]+", text))
    words = txt.split()

    matches = {'Diagnosis': "", 'Treatment': "", 'Prescription': "", 'Symptoms': "", 'Recommendations': ""}
    current_keyword = ""
    for word in words:
        if word in matches:
            current_keyword = word
            matches[word] = ""
        else:
            if current_keyword != "":
                matches[current_keyword] = matches[current_keyword] + ' ' + word

    return matches


def get_keywords(text):
    # account settings
    endpoint = "https://westeurope.api.cognitive.microsoft.com/"

    # client
    text_analytics_client = TextAnalyticsClient(endpoint, credential)

    # analyse text from image/pdf
    documents = [text[:-1]]

    response = text_analytics_client.extract_key_phrases(documents, language="en")
    result = [doc for doc in response if not doc.is_error]

    return result[0].key_phrases


def get_text_from_file(filename):
    path_to_tesseract = r"/usr/bin/tesseract"
    # filename = r"pr.pdf"

    if filename.endswith('.jpg') or filename.endswith('.png'):
        img = Image.open(filename)

        # Providing the tesseract executable location to pytesseract library
        pytesseract.tesseract_cmd = path_to_tesseract

        text = pytesseract.image_to_string(img)

        # Displaying the extracted text
        return text[:-1]

    else:
        parsed_pdf = parser.from_file(filename)
        data = parsed_pdf['content']
        print(get_keywords(data))
        custom_analysis(data)

        return data