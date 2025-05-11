is_instrumented = False


def setup_instrumentor():
    import base64
    import os

    global is_instrumented
    if is_instrumented:
        return

    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")
    LANGFUSE_AUTH = base64.b64encode(
        f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()
    ).decode()

    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = (
        f"{LANGFUSE_HOST}/api/public/otel"  # EU data region
    )
    # os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://us.cloud.langfuse.com/api/public/otel" # US data region
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

    # your Hugging Face token
    # os.environ["HF_TOKEN"] = "hf_..."

    from openinference.instrumentation.smolagents import SmolagentsInstrumentor
    from phoenix.otel import register

    register()
    SmolagentsInstrumentor().instrument()
