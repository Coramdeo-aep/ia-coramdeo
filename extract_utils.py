import fitz
import docx
import pandas as pd
from bs4 import BeautifulSoup


def extrair_pdf(path):
    return "\n".join([page.get_text() for page in fitz.open(path)]).strip()


def extrair_docx(path):
    return "\n".join([p.text for p in docx.Document(path).paragraphs])


def extrair_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f, 'html.parser').get_text()


def extrair_planilha(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    return df.to_string()
