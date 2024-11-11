import hashlib
import time
import requests
from XMZAPI.APM import OpenTelemetryConfigurator, get_tracer
from XMZAPI.KVS import LogHandler
from XMZAPI.KMS import KMS


class DNSResolver:
    def __init__(self):
        self.kms = KMS()
        self.account_id = self.kms.kms("ali_account_id")
        self.access_key_id = self.kms.kms("ali_access_key_id")
        self.access_key_secret = self.kms.kms("ali_access_key_secret")
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

    def generate_signature(self, qname, ts):
        """
        生成鉴权用的哈希串
        """
        signature_string = (
            f"{self.account_id}{self.access_key_secret}{ts}{qname}{self.access_key_id}"
        )
        M = hashlib.sha256(signature_string.encode()).hexdigest()
        return M

    def get_dns_record(self, name, record_type):
        """
        调用DoH JSON API获取DNS记录
        param: name: 域名
        param: record_type: 记录类型
        """
        with self.tracer.start_as_current_span("get_dns_record") as span:
            # 基本参数
            uid = self.account_id
            ak = self.access_key_id
            ts = str(int(time.time()))
            key = self.generate_signature(name, ts)
            # 构建请求URL
            url = f"https://223.5.5.5/resolve?name={name}&type={record_type}&uid={uid}&ak={ak}&key={key}&ts={ts}"
            # 发送请求
            response = requests.get(url)
            self.log.process_log(response.json(), "get_dns_record")
            span.set_attribute("uid", uid)
            span.set_attribute("ak", ak)
            span.set_attribute("ts", ts)
            span.set_attribute("key", key)
            span.set_attribute("url", url)
            span.set_attribute("response", response.text)
            # 检查响应状态码
            if response.status_code == 200:
                return response.json()  # 返回JSON响应
            else:
                return {
                    "error": f"Failed to retrieve data, status code: {response.status_code,response.text}"
                }
