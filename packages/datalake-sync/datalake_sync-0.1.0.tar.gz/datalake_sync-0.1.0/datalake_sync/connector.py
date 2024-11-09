from datalake_sync import *

class ConfigLoader:
    def __init__(self, config, spark: SparkSession):
        self.spark = spark
        self.config = self._load_config(config)
        self._set_adls_credentials()

    def _load_config(self, config):
        if isinstance(config, dict):
            return config
        elif isinstance(config, str):
            with open(config, 'r') as file:
                return json.load(file)
        else:
            raise TypeError("Config must be a dictionary or a valid file path.")

    def _set_adls_credentials(self):
        azure_account_name = self.config.get("account_name")
        azure_account_key = self.config.get("account_key")
        use_service_principal = self.config.get("use_service_principal", False)

        if azure_account_key:
            self.spark.conf.set(f"fs.azure.account.key.{azure_account_name}.dfs.core.windows.net", azure_account_key)
        elif use_service_principal:
            client_id = self.config.get("client_id")
            tenant_id = self.config.get("tenant_id")
            client_secret = self.config.get("client_secret")

            self.spark.conf.set(f"fs.azure.account.auth.type.{azure_account_name}.dfs.core.windows.net", "OAuth")
            self.spark.conf.set(f"fs.azure.account.oauth.provider.type.{azure_account_name}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
            self.spark.conf.set(f"fs.azure.account.oauth2.client.id.{azure_account_name}.dfs.core.windows.net", client_id)
            self.spark.conf.set(f"fs.azure.account.oauth2.client.secret.{azure_account_name}.dfs.core.windows.net", client_secret)
            self.spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{azure_account_name}.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")
        else:
            raise ValueError("Either 'account_key' or Service Principal credentials (client_id, tenant_id, client_secret) must be provided.")

    def get_abfss_url(self):
        container = self.config.get("container")
        account_name = self.config.get("account_name")
        directory = self.config.get("directory")
        return f"abfss://{container}@{account_name}.dfs.core.windows.net/{directory}" if directory else f"abfss://{container}@{account_name}.dfs.core.windows.net/"

    def get_file_type(self):
        return self.config["file_type"]

class FileReader:
    def __init__(self, config_loader: ConfigLoader, ingestion_detail: dict):
        self.config_loader = config_loader
        self.ingestion_detail = ingestion_detail
        self.file_type = ingestion_detail["file_type"]

    def read_files_df(self, spark: SparkSession):
        abfss_url = self.config_loader.get_abfss_url()

        if self.file_type == "json":
            reader = JSONReader(self.config_loader, self.ingestion_detail)
            return reader.read_json(spark, abfss_url)
        elif self.file_type == "csv":
            reader = CSVReader(self.config_loader, self.ingestion_detail)
            return reader.read_csv(spark, abfss_url)
        elif self.file_type == "parquet":
            reader = ParquetReader(self.config_loader, self.ingestion_detail)
            return reader.read_parquet(spark, abfss_url)
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

class JSONReader:
    def __init__(self, config_loader: ConfigLoader, ingestion_detail: dict):
        self.config_loader = config_loader
        self.ingestion_detail = ingestion_detail

    def read_json(self, spark: SparkSession, path: str):
        return (spark.readStream
                .format("cloudFiles")
                .option("cloudFiles.format", "json")
                .option("cloudFiles.schemaLocation", self.ingestion_detail["schema_location"])
                .load(path))

class CSVReader:
    def __init__(self, config_loader: ConfigLoader, ingestion_detail: dict):
        self.config_loader = config_loader
        self.ingestion_detail = ingestion_detail

    def read_csv(self, spark: SparkSession, path: str):
        options = self.ingestion_detail.get("options", {})
        return (spark.readStream
                .format("cloudFiles")
                .option("cloudFiles.format", "csv")
                .option("cloudFiles.schemaLocation", self.ingestion_detail["schema_location"])
                .options(**options)
                .load(path))

class ParquetReader:
    def __init__(self, config_loader: ConfigLoader, ingestion_detail: dict):
        self.config_loader = config_loader
        self.ingestion_detail = ingestion_detail

    def read_parquet(self, spark: SparkSession, path: str):
        return (spark.readStream
                .format("cloudFiles")
                .option("cloudFiles.format", "parquet")
                .option("cloudFiles.schemaLocation", self.ingestion_detail["schema_location"])
                .load(path))

class DeltaWriter:
    def __init__(self, config_loader: ConfigLoader, ingestion_detail: dict):
        self.config_loader = config_loader
        self.ingestion_detail = ingestion_detail
        self.checkpoint_location = ingestion_detail["checkpoint_location"]
        self.merge_column_key = ingestion_detail["merge_column_key"]
        self.output_table = ingestion_detail["output_table"]

    def merge_into_delta(self, spark, df):
        def upsert_to_delta(batch_df, batch_id):
            delta_table = DeltaTable.forName(spark, self.output_table)
            merge_condition = " AND ".join([f"target.{col} = source.{col}" for col in self.merge_column_key])
            delta_table.alias("target").merge(batch_df.alias("source"), merge_condition)\
                .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        (df.writeStream
           .format("delta")
           .option("checkpointLocation", self.checkpoint_location)
           .foreachBatch(upsert_to_delta)
           .trigger(once=True))
        

    def write_to_delta(self, df):
        (df.writeStream
           .format("delta")
           .option("checkpointLocation", self.checkpoint_location)
           .trigger(once=True)
           .table(self.output_table))

    def write_to_delta_table(self, spark, df):
        if not spark.catalog.tableExists(self.output_table):
            self.write_to_delta(df)
        else:
            self.merge_into_delta(spark, df)