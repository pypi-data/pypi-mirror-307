import json
from functools import wraps
from abc import abstractmethod
from typing import Any, Dict, Iterable

from dingo.io import InputArgs


class DataSource:
    """
    Represents the source of a dataset used in Dingo Tracking, providing information such as
    cloud storage location, delta table name / version, etc.
    """
    datasource_map = {}

    def __init__(self, input_args: InputArgs):
        self.input_args = input_args

    @staticmethod
    @abstractmethod
    def get_source_type() -> str:
        """Obtains a string representing the source type of the dataset.

        Returns:
            A string representing the source type of the dataset, e.g. "s3", "delta_table", ...

        """

    @abstractmethod
    def load(self) -> Iterable:
        """
        Loads files / objects referred to by the Datasource. For example, depending on the type
        of :py:class:`Datasource <dingo.data.datasource.Datasource>`, this may download
        source CSV files from S3 to the local filesystem, load a source Delta Table as a Spark
        DataFrame, etc.

        Returns:
            The downloaded source, e.g. a local filesystem path, a Spark DataFrame, etc.

        """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Obtains a JSON-compatible dictionary representation of the Datasource.

        Returns:
            A JSON-compatible dictionary representation of the Datasource.

        """

    def to_json(self) -> str:
        """
        Obtains a JSON string representation of the
        :py:class:`Datasource <dingo.data.datasource.Datasource>`.

        Returns:
            A JSON string representation of the
            :py:class:`Datasource <dingo.data.datasource.Datasource>`.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def register(cls):
        """
        Register a datasource. (register)

        """

        def decorator(root_class):
            cls.datasource_map[root_class.get_source_type()] = root_class

            @wraps(root_class)
            def wrapped_function(*args, **kwargs):
                return root_class(*args, **kwargs)

            return wrapped_function

        return decorator
