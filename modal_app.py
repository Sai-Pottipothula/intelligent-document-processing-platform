from __future__ import annotations

import modal

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("tesseract-ocr", "poppler-utils")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir("app", remote_path="/app/app", copy=True)
    .workdir("/app")
)

app = modal.App("intelligent-document-processing-platform")


@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("openai-secret"),
        modal.Secret.from_name("anthropic-secret"),
    ],
    timeout=300,
)
@modal.asgi_app()
def fastapi_app():
    from app.main import app as fastapi_app
    return fastapi_app