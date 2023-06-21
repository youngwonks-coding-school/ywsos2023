import json
from tinydb import TinyDB
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


class TinyDBSpanExporter(SpanExporter):
    """Implementation of :class:`SpanExporter` that prints spans to the
    console.

    This class can be used for diagnostic purposes. It prints the exported
    spans to the console STDOUT.
    """

    def __init__(
        self,
        out: str,
        service_name=None,
        formatter=lambda span: json.loads(span.to_json()),
    ):
        self.out = TinyDB(out)
        self.formatter = formatter
        self.service_name = service_name

    def export(self, spans):
        for span in spans:
            self.out.insert(self.formatter(span))
        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True

    def shutdown(self):
        self.out.close()


class MongoDBSpanExporter(SpanExporter):
    """Implementation of :class:`SpanExporter` that prints spans to the
    console.

    This class can be used for diagnostic purposes. It prints the exported
    spans to the console STDOUT.
    """

    def __init__(
        self,
        db: str,
        col="server_telemetry",
        service_name=None,
        formatter=lambda span: json.loads(span.to_json()),
    ):
        self.db = db
        self.col = col
        self.formatter = formatter
        self.service_name = service_name

    def export(self, spans):
        for span in spans:
            self.db[self.col].insert(self.formatter(span))
        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True

    def shutdown(self):
        self.out.close()
