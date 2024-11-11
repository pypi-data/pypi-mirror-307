from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanHttpExporter,
)
from opentelemetry.sdk.resources import (
    Resource,
    SERVICE_NAME,
    SERVICE_VERSION,
    DEPLOYMENT_ENVIRONMENT,
    HOST_NAME,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def get_tracer():
    """
    获取OpenTelemetry Tracer实例。
    """
    return trace.get_tracer(__name__)


def shutdown():
    """
    关闭TracerProvider，确保所有追踪数据被上传。
    """
    trace.get_tracer_provider()


class OpenTelemetryConfigurator:
    """
    用于配置和初始化OpenTelemetry的类。
    """

    def __init__(
        self, host_name, service_name, service_version, deployment_environment, endpoint
    ):
        """
        初始化OpenTelemetryConfigurator类的构造函数。

        :param service_name: 服务名称，用于标识跟踪的应用程序或服务。
        :param service_version: 服务版本，用于区分同一服务的不同版本。
        :param deployment_environment: 部署环境，例如"prod"、"staging"等。
        :param endpoint: OpenTelemetry数据导出器的端点URL。
        """
        self.service_name = service_name
        self.service_version = service_version
        self.deployment_environment = deployment_environment
        self.host_name = host_name
        self.endpoint = endpoint

    def init_opentelemetry(self):
        """
        初始化OpenTelemetry，配置资源、TracerProvider和SpanProcessor。
        """
        # 创建资源，包括服务名、版本、部署环境和主机名
        resource = Resource(
            attributes={
                SERVICE_NAME: self.service_name,
                SERVICE_VERSION: self.service_version,
                DEPLOYMENT_ENVIRONMENT: self.deployment_environment,
                HOST_NAME: self.host_name,
            }
        )
        # 创建OTLP HTTP Exporter
        exporter = OTLPSpanHttpExporter(endpoint=self.endpoint)
        # 创建BatchSpanProcessor
        span_processor = BatchSpanProcessor(exporter)
        # 创建TracerProvider
        trace_provider = TracerProvider(
            resource=resource,
            active_span_processor=span_processor,
        )
        # 设置全局TracerProvider
        trace.set_tracer_provider(trace_provider)
