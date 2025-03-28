def setup_instrument():
    from openinference.instrumentation.smolagents import SmolagentsInstrumentor
    from phoenix.otel import register

    register()
    SmolagentsInstrumentor().instrument()
