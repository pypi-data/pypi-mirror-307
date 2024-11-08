from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.context import attach, set_value
from traceloop.sdk.instruments import Instruments
from traceloop.sdk import Traceloop

from typing import TypedDict, Optional, Any
import os


class LytixMetadata(TypedDict, total=False):
    userId: Optional[str]
    sessionId: Optional[str]
    workflowName: Optional[str]
    __extra__: dict[str, Any]  # This allows arbitrary additional keys


class LytixAsyncLogger:
    baseURL: str
    lytixAPIKey: str

    def __init__(
        self,
        lytixAPIKey: str | None = None,
        baseURL: Optional[str] = "https://api.lytix.co/v2/metrics/async",
    ) -> None:
        if lytixAPIKey is None:
            raise Exception(
                "The Lytix API Key must be set by passing lytixAPIKey to the class."
            )
        self.lytixAPIKey = lytixAPIKey

        self.baseURL = baseURL

    def init(self) -> None:
        """
        Initialize the Lytix Async Logger
        """
        exporter = OTLPSpanExporter(
            endpoint=self.baseURL,
            headers={"lx-api-key": f"{self.lytixAPIKey}"},
        )

        """
        Disable logging
        @see https://www.traceloop.com/docs/openllmetry/privacy/traces
        """
        os.environ["TRACELOOP_TRACE_CONTENT"] = "true"

        Traceloop.init(
            exporter=exporter,
            disable_batch=True,
            should_enrich_metrics=False,
            instruments=set([Instruments.OPENAI]),
        )

    def set_metadata(self, metadata: LytixMetadata):
        """
        Set additional lytix metadata

        Args:
            metadata (LytixMetadata): Metadata to associate with the function call
                                    Can include userId, sessionId, workflowName, or other key-value pairs
            callback (callable): Function to call

        Returns:
            The result of the callback function
        """
        Traceloop.set_association_properties(metadata)
