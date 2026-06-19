"""Tests for trace_generator module."""

from unittest.mock import MagicMock, patch

from eventhub_otel_mapper.trace_generator import emit_span


def _mapped() -> dict:
    return {
        "span.name": "user.login",
        "span.trace_id": "abc-123",
        "resource.service.name": "auth-service",
        "span.attributes.event.severity": "INFO",
        "span.attributes.duration_ms": "42",
        "span.attributes.http.status_code": "200",
    }


def test_emit_span_ok():
    mock_span = MagicMock()
    mock_tracer = MagicMock()
    mock_tracer.start_as_current_span.return_value.__enter__ = lambda s: mock_span
    mock_tracer.start_as_current_span.return_value.__exit__ = MagicMock(
        return_value=False
    )

    emit_span(_mapped(), mock_tracer)

    mock_tracer.start_as_current_span.assert_called_once()
    call_kwargs = mock_tracer.start_as_current_span.call_args
    assert call_kwargs.args[0] == "user.login"


def test_emit_span_with_error():
    mapped = _mapped()
    mapped["span.status.description"] = "connection refused"

    mock_span = MagicMock()
    mock_tracer = MagicMock()
    mock_tracer.start_as_current_span.return_value.__enter__ = lambda s: mock_span
    mock_tracer.start_as_current_span.return_value.__exit__ = MagicMock(
        return_value=False
    )

    emit_span(mapped, mock_tracer)

    mock_span.set_status.assert_called_once()
    status_args = mock_span.set_status.call_args.args
    from opentelemetry.trace import StatusCode
    assert status_args[0] == StatusCode.ERROR


def test_emit_span_invalid_http_status():
    mapped = _mapped()
    mapped["span.attributes.http.status_code"] = "not_a_number"

    mock_span = MagicMock()
    mock_tracer = MagicMock()
    mock_tracer.start_as_current_span.return_value.__enter__ = lambda s: mock_span
    mock_tracer.start_as_current_span.return_value.__exit__ = MagicMock(
        return_value=False
    )

    emit_span(mapped, mock_tracer)
    mock_tracer.start_as_current_span.assert_called_once()
