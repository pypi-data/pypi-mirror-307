import os

from .KubernetesSparkSession import KubernetesSparkSession


class JupyterKubernetesSparkSession(KubernetesSparkSession):

    def __init__(
            self,
            name: str,

            executor_instances: int = 1,
            executor_cores: int = 1,
            executor_memory: str = "4g",

            spark_ui_port: int = 4040,

            config: dict | None = None,
            **kwargs
    ):
        username = os.getenv('JUPYTERHUB_USER')

        config = config or {}

        if os.getenv("KUBERNETES_POD_NAME"):
            config["spark.kubernetes.driver.pod.name"] = os.getenv("KUBERNETES_POD_NAME")

        # Proxy configurations
        config["spark.ui.proxyBase"] = f"/user/{username}/vscode/proxy/{spark_ui_port}"
        config["spark.ui.proxyRedirectUri"] = "/"

        super().__init__(
            name=name,
            spark_ui_port=spark_ui_port,

            google_service_account_path=f"/home/{username}/.config/gcloud/application_default_credentials.json",

            executor_instances=executor_instances,
            executor_cores=executor_cores,
            executor_memory=executor_memory,

            config=config,
            **kwargs
        )
