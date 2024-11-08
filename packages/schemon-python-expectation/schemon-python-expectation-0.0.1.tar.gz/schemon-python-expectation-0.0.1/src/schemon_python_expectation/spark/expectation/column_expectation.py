from pyspark.sql import functions as F
from pyspark.sql.types import (
    TimestampType, DoubleType, IntegerType, StringType, BooleanType,
    LongType, FloatType, DateType
)



class ColumnExpectation:
    @staticmethod
    def is_timestamp(column: str):
        """Check if column contains valid timestamps."""
        return F.col(column).cast(TimestampType()).isNotNull()

    @staticmethod
    def is_numeric(column: str):
        """Check if column contains numeric (double/float) values."""
        return F.col(column).cast(DoubleType()).isNotNull()

    @staticmethod
    def is_integer(column: str):
        """Check if column contains integer values."""
        return F.col(column).cast(IntegerType()).isNotNull()

    @staticmethod
    def is_string(column: str):
        """Check if column contains string values."""
        return F.col(column).cast(StringType()).isNotNull()

    @staticmethod
    def is_boolean(column: str):
        """Check if column contains boolean values."""
        return F.col(column).cast(BooleanType()).isNotNull()

    @staticmethod
    def is_long(column: str):
        """Check if column contains long integer values."""
        return F.col(column).cast(LongType()).isNotNull()

    @staticmethod
    def is_int32(column: str):
        """Check if column contains int32 values."""
        return F.col(column).cast(IntegerType()).isNotNull()

    @staticmethod
    def is_int64(column: str):
        """Check if column contains int64 values."""
        return F.col(column).cast(IntegerType()).isNotNull()

    @staticmethod
    def is_object(column: str):
        """Check if column contains string (object) values."""
        return F.col(column).cast(StringType()).isNotNull()

    @staticmethod
    def is_float(column: str):
        """Check if column contains float values."""
        return F.col(column).cast(FloatType()).isNotNull()

    @staticmethod
    def is_date(column: str):
        """Check if column contains date values."""
        return F.col(column).cast(DateType()).isNotNull()

    @staticmethod
    def is_positive(column: str):
        """Check if column contains positive values."""
        return F.col(column) > 0

    @staticmethod
    def regex_match(column: str, pattern: str):
        """Check if column values match the given regex pattern."""
        return F.col(column).rlike(pattern)

    @staticmethod
    def not_null(column: str):
        """Check if column is not null."""
        return F.col(column).isNotNull()
