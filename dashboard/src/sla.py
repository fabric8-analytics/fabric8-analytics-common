"""Thresholds for SLA."""

SLA = {
    "component analysis": {
        "sequenced_calls_known_component": {
            "max": 1.5,
            "avg": 1.0,
            "sum": 12.0
        },
        "sequenced_calls_unknown_component": {
            "max": 1.5,
            "avg": 1.0,
            "sum": 12.0
        },
        "parallel_calls_known_component": {
            "max": 5.0,
            "avg": 2.0,
            "sum": 12.0
        },
        "parallel_calls_unknown_component": {
            "max": 5.0,
            "avg": 2.0,
            "sum": 12.0
        },
    },
    "stack analysis": {
        "sequenced_calls": {
            "max": 60.0,
            "avg": 45.0,
            "sum": 250.0
        },
        "parallel_calls": {
            "max": 60.0,
            "avg": 45.0,
            "sum": 200.0
        },
    }
}
