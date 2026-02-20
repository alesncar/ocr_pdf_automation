import os
import time
from dotenv import load_dotenv
from ocr_azure import ocr_pdf_azure
from llm_mistral import analisar_texto_com_mistral

load_dotenv()

PDF_FOLDER = r"C:\pdfs_testes"
OUTPUT_FOLDER = r"C:\projetos\ocr_pdf_automation\output_texts"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("👀 Monitorando a pasta:", PDF_FOLDER)

def process_pdf(pdf_path):
    print(f"\n📄 Processando: {os.path.basename(pdf_path)}")

    try:
        texto = ocr_pdf_azure(pdf_path)
        print("🧠 Enviando texto para Mistral...")

        resultado = analisar_texto_com_mistral(texto)

        output_file = os.path.join(
            OUTPUT_FOLDER,
            os.path.basename(pdf_path).replace(".pdf", "_estruturado.txt")
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(resultado)

        print(f"✅ Resultado salvo em: {output_file}")

    except Exception as e:
        print(f"❌ Erro: {e}")

def monitor_folder():
    vistos = set()

    while True:
        for f in os.listdir(PDF_FOLDER):
            if f.lower().endswith(".pdf"):
                full = os.path.join(PDF_FOLDER, f)
                if full not in vistos:
                    process_pdf(full)
                    vistos.add(full)
        time.sleep(5)

if __name__ == "__main__":
    monitor_folder()