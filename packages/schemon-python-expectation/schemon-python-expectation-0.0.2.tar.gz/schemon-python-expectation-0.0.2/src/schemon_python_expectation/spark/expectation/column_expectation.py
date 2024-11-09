from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf
import pandas as pd
import inspect


class ColumnExpectation:
    @staticmethod
    @pandas_udf("boolean")
    def is_timestamp(column: pd.Series) -> pd.Series:
        """Check if column contains valid timestamps."""
        return pd.to_datetime(column, errors="coerce").notna()

    @staticmethod
    @pandas_udf("boolean")
    def is_numeric(column: pd.Series) -> pd.Series:
        """Check if column contains numeric (double/float) values."""
        return pd.to_numeric(column, errors="coerce").notna()

    @staticmethod
    @pandas_udf("boolean")
    def is_integer(column: pd.Series) -> pd.Series:
        """Check if column contains integer values."""
        # Coerce non-numeric values to NaN and then check if the remaining values are integers
        numeric_column = pd.to_numeric(column, errors="coerce")
        return numeric_column.notna() & numeric_column.apply(lambda x: float(x).is_integer())

    @staticmethod
    @pandas_udf("boolean")
    def is_string(column: pd.Series) -> pd.Series:
        """Check if column contains string values."""
        return column.apply(lambda x: isinstance(x, str))

    @staticmethod
    @pandas_udf("boolean")
    def is_boolean(column: pd.Series) -> pd.Series:
        """Check if column contains boolean values."""
        return column.apply(lambda x: isinstance(x, bool))

    @staticmethod
    @pandas_udf("boolean")
    def is_long(column: pd.Series) -> pd.Series:
        """Check if column contains long integer values."""
        return pd.to_numeric(column, errors="coerce").apply(
            lambda x: isinstance(x, (int, float)) and x.is_integer()
        )

    @staticmethod
    @pandas_udf("boolean")
    def is_int32(column: pd.Series) -> pd.Series:
        """Check if column contains int32 values."""
        return pd.to_numeric(column, errors="coerce").apply(
            lambda x: -(2**31) <= x < 2**31
        )

    @staticmethod
    @pandas_udf("boolean")
    def is_int64(column: pd.Series) -> pd.Series:
        """Check if column contains int64 values."""
        return pd.to_numeric(column, errors="coerce").apply(
            lambda x: -(2**63) <= x < 2**63
        )

    @staticmethod
    @pandas_udf("boolean")
    def is_object(column: pd.Series) -> pd.Series:
        """Check if column contains string (object) values."""
        return column.apply(lambda x: isinstance(x, str))

    @staticmethod
    @pandas_udf("boolean")
    def is_float(column: pd.Series) -> pd.Series:
        """Check if column contains float values."""
        return pd.to_numeric(column, errors="coerce").apply(
            lambda x: isinstance(x, float)
        )

    @staticmethod
    @pandas_udf("boolean")
    def is_date(column: pd.Series) -> pd.Series:
        """Check if column contains only date values (no time component)."""
        def is_date_only(value):
            try:
                # Convert to datetime
                date_value = pd.to_datetime(value, errors="coerce")
                # Check if value is valid and time component is zero
                return date_value is not pd.NaT and date_value == date_value.normalize()
            except Exception:
                return False
        
        return column.apply(is_date_only)

    @staticmethod
    @pandas_udf("boolean")
    def is_positive(column: pd.Series) -> pd.Series:
        """Check if column contains positive values."""
        return column > 0

    @staticmethod
    def regex_match(pattern: str):
        """Returns a Pandas UDF function that matches a regex pattern."""
        @pandas_udf("boolean")
        def inner_regex_match(column: pd.Series) -> pd.Series:
            return column.str.match(pattern)
        return inner_regex_match

    @staticmethod
    @pandas_udf("boolean")
    def not_null(column: pd.Series) -> pd.Series:
        """Check if column is not null."""
        return column.notna()