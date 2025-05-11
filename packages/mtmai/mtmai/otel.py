import logging

is_instrumented = False

logger = logging.getLogger(__name__)


def setup_instrumentor():
    import base64
    import os

    global is_instrumented
    if is_instrumented:
        logger.warning("setup_instrumentor is already called")
        return

    is_instrumented = True

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

    # from openinference.instrumentation.smolagents import SmolagentsInstrumentor
    # from phoenix.otel import register

    # register()
    # SmolagentsInstrumentor().instrument()

    # languse
    from openinference.instrumentation.smolagents import SmolagentsInstrumentor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    trace_provider = TracerProvider()
    trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

    SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)
