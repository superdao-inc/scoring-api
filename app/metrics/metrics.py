from prometheus_client import Counter, Histogram

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    labelnames=['code', 'route'],
    buckets=[1, 50, 100, 500, 1000, 5000, 10000],
)
RESPONSE_STATUS_COUNT = Counter(
    'response_status_count',
    'Response status count',
    labelnames=['code', 'route'],
)
