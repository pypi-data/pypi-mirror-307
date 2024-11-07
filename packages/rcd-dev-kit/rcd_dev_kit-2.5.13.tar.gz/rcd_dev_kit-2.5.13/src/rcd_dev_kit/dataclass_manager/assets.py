import os

import datetime
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Type, Union

from rcd_dev_kit.database_manager import (
    RedshiftOperator,
    read_from_redshift,
    send_to_redshift,
)
from .raw_data_file import RawDataFile
from ..pandas_manager import check_duplication, check_na
from sqlalchemy import (
    inspect, text
)
from sqlalchemy.engine.reflection import Inspector


""" Assets """


class DataAsset:
    """
    Base class for managing data assets within the Tekkare environment.

    Attributes:
        __asset_type__ (str): Type of the asset.
        asset_key (str): Key identifying the asset.

    Methods:
        __init__(): Initializes a new instance of the DataAsset class.
        get_asset_key(): Retrieves the asset key.
    """

    __asset_type__: str = NotImplemented
    asset_key: str = NotImplemented

    def __init__(self) -> None:
        pass

    def get_asset_key(self):
        """
        Retrieves the asset key.

        Returns:
            str: The asset key.
        """
        return self.asset_key


""" Table Asset """


class Table(DataAsset):
    """
    Table Asset.

    Represents a dataset table, providing methods to interact with its schema,
    columns, and data.

    Attributes:
    ----------
    __asset_type__ : str
        The type of asset, set to "Dataset".
    is_dictionary : bool
        Indicates if the table is represented as a dictionary format.
    table_name : str
        The name of the table.
    schema_name : str
        The schema of the table.
    model_class : SQLAlchemy model
        The SQLAlchemy model class representing the table structure.
    ro : RedshiftOperator
        RedshiftOperator instance for database operations.
    engine : SQLAlchemy engine
        The engine connected to the database.
    asset_key : str
        Unique key identifying the asset in the format "{schema_name}.{table_name}".
    start_period : None
        Placeholder for the start period of data (not initialized in __init__).
    end_period : None
        Placeholder for the end period of data (not initialized in __init__).
    inspector : Inspector
        SQLAlchemy Inspector for introspecting the table structure.
    dct__python_type : dict
        Dictionary mapping column names to their expected Python types based on SQL types.
    _df : pandas.DataFrame or None
        Internal storage for the DataFrame representation of the table (None by default).

    Properties:
    -----------
    df : pandas.DataFrame or None
        Getter and setter property for the DataFrame representation of the table.
    lst__primary_key : list
        List of primary key column names in the table.
    lst__non_nullable_cols : list
        List of column names that are non-nullable.
    dct__sql_type : dict
        Dictionary mapping column names to their SQLAlchemy column types.
    
    Methods:
    --------
    __init__(self, table_model, is_dictionary: bool = False)
        Initializes the Table instance with table metadata and database connections.
    check_if_table_exists(self)
        Checks if the table exists in the database.
    """
    __asset_type__ = "Dataset"

    def __init__(self, table_model, is_dictionary: bool = False):
        """
        Initialize the Table instance.

        Args:
        ----
        table_model : SQLAlchemy model
            SQLAlchemy model representing the table structure.
        is_dictionary : bool, optional, default=False
            Indicates if the table is represented in dictionary format.

        Initializes attributes including table metadata, database connections,
        and extracts column Python types from SQL types.
        """
        self.is_dictionary = is_dictionary
        
        self.table_name = table_model.__tablename__
        self.schema_name = table_model.__schema__
        self.model_class = table_model
        
        self.ro = RedshiftOperator(database='staging')
        self.ro.schema = table_model.__schema__
        self.ro.table = table_model.__tablename__
        self.engine = self.ro.engine
        
        self.asset_key = f"{self.schema_name}.{self.table_name}"
        self.start_period = None
        self.end_period = None
        super().__init__()
        self.inspector = inspect(self.model_class)
        self.dct__python_type = self.extract_column_types_python()
        self._df = None

    """ 
    ========================================
        SETTERS / PROPERTIES
    ========================================

    This section contains the setter methods and properties 
    for managing the internal state and variables of the class. 
    It includes direct property definitions, getter and setter 
    methods, and other methods that facilitate the modification 
    of key attributes in a controlled manner.

    These properties and setters allow for controlled access 
    to class variables, ensuring proper encapsulation and 
    maintaining data integrity when interacting with the internal 
    state of the class.

    Use these methods to get or modify the class's internal 
    data without directly accessing the variables.

    """
    @property
    def df(self):
        """
        pandas.DataFrame or None: Getter and setter property for the DataFrame representation of the table.
        """
        return self._df

    @df.setter
    def df(self, dataframe):
        """
        Setter for the DataFrame representation of the table.

        Args:
        ----
        dataframe : pandas.DataFrame
            DataFrame to set as the representation of the table.
        """
        print("Setting DataFrame")
        self._df = dataframe

    @property
    def lst__primary_key(self):
        """
        list: List of primary key column names in the table.
        """
        return [column.name for column in self.inspector.primary_key]
    
    @property
    def lst__columns(self):
        """
        list: List of primary key column names in the table.
        """
        return [column.name for column in self.inspector.columns]

    @property
    def lst__non_nullable_cols(self):
        """
        list: List of column names that are non-nullable.
        """
        return [
            column.name
            for column in self.inspector.columns.values()
            if not column.nullable
        ]

    @property
    def dct__sql_type(self):
        """
        dict: Dictionary mapping column names to their SQLAlchemy column types.
        """
        # Create an inspector for the model's table
        return {column.name: column.type for column in self.inspector.columns.values()}

    """ 
    ========================================
        UTILITY FUNCTIONS
    ========================================

    This section contains utility functions that provide 
    specialized support for various tasks within the codebase. 
    These functions are designed to be reusable and modular, 
    performing common operations that can be leveraged across 
    the system.

    - `extract_column_types_python`: A function that retrieves 
      and processes the column types of a dataset, ensuring the 
      appropriate types are handled correctly for further data 
      manipulation or processing.
      
    - `update_comments`: A function responsible for updating 
      or adding comments to data structures, ensuring that 
      documentation or annotations are correctly applied to 
      columns, tables, or other elements.

    Use these functions when you need to perform data-type 
    extraction or manage comment updates without repeating code 
    throughout the system.

    """
    
    def extract_column_types_python(self):
        """
        Extract Python types from self.dct__sql_type.

        Returns:
        -------
        dict
            A dictionary mapping column names to their expected Python types based on self.dct__sql_type.
        """
        return {
            column_name: expected_type.python_type
            for column_name, expected_type in self.dct__sql_type.items()
        }
    
    def update_comments(self):
        """
        Updates column comments in the database to match the comments defined in the model class.

        This method iterates over the columns of the table, retrieves the comments 
        set in the model class, and applies them to the respective columns in the database. 
        If a column has a comment defined, it constructs an SQL `ALTER TABLE` statement to 
        set the comment on the corresponding column in the database.

        Notes:
            - The operation is performed using a connection to the database engine.
            - The SQL command is constructed dynamically for each column with an associated comment.
            - Currently, the actual database modification is commented out for testing purposes.

        Example:
            If the model class has a column with the comment "Stores the user's email address",
            this method will update the database to set that comment on the corresponding column.
        """
        with self.engine.connect() as conn:
            for column in self.inspector.columns.values():
                column_name = column.name
                comment = column.comment

                # Skip if no comment is set for this column
                if comment:
                    sql = f"ALTER TABLE {self.table_name} ALTER COLUMN {column_name} SET COMMENT :comment"
                    print(f"Updating column comment for '{column_name}' in table '{self.table_name}': '{comment}'")
                    conn.execute(text(sql), {"comment": comment})
    
    """ 
    ========================================
        VALIDATORS AND CHECKS
    ========================================

    This section contains functions responsible for validating 
    and ensuring the integrity, consistency, and correctness 
    of the data before further processing or transfer to external 
    systems. These functions help maintain high data quality by 
    checking that the data meets predefined criteria, adheres to 
    expected formats, and is free from errors or inconsistencies.

    The validations include checks for missing values, data types, 
    value ranges, column consistency, and other business logic rules 
    required for the data to be processed correctly.

    These functions are used to perform essential pre-processing 
    checks, ensuring that invalid data is caught early and preventing 
    errors in downstream operations.

    """
    
    def check_if_table_exists(self):
        """
        Check if the specified table exists in the database.

        This function uses the database inspector to verify the 
        existence of the table by checking the table's presence 
        in the database schema.

        Returns:
        -------
        bool
            True if the table exists in the database, False otherwise.
        """
        insp = Inspector.from_engine(self.engine)
        table_exist = insp.has_table(self.table_name, schema=self.schema_name)
        return table_exist
        
    def check_data_types(self):
        """
        Validate and convert columns in the DataFrame (`self.df`) to 
        the specified data types in `self.dct__python_type`.

        The function checks each column in the DataFrame and attempts 
        to convert it to the type specified in the dictionary `self.dct__python_type`. 
        For columns requiring date conversion, it uses `pd.to_datetime` and raises 
        a `ValueError` if conversion fails.

        Returns:
        -------
        pandas.DataFrame
            The DataFrame with columns converted to the specified data types.

        Raises:
        ------
        ValueError
            If there is an error converting a column to `datetime.date` or other 
            specified types.
        """

        for col, dtype in self.dct__python_type.items():
            if dtype == datetime.date:
                try:
                    self.df[col] = pd.to_datetime(self.df[col]).dt.date
                except ValueError as e:
                    raise ValueError(f"Error converting column '{col}' to datetime: {str(e)}")
            else:
                self.df[col] = self.df[col].astype(dtype)
        
    def check_non_nullable_columns(self):
        """
        Check that non-nullable columns in the DataFrame do not contain missing values.

        This function inspects the table's schema and checks whether the 
        non-nullable columns contain any missing (null) values in the 
        DataFrame. If any such values are found, it raises a `ValueError`.

        Raises:
        ------
        ValueError
            If non-nullable columns contain missing values.
        """
        nullable_columns = [
            column.name
            for column in self.model_class.__table__.columns
            if not column.nullable
        ]
        missing_values = self.df[nullable_columns].isnull().any()
        if missing_values.any():
            raise ValueError(
                f"Non-nullable columns contain missing values: {missing_values[missing_values].index.tolist()}"
            )

    def check_columns(self):
        """
        Validate that the DataFrame contains only the expected columns.

        This function compares the columns present in the DataFrame 
        (`self.df`) with the expected columns listed in `self.lst__columns`. 
        If there are extra columns or missing columns, a `ValueError` is raised.

        Raises:
        ------
        ValueError
            If extra columns are found in the DataFrame.
            If expected columns are missing from the DataFrame.
        """
        actual_set = set(self.df.columns)
        expected_set = set(self.lst__columns)
        
        # Check if there are extra columns in the DataFrame
        extra_columns = actual_set - expected_set
        if extra_columns:
            raise ValueError(f"Extra columns found: {', '.join(extra_columns)}")
        
        # Check if there are missing columns in the DataFrame
        missing_columns = expected_set - actual_set
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
    
    def validate_dataframe(self):
        """
        Perform a full validation of the DataFrame against multiple checks.

        This function validates the DataFrame by running various checks 
        to ensure the data meets the required quality and consistency 
        standards, such as verifying data types, non-nullable columns, 
        and the presence of expected columns.

        The function also checks for missing values in non-nullable columns 
        and checks for duplicate entries in the primary key columns.

        Raises:
        ------
        ValueError
            If any of the checks fail (e.g., missing values, wrong data types, etc.).
        """
        # self.check_missing_values()
        self.check_data_types()
        self.check_non_nullable_columns()

        check_na(self.df.loc[:, self.lst__non_nullable_cols], raise_error=True)
        check_duplication(self.df, lst_col=self.lst__primary_key, raise_error=True)
        
    """ 
    ========================================
        REDSHIFT DATA TRANSFER FUNCTIONS
    ========================================

    This section contains functions responsible for sending data 
    to Redshift. These functions handle the process of preparing, 
    formatting, and transmitting data from the application to Redshift 
    tables or staging areas.

    Each function ensures that the data is validated, formatted, and 
    transferred to the correct Redshift schemas or tables, maintaining 
    integrity and consistency across the database.

    Use these functions whenever there is a need to push data to 
    Redshift as part of the ETL (Extract, Transform, Load) pipeline 
    or any data synchronization process.


    """
    
    def create_table(self, database: str = "staging"):
        """
        Create the table structure in Redshift.

        This function uses the RedshiftOperator to create a new table 
        in the specified schema of Redshift. The table structure is 
        generated based on the metadata from the model class.

        Args:
        -----
        database (str): The Redshift database where the table will be created (default is 'staging').
        """
        ro = RedshiftOperator(database=database)
        ro.schema = self.schema_name
        ro.table = self.table_name

        # Use the model class metadata to create the table in Redshift
        self.model_class.metadata.create_all(ro.engine)

    def read_table(self, database: str = "staging"):
        """
        Read data from a table in Redshift into a DataFrame.

        This function retrieves data from a specified Redshift table 
        and stores it in the `self.df` DataFrame.

        Args:
        -----
        database (str): The Redshift database from which data is read (default is 'staging').
        """
        self.df = read_from_redshift(
            database=database,
            schema=self.schema_name,
            table=self.table_name,
            method="auto",
        )

    def extract_periods_from_dataframe(self, period_variable : str = "period") -> None:
        """
        Extract the start and end periods from the DataFrame.

        This function calculates the start and end periods based on 
        the `period_variable` column in the DataFrame. The periods are 
        determined by finding the minimum and maximum values in the column.

        Args:
        -----
        period_variable (str): The name of the column containing the period data (default is 'period').
        """

        if self.is_dictionary:
            current_year = datetime.datetime.now().year

            self.start_period = str(current_year)
            self.end_period = str(current_year)
        else:
            if self._df is not None:
                try:
                    # Assuming 'period' column exists in _df DataFrame
                    self.start_period = str(self._df[period_variable].min())
                    self.end_period = str(self._df[period_variable].max())
                    print(
                        f"Start period: {self.start_period}, End period: {self.end_period}"
                    )
                except KeyError:
                    print("Error: 'period' column not found in _df DataFrame.")
            else:
                print("Error: _df DataFrame is not set.")

    def overwrite_table(self) -> None:
        """
        Overwrite an existing table in Redshift.

        This function first checks if the table exists. If it does not, 
        it creates the table. Then, it overwrites the data in the table 
        with the DataFrame's contents.

        """
        if not self.check_if_table_exists():
            self.create_table()
        
        self.dataframe_to_redshift(mode="overwrite")

    def update_table(self) -> None:
        """
        Update an existing table in Redshift.

        This function updates the existing table in Redshift by using 
        the `merge_update` mode for transferring data.
        """
        self.dataframe_to_redshift(mode="merge_update")

    def from_staging_to_prod(self) -> None:
        """
        Transfer data from the staging table to the production table.

        This function reads data from the staging table and transfers it 
        to the production environment. It uses the `overwrite` mode to 
        ensure the production table is replaced with the updated data.
        """

        self.read_table()
        self.dataframe_to_redshift(mode="overwrite", database="oip")

    def dataframe_to_redshift(
        self, mode: str = "overwrite", database: str = "staging", extract_periods : bool = False , period_variable : str = None
    ) -> None:
        """
        Send a DataFrame to Redshift.

        This function sends the contents of `self._df` to a Redshift table. 
        It validates the DataFrame and optionally extracts periods from 
        the data based on the provided period column.

        Args:
        -----
        mode (str): The mode for writing data to Redshift ('overwrite' or 'merge_update').
        database (str): The Redshift database to write to (default is 'staging').
        extract_periods (bool): Flag indicating if the start and end periods should be extracted (default is False).
        period_variable (str): The name of the period column to extract periods from (default is None).
        """

        # Retrieve table information
        self.validate_dataframe()
        
        if extract_periods:
            if period_variable is not None:
                self.extract_periods_from_dataframe(period_variable=period_variable)
            else:
                self.extract_periods_from_dataframe()
                
        # Reorder columns according to the specified order in lst__columns
        # Ensure that all columns in lst__columns exist in _df before reordering
        self._df = self._df[self.lst__columns]
        
        send_to_redshift(
            database=database,
            schema=self.schema_name,
            table=self.table_name,
            mode=mode,
            primary_key=self.lst__primary_key,
            column_pivot=self.lst__primary_key,
            df=self._df,
            start_period=self.start_period,
            end_period=self.end_period,
            dct_aws_type=self.dct__sql_type,
        )


""" ETL Asset """


class ETLOperator(DataAsset, ABC):
    """
    Base class for ETL (Extract, Transform, Load) operators.

    Attributes:
        __asset_type__ (str): Type identifier for ETL processes.
        asset_key (str): Key for identifying the asset.
        dct_input (Dict[str, Union[RawDataFile, Type[RawDataFile]]]): Input data sources.
        output (DataAsset): Output data asset.
    """

    __asset_type__: str = "etl_process"
    asset_key: str = NotImplemented
    dct_input: Dict[str, Union[RawDataFile, Type[DataAsset]]] = NotImplemented
    dct_output: Dict[str, Union[RawDataFile, Type[DataAsset]]] = NotImplemented

    def __init__(self):
        """
        Initialize the ETL operator and validate input/output.
        """
        self._validate_input()
        self._validate_output()
        super().__init__()

    @classmethod
    def _validate_input(cls) -> None:
        """
        Validate the input data sources.

        Raises:
            TypeError: If input is not a DataAsset or a subclass of RawDataFile.
        """
        for key, source in cls.dct_input.items():
            if not isinstance(source, DataAsset) and not (
                isinstance(source, RawDataFile) or issubclass(type(source), RawDataFile)
            ):
                raise TypeError(
                    f"Value associated with key '{key}' must be an instance of DataAsset or a subclass of RawDataFile"
                )

    @classmethod
    def _validate_output(cls) -> None:
        """
        Validate the input data sources.

        Raises:
            TypeError: If input is not a DataAsset or a subclass of RawDataFile.
        """
        for key, source in cls.dct_output.items():
            if not isinstance(source, DataAsset) and not (
                isinstance(source, RawDataFile) or issubclass(type(source), RawDataFile)
            ):
                raise TypeError(
                    f"Value associated with key '{key}' must be an instance of DataAsset or a subclass of RawDataFile"
                )

    def process(self):
        """
        Perform the ETL process: get raw data, transform, and load.
        """
        self.get_raw_data()
        self.transform()
        self.load()

    @abstractmethod
    def get_raw_data(self):
        """
        Abstract method to extract raw data.
        """
        pass

    @abstractmethod
    def transform(self):
        """
        Abstract method to transform the data.
        """
        pass

    @abstractmethod
    def load(self):
        """
        Abstract method to load the transformed data.

        Also sends metadata to Directus.
        """
        self.send_metadata_to_directus()

    def get_metadata(self):
        """
        Extract metadata about input, process, and output.

        Returns:
            Dict: Metadata dictionary.
        """
        lst_source = []

        for key, source in self.dct_input.items():
            if isinstance(source, RawDataFile):
                dct_source = {
                    "asset_type": "RawDataFile",
                    "asset_value": {
                        "source_uuid": source.source_uuid,
                        "file_name": source.file_name,
                    },
                }
            elif isinstance(source, DataAsset):
                dct_source = {
                    "asset_type": source.__asset_type__,
                    "asset_key": source.get_asset_key(),
                }
            else:
                raise ValueError("Data Asset source type not recognized")

            lst_source.append(dct_source)

        return {
            "lst_input": self.get_metadata_info(self.dct_input),
            "etl_process": {
                "asset_key": self.get_asset_key(),
                "asset_type": self.__asset_type__,
            },
            "output": self.get_metadata_info(self.dct_output),
        }

    def get_metadata_info(self, dct_asset: dict):
        """
        Extract metadata about input, process, and output.

        Returns:
        """
        lst_metadata = []

        for key, source in dct_asset.items():
            if isinstance(source, RawDataFile):
                dct_metadata = {
                    "asset_type": "RawDataFile",
                    "asset_value": {
                        "source_uuid": source.source_uuid,
                        "file_name": source.file_name,
                    },
                }
            elif isinstance(source, DataAsset):
                dct_metadata = {
                    "asset_type": source.__asset_type__,
                    "asset_key": source.get_asset_key(),
                }
            else:
                raise ValueError("Data Asset source type not recognized")

            lst_metadata.append(dct_metadata)
