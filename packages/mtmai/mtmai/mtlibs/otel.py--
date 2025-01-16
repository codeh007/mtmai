import logging
from collections.abc import Iterable

from fastapi import FastAPI

from mtmai.core.coreutils import is_in_vercel


def setup_otel(app: FastAPI):
    """参考:  https://github.com/softwarebloat/python-tracing-demo ."""
    from opentelemetry import trace
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    # def setting_otlp(app: ASGIApp, app_name: str,  log_correlation: bool = True) -> None:
    # Setting OpenTelemetry
    # set the service name to show in traces
    service_name = "mtmai.dev.1"
    if is_in_vercel():
        service_name = "mtmai.vercel"
    resource = Resource.create(
        attributes={"service.name": service_name, "compose_service": service_name}
    )

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    print("service name")
    print(service_name)
    # print(
    #     "otel tracer: service_name="
    #     + service_name
    #     + ",endpoint:"
    #     + os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    # )
    tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    # tracer.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    log_correlation = True
    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    # metrics.set_meter_provider(
    #     MeterProvider(
    #         resource=resource,
    #         metric_readers=[
    #             (
    #                 PeriodicExportingMetricReader(
    #                     OTLPMetricExporter(endpoint=collector_endpoint)
    #                 )
    #             )
    #         ],
    #     )
    # )

    # logger_provider = LoggerProvider(resource=resource)
    # logger_provider.add_log_record_processor(
    #     BatchLogRecordProcessor(OTLPLogExporter(endpoint=collector_endpoint))
    # )
    # logging.getLogger().addHandler(
    #     LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    # )

    # metrics ----------------------------------------------------------------------------
    from opentelemetry.metrics import (
        CallbackOptions,
        Observation,
        get_meter_provider,
        set_meter_provider,
    )

    def observable_counter_func(options: CallbackOptions) -> Iterable[Observation]:
        yield Observation(1, {})

    def observable_up_down_counter_func(
        options: CallbackOptions,
    ) -> Iterable[Observation]:
        yield Observation(-10, {})

    def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
        yield Observation(9, {})

    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.metrics import CallbackOptions, Observation
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    exporter = OTLPMetricExporter()
    reader = PeriodicExportingMetricReader(exporter)
    provider = MeterProvider(metric_readers=[reader])
    set_meter_provider(provider)

    meter = get_meter_provider().get_meter("getting-started", "0.1.2")
    # Counter
    counter = meter.create_counter("counter")
    counter.add(1)

    # Async Counter
    observable_counter = meter.create_observable_counter(
        "observable_counter",
        [observable_counter_func],
    )

    # UpDownCounter
    updown_counter = meter.create_up_down_counter("updown_counter")
    updown_counter.add(1)
    updown_counter.add(-5)

    # Async UpDownCounter
    observable_updown_counter = meter.create_observable_up_down_counter(
        "observable_updown_counter", [observable_up_down_counter_func]
    )

    # Histogram
    histogram = meter.create_histogram("histogram")
    histogram.record(99.9)

    # Async Gauge
    gauge = meter.create_observable_gauge("gauge", [observable_gauge_func])

    # logging ----------------------------------------------------------------------------
    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "service.name": "shoppingcart113",
                "service.instance.id": "instance-12",
            }
        ),
    )
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
    # 之后, 其他地方可以使用标准的方式使用 logging 例如:
    # logger1 = logging.getLogger("myapp.area1")
    # logger1.info("hello otel logger")

    urls_to_exclude = "client/.*/info,/otherpath123"
    FastAPIInstrumentor.instrument_app(
        app, tracer_provider=tracer, excluded_urls=urls_to_exclude
    )
