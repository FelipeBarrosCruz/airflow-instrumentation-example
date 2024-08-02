import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("msg"),
        structlog.processors.JSONRenderer(),
    ]
)

def create_logger(**kwargs):
  return structlog.get_logger(**kwargs)