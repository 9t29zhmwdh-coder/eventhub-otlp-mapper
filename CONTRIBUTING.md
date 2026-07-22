# Contributing

## Development Setup

```bash
git clone https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper
cd eventhub-otlp-mapper
pip install -e ".[dev]"

# Lint
ruff check src/ tests/

# Test
pytest tests/ -v
```

## Adding a New Payload Format

1. Add detection and decoding logic to `src/eventhub_otel_mapper/schema_mapper.py`
2. Add a test in `tests/` with a sample payload of the new format
3. Document the format in the Features table in `README.md` and in `ARCHITECTURE.md`

## Adding a New Export Target

1. Add the exporter setup in `src/eventhub_otel_mapper/metric_exporter.py` (or `trace_generator.py` for traces)
2. Gate it behind a config option in `config_validator.py` so existing users are unaffected
3. Add a test covering the new exporter path
4. Update `README.md` Requirements/Features sections

## Pull Request Requirements

- `ruff check` passes with no errors
- `pytest tests/ -v` passes on both ubuntu-latest and windows-latest
- No connection strings, tenant IDs, or captured event payloads in any committed file
- `CHANGELOG.md` updated
