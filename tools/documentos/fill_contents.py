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
                    html_content += payload.decode("utf-8", errors="ignore")
                except Exception:
                    continue
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n")
    return text


def main():
    expected_name = "Consultoria_ Projeto Comercial & Automação _ OpenHands Cloud (1).mht"
    if os.path.exists(expected_name):
        mht_filename = expected_name
    else:
        files = [f for f in os.listdir('.') if f.lower().endswith('.mht')]
        if files:
            mht_filename = files[0]
        else:
            print(f"Arquivo {expected_name} não encontrado, e nenhum .mht encontrado.")
            return

    full_text = extract_text_from_mht(mht_filename)
    if not full_text.strip():
        print("Nenhum texto extraído.")
        return

    # Dividir o texto extraído em 4 partes para cada diretório
    text_len = len(full_text)
    block_size = text_len // 4
    docs_text = full_text[:block_size]
    automacao_text = full_text[block_size:2*block_size]
    comercial_text = full_text[2*block_size:3*block_size]
    metas_pessoais_text = full_text[3*block_size:]

    # Preencher os arquivos .gitkeep em cada pasta com o conteúdo respectivo
    with open(os.path.join("docs", ".gitkeep"), "w", encoding="utf-8") as f:
        f.write(docs_text)
    with open(os.path.join("automacao", ".gitkeep"), "w", encoding="utf-8") as f:
        f.write(automacao_text)
    with open(os.path.join("comercial", ".gitkeep"), "w", encoding="utf-8") as f:
        f.write(comercial_text)
    with open(os.path.join("metas_pessoais", ".gitkeep"), "w", encoding="utf-8") as f:
        f.write(metas_pessoais_text)

    # Atualizar dashboard.md e MANUAL_DE_USO.md com o conteúdo completo
    dashboard_file = "dashboard.md"
    manual_file = "MANUAL_DE_USO.md"
    dashboard_header = "# Dashboard do Negócio\n\nEste dashboard foi atualizado com informações completas da consultoria.\n\n"
    manual_header = "# MANUAL DE USO\n\nEste manual foi atualizado com o conteúdo completo da consultoria.\n\n"
    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.write(dashboard_header + full_text)
    with open(manual_file, "w", encoding="utf-8") as f:
        f.write(manual_header + full_text)

    print("Arquivos preenchidos com sucesso.")


if __name__ == '__main__':
    main()
