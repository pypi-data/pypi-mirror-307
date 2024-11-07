from lib import trace_loop

SERVICE_NAME = "my-otel-test"
NUM_ADDS = 12

if __name__ == "__main__":
    trace_loop(NUM_ADDS)

class MyOtelTest:
    def requirements(self):
        return "opentelemetry-distro", "opentelemetry-exporter-otlp-proto-grpc"

    def environment_variables(self):
        return {
            "OTEL_SERVICE_NAME": SERVICE_NAME,
            "OTEL_EXPERIMENTAL_RESOURCE_DETECTORS": "process",
        }

    def wrapper_command(self):
        return "opentelemetry-instrument"

    def on_start(self):
        return None

    def on_stop(self, telemetry, stdout: str, stderr: str, returncode: int) -> None:
        pass

    def is_http(self):
        return False
