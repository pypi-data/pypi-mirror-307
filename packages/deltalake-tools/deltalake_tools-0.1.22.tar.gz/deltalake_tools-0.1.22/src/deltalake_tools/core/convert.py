import logging
import pyarrow.dataset as ds
import pyarrow as pa
from deltalake import convert_to_deltalake
from deltalake_tools.models.models import S3ClientDetails
from deltalake_tools.result import Err, Ok, Result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeltaConverter:
    def __init__(self, source_path: str, table_path: str = None):
        self.source_path = source_path
        self.table_path = table_path

    def infer_partitioning(self) -> tuple[list[str], list[tuple[str, str]]]:
        dataset = ds.dataset(self.source_path, format="parquet", partitioning="hive")

        partitioning = dataset.partitioning

        if partitioning:
            schema = partitioning.schema
            partition_schema: list[tuple[str, str]] = []
            for field in schema:
                partition_schema.append((field.name, field.type))
            return pa.schema(partition_schema)

        else:
            print("The dataset is not partitioned.")
            return None

    def convert_parquet_to_delta(
        self,
        inplace: bool = False,
        storage_options: S3ClientDetails = None,
        partition_schema: pa.Schema = None,
        partition_strategy: str = None,
        infer_partitioning: bool = False,
    ) -> Result[str, str]:

        # logger.warning(f"{infer_partitioning=}")
        if infer_partitioning:
            partition_schema = self.infer_partitioning()

        if partition_schema is not None and partition_strategy is None:
            partition_strategy = "hive"

        if storage_options is not None:
            storage_options = storage_options.to_s3_config().unwrap()

        try:
            convert_to_deltalake(
                self.source_path,
                storage_options=storage_options,
                partition_by=partition_schema,
                partition_strategy=partition_strategy,
            )
        except Exception as e:
            logger.error(f"Error converting Parquet to Delta: {str(e)}")
            return Err(f"Error converting Parquet to Delta: {str(e)}")

        return Ok("Parquet converted to Delta successfully")


def convert_parquet_to_delta(
    source_path: str,
    table_path: str = None,
    inplace: bool = False,
    storage_options: S3ClientDetails = None,
    partition_schema: pa.Schema = None,
    infer_partitioning: bool = False,
) -> Result[str, str]:
    converter = DeltaConverter(source_path, table_path)
    return converter.convert_parquet_to_delta(
        inplace=inplace,
        storage_options=storage_options,
        partition_schema=partition_schema,
        infer_partitioning=infer_partitioning,
    )
