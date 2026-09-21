#!/usr/bin/env python3
import os
import email
from bs4 import BeautifulSoup

def extract_text_from_mht(filename):
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        msg = email.message_from_file(f)
    html_content = ""
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            payload = part.get_payload(decode=True)
            if payload:
                try:
                    html_content += payload.decode('utf-8', errors="ignore")
                except Exception:
                    continue
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    return text

def paginate_text(text, lines_per_page=200):
    lines = text.splitlines()
    pages = [lines[i:i+lines_per_page] for i in range(0, len(lines), lines_per_page)]
    return pages


if __name__ == "__main__":
    mht_file = "👔 Consultoria_ Projeto Comercial & Automação _ OpenHands Cloud (1).mht"
    if not os.path.exists(mht_file):
        print(f"Arquivo {mht_file} não encontrado.")
        exit(1)
    text = extract_text_from_mht(mht_file)
    pages = paginate_text(text)
    output_folder = "extracted_text"
    os.makedirs(output_folder, exist_ok=True)
    for i, page in enumerate(pages, start=1):
        with open(os.path.join(output_folder, f"page_{i}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(page))
    print(f"Extração completa. {len(pages)} páginas geradas na pasta {output_folder}.")
