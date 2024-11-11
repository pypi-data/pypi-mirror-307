import json

import requests
from XMZAPI.APM import OpenTelemetryConfigurator, get_tracer
from XMZAPI.KVS import LogHandler


class ERNIE_Bot_4_0_8k:
    def __init__(self):
        self.log = LogHandler()
        self.configurator = OpenTelemetryConfigurator(
            host_name="ERNIE-4-0-8K",
            service_name="XMZSDK",
            service_version="1.0.0",
            deployment_environment="prod",
            endpoint="http://tracing-analysis-dc-sh.aliyuncs.com/adapt_i8ucd7m6kr@c81a1d4e5cb019a_i8ucd7m6kr@53df7ad2afe8301/api/otlp/traces",
        )
        self.configurator.init_opentelemetry()
        self.tracer = get_tracer()

    def get_response(self, Content):
        with self.tracer.start_as_current_span("ERNIE-4-0-8K") as span:
            url = "https://hwapi.mizhoubaobei.top/ERNIE-4-0-8K"
            payload = json.dumps({"messages": [{"role": "user", "content": Content}]})
            response = requests.request("POST", url, data=payload)
            span.set_attribute("request", payload)
            span.set_attribute("url", url)
            span.set_attribute("method", "POST")
            M = response.json()
            response = response.text
            W = json.loads(response)
            self.log.process_log(response, "ERNIE-4-0-8K")
            span.set_attribute("response_id", M.get("data").get("id"))
            span.set_attribute("response_text", W)
            return response
