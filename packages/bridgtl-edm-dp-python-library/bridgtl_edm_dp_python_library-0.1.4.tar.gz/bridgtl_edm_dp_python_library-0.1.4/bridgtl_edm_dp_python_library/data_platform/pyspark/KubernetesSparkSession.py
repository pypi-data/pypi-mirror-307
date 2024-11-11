import os
import socket
from typing import List

from pyspark import SparkConf
from pyspark.sql import SparkSession

from bridgtl_edm_dp_python_library.common import get_env_or_raise
from bridgtl_edm_dp_python_library.data_platform.pyspark.utility import copy_file_to_spark


class KubernetesSparkSession:
    def __init__(
            self,
            name: str,
            master: str | None = None,
            spark_ui_port: int = 4040,
            image: str | None = None,
            image_pull_policy: str = "IfNotPresent",

            google_service_account_path: str = None,

            executor_instances: int | None = None,
            executor_cores: int | None = None,
            executor_memory: str | None = None,

            jars: List[str] | None = None,
            packages: List[str] | None = None,

            config: dict | None = None
    ):
        self.name = name
        self.master = master or get_env_or_raise("KUBERNETES_SPARK_MASTER")
        self.spark_ui_port = spark_ui_port

        self.kubernetes_spark_image = image or get_env_or_raise("KUBERNETES_SPARK_IMAGE")
        self.kubernetes_spark_image_pull_policy = image_pull_policy

        self.google_service_account_path = google_service_account_path

        # Using the provided arguments or default values
        self.executor_instances = executor_instances or 1
        self.executor_cores = executor_cores or 1
        self.executor_memory = executor_memory or "4g"

        # Adding default jars if not provided
        self.jars = jars or []

        self.packages = packages or []

        # Initialize configuration with defaults and environment variables
        self.config = config or {}
        self._initialize_default_config()

    def _initialize_default_config(self):
        self.config["spark.bigquery.viewsEnabled"] = "true"

        self.config["spark.ui.port"] = self.spark_ui_port

        self.config["spark.kubernetes.container.image"] = self.kubernetes_spark_image
        self.config["spark.kubernetes.container.image.pullPolicy"] = self.kubernetes_spark_image_pull_policy

        self.config["spark.kubernetes.namespace"] = "jupyterhub"
        self.config["spark.kubernetes.container.image.pullSecrets"] = "gitlab-pull-secret"
        self.config["spark.driver.host"] = socket.gethostbyname(socket.gethostname())

        # Set executor configurations
        self.config["spark.executor.instances"] = self.executor_instances
        self.config["spark.executor.cores"] = self.executor_cores
        self.config["spark.executor.memory"] = self.executor_memory
        self.config["spark.kubernetes.executor.limit.cores"] = self.executor_cores

        # Google Cloud configurations

        if self.google_service_account_path:
            self.config["spark.hadoop.google.cloud.auth.service.account.enable"] = "true"
            self.config["spark.hadoop.google.cloud.auth.service.account.json.keyfile"] = self.google_service_account_path
            self.config["fs.AbstractFileSystem.gs.impl"] = "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS"
            self.config["spark.hadoop.fs.gs.impl"] = "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"

            # Extra Java options for GCP authentication
            self.config["spark.driver.extraJavaOptions"] = f"-DGOOGLE_APPLICATION_CREDENTIALS={self.google_service_account_path}"
            self.config["spark.executor.extraJavaOptions"] = f"-DGOOGLE_APPLICATION_CREDENTIALS={self.google_service_account_path}"

        # Google Cloud Storage configurations
        jars_str = ",".join(self.jars)
        self.config["spark.jars"] = jars_str

        packages_str = ",".join(self.packages)
        self.config["spark.jars.packages"] = packages_str

        # Logging configurations
        history_path = os.getenv("KUBERNETES_SPARK_HISTORY_PATH")
        if history_path:
            self.config["spark.eventLog.enabled"] = "true"
            self.config["spark.eventLog.rolling.enabled"] = "true"
            self.config["spark.eventLog.rolling.maxFileSize"] = "10m"
            self.config["spark.eventLog.dir"] = history_path
            self.config["spark.history.fs.logDirectory"] = history_path

    def create(self):
        config = SparkConf()

        for key, value in self.config.items():
            config.set(key, str(value))

        session = SparkSession.builder \
            .appName(self.name) \
            .master(self.master) \
            .config(conf=config) \
            .enableHiveSupport() \
            .getOrCreate()

        copy_file_to_spark(session, self.google_service_account_path)

        print(f"Spark UI: http://127.0.0.1:4040")

        return session
