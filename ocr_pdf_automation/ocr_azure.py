import time
import requests
import os

AZURE_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_VISION_KEY")

def ocr_pdf_azure(pdf_path: str) -> str:
    url = f"{AZURE_ENDPOINT}vision/v3.2/read/analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/pdf"
    }

    with open(pdf_path, "rb") as f:
        resp = requests.post(url, headers=headers, data=f)

    if resp.status_code != 202:
        raise Exception(resp.text)

    operation_url = resp.headers["Operation-Location"]

    for _ in range(30):
        result = requests.get(operation_url, headers={
            "Ocp-Apim-Subscription-Key": AZURE_KEY
        }).json()

        if result.get("status") == "succeeded":
            text = ""
            for page in result["analyzeResult"]["readResults"]:
                for line in page["lines"]:
                    text += line["text"] + "\n"
            return text

        time.sleep(2)

    raise Exception("Timeout OCR Azure")