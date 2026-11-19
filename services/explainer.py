def generate_explanation(alert) -> str:
    """Generate a human-readable explanation for an alert.

    Args:
        alert: An object providing severity, source, title, metric_name,
            metric_value, and threshold attributes. An optional resolved_by
            attribute is used to report who acknowledged the alert.

    Returns:
        A string describing the alert, its metric relative to the threshold,
        a severity-specific next step, and the acknowledgment status.

    Raises:
        KeyError: If alert.severity is not "critical", "warning", or "info".
        TypeError: If alert.metric_value and alert.threshold cannot be compared.
    """
    if alert.metric_value > alert.threshold:
        comparison = "exceeded"
    elif alert.metric_value < alert.threshold:
        comparison = "fell below"
    else:
        comparison = "reached"

    next_steps = {
        "critical": "Investigate immediately and take corrective action.",
        "warning": "Review the affected system and monitor the metric closely.",
        "info": "Review the metric and confirm whether any action is needed.",
    }

    explanation = (
        f'This {alert.severity} alert from {alert.source} is titled "{alert.title}". '
        f"The {alert.metric_name} metric {comparison} its threshold: the current value is "
        f"{alert.metric_value}, compared with a threshold of {alert.threshold}. "
        f"Recommended next step: {next_steps[alert.severity]}"
    )

    resolved_by = getattr(alert, "resolved_by", None)
    acknowledged_by = "Not yet acknowledged" if resolved_by is None else resolved_by.upper()

    return explanation + f" Acknowledged by: {acknowledged_by}."