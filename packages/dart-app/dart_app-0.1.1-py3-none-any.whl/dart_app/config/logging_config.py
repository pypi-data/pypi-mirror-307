import logging
from sqlalchemy.orm import sessionmaker
from dart_app.config.models import engine, MainLog, LoginLog, SetupLog
from datetime import datetime

# Create a session
Session = sessionmaker(bind=engine)

# Mapping of module names to tables
TABLE_MAP = {
    "login_window": LoginLog,
    "setup_window": SetupLog,
}

FORMATTER = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")


class DBLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.session = Session()

    def emit(self, record):
        # Determine the table based on the module name
        table = TABLE_MAP.get(record.module, MainLog)

        log_datetime = datetime.fromtimestamp(record.created)
        # Create a log entry
        log_entry = table(
            date=log_datetime.date(),
            time=log_datetime.time(),
            level=record.levelname,
            message=self.format(record),
        )

        # Add the log entry to the database
        self.session.add(log_entry)
        self.session.commit()

    def close(self):
        self.session.close()
        super().close()
