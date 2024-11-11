import os
import json
from pathlib import Path
from traitlets import Unicode
from traitlets.config import Configurable, Config
from jupyter_core.paths import jupyter_config_dir


class JupyterLabS3(Configurable):
    """
    Config options for jupyterlab_minio
    """

    url = Unicode(
        default_value=os.environ.get("MINIO_ENDPOINT", ""),
        config=True,
        help="The url for the S3 api",
    )
    accessKey = Unicode(
        default_value=os.environ.get("MINIO_ACCESS_KEY", ""),
        config=True,
        help="The client ID for the S3 api",
    )
    secretKey = Unicode(
        default_value=os.environ.get("MINIO_SECRET_KEY", ""),
        config=True,
        help="The client secret for the S3 api",
    )

    def get_config(self) -> Config:
        """
        Returns a standalone Config object with the same configurations.
        """
        return self.config

    def get_config_as_dict(self) -> dict:
        """
        Converts the Config object to a dictionary, resolving LazyConfigValues.
        """
        # Use the `to_dict()` method to resolve LazyConfigValue objects
        return self.config.to_dict()
    

class EnvironmentManager:
    
    def update_env_var(self, var_name, var_value):
        """Add a new environment variable or update its value if it exists."""
        os.environ[var_name] = var_value


    def remove_env_var(self, var_name):
        """Remove an environment variable if it exists."""
        if var_name in os.environ:
            del os.environ[var_name]


    def get_env_var(self, var_name):
        """Retrieve the value of an environment variable."""
        return os.environ.get(var_name, None)


class MinIOConfigHelper:
    """
    A helper class to add or update aliases in the MinIO configuration JSON file.
    """

    def __init__(self, alias_name=None, config_path=None):
        # Path to the MinIO configuration file
        self.config_path = Path(config_path) if config_path else Path("{}/.mc/config.json".format(Path.home()))
        self.alias_name = alias_name or "storage"

    def load_config(self):
        """Loads the MinIO configuration file as a dictionary."""
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            return {}
        
        with open(self.config_path, 'r') as file:
            return json.load(file)
    
    def save_config(self, config):
        """Saves the modified configuration back to the JSON file."""
        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=4)
    
    def update_alias(self, url, access_key, secret_key):
        """
        Adds or updates an alias in the MinIO configuration.
        """
        # Load existing config
        config = self.load_config()
        
        # Ensure "version" section exists in the configuration
        if "version" not in config:
            config["version"] = "10"

        # Ensure "aliases" section exists in the configuration
        if "aliases" not in config:
            config["aliases"] = {}
        
        # Update or add the alias
        config["aliases"][self.alias_name] = {
            "url": url or "",
            "accessKey": access_key or "",
            "secretKey": secret_key or "",
            "api": "S3v4",
            "path": "auto"
        }
        
        # Save the modified config
        self.save_config(config)
            
    def remove_alias(self):
        """
        Removes an alias from the MinIO configuration if it exists.
        """
        # Load existing config
        config = self.load_config()
        
        # Check if the alias exists and remove it
        if "aliases" in config and self.alias_name in config["aliases"]:
            del config["aliases"][self.alias_name]
            self.save_config(config)

    def remove_config_path(self):
        """ delete config path """
        if self.config_path.exists():
            os.remove(self.config_path)

    def get_alias_dict(self):
        """
        get alias from the MinIO configuration if it exists.
        """
        # Load existing config
        config = self.load_config()
        
        alias = {
            "url": "",
            "accessKey": "",
            "secretKey": ""
        }
        # Check if the alias exists and remove it
        if "aliases" in config and self.alias_name in config["aliases"]:
            al = config["aliases"][self.alias_name]
            alias["url"] = al.get("url", "")
            alias["accessKey"] = al.get("accessKey", "")
            alias["secretKey"] = al.get("secretKey", "")
        return alias


    @property
    def config(self):
        minio_dict={}
        minio_dict["JupyterLabS3"] = self.get_alias_dict()
        config = Config(minio_dict)
        return JupyterLabS3(config = config)
    
    @property
    def exist(self):
        alias = self.get_alias_dict()
        return all([alias["url"], alias["accessKey"], alias["secretKey"]])
