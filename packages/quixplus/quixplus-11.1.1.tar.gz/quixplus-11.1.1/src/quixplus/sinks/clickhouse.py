import logging
from typing import Any, Dict, List, Tuple

from quixstreams.models import HeaderValue
from quixstreams.sinks.base.batch import BatchingSink, SinkBatch
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class ClickHouseSink(BatchingSink):

    def __init__(self, db_url: str, table_name: str, column_types: Dict[str, str], mapper: callable=None):
        """
        Initialize the ClickHouseSink.

        :param db_url: The ClickHouse database connection URL.
        :param table_name: The name of the ClickHouse table where records will be written.
        :param column_types: A dictionary mapping column names to their ClickHouse data types.
        :param mapper: A callable to transform records into the desired format. Optional.
        """
        super().__init__()
        self.engine = create_engine(db_url)
        self.table_name = table_name
        self.column_types = column_types
        self.mapper = mapper or (lambda record: record)

    def write(self, batch: SinkBatch):
        """
        Write a batch of records to the ClickHouse database.

        :param batch: The batch of records to write.
        """
        records = []
        for record in batch:
            try:
                # Transform record using the mapper
                mapped_record = self.mapper({
                    "value": record.value,
                    "key": record.key,
                    "timestamp": record.timestamp,
                    "headers": {header[0]: header[1].value for header in record.headers},
                })
                # Map record fields to ClickHouse column types
                records.append({col: mapped_record.get(col) for col in self.column_types})
            except Exception as e:
                logger.error(f"Error mapping record: {e}")

        # Insert the records into ClickHouse
        if records:
            try:
                columns = ", ".join(self.column_types.keys())
                placeholders = ", ".join([f"%({col})s" for col in self.column_types.keys()])
                insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
                with self.engine.connect() as connection:
                    connection.execute(insert_query, records)
                logger.info(f"Inserted {len(records)} records into {self.table_name}.")
            except SQLAlchemyError as e:
                logger.error(f"Error writing batch to ClickHouse: {e}")
                raise

    def on_paused(self, topic: str, partition: int):
        """
        Log when the sink is paused due to backpressure.
        """
        logger.warning(f"Sink paused for topic {topic}, partition {partition}. Dropping accumulated batch.")
        super().on_paused(topic, partition)

__all__ = ["ClickHouseSink"]
