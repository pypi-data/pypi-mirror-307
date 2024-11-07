from math import trunc

from openai import OpenAI
from XMZAPI.APM import OpenTelemetryConfigurator, get_tracer
from XMZAPI.KVS import LogHandler


class aistudio:
    def __init__(self):
        self.api_key = "c43bf1c3f5c3bf6429f9d8333eb1d5b5d63d14d1"
        self.url = "https://aistudio.baidu.com/llm/lmapi/v3"
        self.log = LogHandler()
        self.configurator = OpenTelemetryConfigurator(
            host_name="aistudio",
            service_name="XMZSDK",
            service_version="1.0.0",
            deployment_environment="prod",
            endpoint="http://tracing-analysis-dc-sh.aliyuncs.com/adapt_i8ucd7m6kr@c81a1d4e5cb019a_i8ucd7m6kr@53df7ad2afe8301/api/otlp/traces",
        )
        self.configurator.init_opentelemetry()
        self.tracer = get_tracer()

    def chat(self, prompt, model):
        with self.tracer.start_as_current_span("aistudio_chat") as span:
            span.set_attribute("apikey", self.api_key)
            span.set_attribute("url", self.url)
            span.set_attribute("prompt", prompt)
            span.set_attribute("model", model)
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.url,
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "你是 AI Studio 实训AI开发平台的开发者助理，你精通开发相关的知识，负责给开发者提供搜索帮助建议。",
                    },
                    {"role": "user", "content": prompt},
                ],
                model=model,
            )
            M = chat_completion.choices[0].message.content
            span.set_attribute("response", M)
            self.log.process_log(M, "aistudio")
            return M
