import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from rlogging import settings
from rlogging.utils import flatten_dict

# from opentelemetry import metrics
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# from opentelemetry.exporter.prometheus import PrometheusMetricReader
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

logger = logging.getLogger('rlogging')


class OtelSettings(settings.BaseSettings):
    model_config = settings.SettingsConfigDict(
        env_file=settings.ENV_FILE,
        env_prefix='ENV_OTEL_',
        extra='ignore',
    )

    TRACES_EXPORT_OTLP_ENDPOINT: str = 'http://localhost:4317'
    TRACES_EXPORT_INTERVAL: float = 5 * 1000
    TRACES_EXPORT_TIMEOUT: float = 10 * 1000

    METRICS_EXPORT_OTLP_ENDPOINT: str = 'http://localhost:4317/v1/metrics'
    METRICS_EXPORT_INTERVAL: float = 10 * 1000
    METRICS_EXPORT_TIMEOUT: float = 10 * 1000


OTEL = OtelSettings()


def init_telemetry():
    resource = Resource(
        attributes=flatten_dict({
            'service': {
                'name': settings.APP.NAME,
                'namespace': settings.APP.NAME.split(':')[0],
                'version': settings.APP.VERSION,
            },
            'deployment': {
                'environment': settings.APP.ENVIRONMENT,
            },
            'app': settings.APP.get_service_info(),
        })
    )

    #
    #
    #
    logger.info('Init otlp trace exporter')

    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=OTEL.TRACES_EXPORT_OTLP_ENDPOINT,
        insecure=True,
    )
    # from opentelemetry.sdk.trace.export import ConsoleSpanExporter
    # otlp_trace_exporter = ConsoleSpanExporter()

    tracer_provider = TracerProvider(resource=resource)

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            otlp_trace_exporter,
            schedule_delay_millis=OTEL.TRACES_EXPORT_INTERVAL,
            export_timeout_millis=OTEL.TRACES_EXPORT_TIMEOUT,
        )
    )

    trace.set_tracer_provider(tracer_provider)

    #
    #
    #

    # logger.info('Init otlp metric exporter')

    # otlp_metric_exporter = OTLPMetricExporter(
    #     endpoint=OTEL.METRICS_EXPORT_OTLP_ENDPOINT,
    #     insecure=True,
    # )

    # meter_provider = MeterProvider(
    #     resource=resource,
    #     metric_readers=[
    #         # PeriodicExportingMetricReader(ConsoleMetricExporter()),
    #         PeriodicExportingMetricReader(
    #             otlp_metric_exporter,
    #             OTEL.METRICS_EXPORT_INTERVAL,
    #             OTEL.METRICS_EXPORT_TIMEOUT,
    #         ),
    #         PrometheusMetricReader(),
    #     ],
    # )

    # metrics.set_meter_provider(meter_provider)

    #
    #
    #

    try:
        import httpx  # noqa: F401
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

        logger.info('Init HTTPXClientInstrumentor instrument')

        HTTPXClientInstrumentor().instrument()

    except ImportError:
        pass

    try:
        import psycopg2  # noqa: F401
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

        logger.info('Init Psycopg2Instrumentor instrument')

        Psycopg2Instrumentor().instrument(enable_commenter=True, commenter_options={})

    except ImportError:
        pass

    try:
        import sqlite3  # noqa: F401

        from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

        logger.info('Init SQLite3Instrumentor instrument')

        SQLite3Instrumentor().instrument()

    except ImportError:
        pass

    try:
        import sqlite3  # noqa: F401

        from opentelemetry.instrumentation.logging import LoggingInstrumentor

        logger.info('Init LoggingInstrumentor instrument')

        LoggingInstrumentor().instrument()

    except ImportError:
        pass

    try:
        import requests  # noqa: F401
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        logger.info('Init RequestsInstrumentor instrument')

        RequestsInstrumentor().instrument()

    except ImportError:
        pass
