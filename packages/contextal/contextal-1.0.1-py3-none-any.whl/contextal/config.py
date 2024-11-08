"""
Platform configuration
"""

import logging
import os
import os.path
import platformdirs
import re

import tomlkit

LOG = logging.getLogger(__name__)


class Config:
    """Management for the on-file platform configuration"""

    def __init__(self, path: str | None = None):
        """
        Initialize the configuration management

        An alternative file can be optionally provided through the path parameter
        """
        self.path = path or os.path.join(
            platformdirs.user_config_dir("contextal"), "config.toml"
        )
        self.url = None
        self.token = None

    def _load_config(self) -> tomlkit.TOMLDocument:
        with open(self.path, "rb") as f:
            return tomlkit.load(f)

    @staticmethod
    def _validate_profile_name(profile_name):
        if not profile_name or not re.fullmatch(r'[a-z0-9A-Z][-_a-z0-9A-Z]*', profile_name):
            raise ValueError("Invalid profile name")

    @staticmethod
    def _validate_url(url):
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("Invalid platform URL")

    def _write_config(self, config):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(
                os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600),
                "w",
                encoding="utf-8",
            ) as f:
                tomlkit.dump(config, f)
        except Exception as e:
            LOG.warning("Failed to save configuration to %s: %s", self.path, e)
            raise

    def load_profile(self, profile_name: str | None = None):
        """
        Load the indicated (or the default if None) profile from the configuration file

        Configuration selection happens in the following order:
          * the configuration profile indicated by the `profile_name` parameter, if provided
          * the configuration profile indicated by the environmental variable `CTX_PROFILE`, if set
          * the (url, [token]) pair indicated by by the environmental variable `CTX_URL`
            (and optionally `CTX_TOKEN`), if set
          * the default profile indicated in the configuration file, if present
        """
        if not profile_name:
            profile_name = os.environ.get("CTX_PROFILE")
        if not profile_name:
            env_url = os.environ.get("CTX_URL")
            if env_url:
                try:
                    self._validate_url(env_url)
                except ValueError as exc:
                    raise ValueError(
                        "The CTX_URL environment variable does not contain a valid url"
                    ) from exc
                self.url = env_url
                self.token = os.environ.get("CTX_TOKEN")
                return
        if profile_name:
            self._validate_profile_name(profile_name)
            profile = profile_name
        try:
            config = self._load_config()
            if not profile_name:
                profile = config.get("default")
            if profile is None:
                raise ValueError(
                    "The default profile name is not set in the configuration file"
                )
            platform = config.get("platform", {}).get(profile, {})
            if not platform:
                raise ValueError(
                    "The {} profile was not found in the configuration file".format(
                        "specified" if profile_name else "default"
                    )
                )
            url = str(platform.get("url"))
            token = platform.get("token")
            try:
                self._validate_url(url)
            except ValueError as exc:
                raise ValueError(
                    "The {} profile does not contain a valid url".format(
                        "specified" if profile_name else "default"
                    )
                ) from exc
            self.url = url
            if token:
                self.token = str(token)
            else:
                self.token = None
            LOG.debug(
                "Loaded profile %s from configuration file %s", profile, self.path
            )
        except Exception as e:
            LOG.debug("Failed to load configuration from %s: %s", self.path, e)
            raise

    def write_profile(
        self,
        profile_name: str,
        platform_url: str,
        platform_token: str | None,
        make_default: bool = False,
    ):
        """
        Create or update a profile in the configuration file

        If make_default is True, the profile is set as the default

        """
        self._validate_profile_name(profile_name)
        self._validate_url(platform_url)
        try:
            config = self._load_config()
        except Exception:
            config = tomlkit.TOMLDocument()
        if "platform" not in config:
            config.add("platform", {})
        profile_data = {
            "url": platform_url,
        }
        if platform_token:
            profile_data["token"] = platform_token
        config["platform"][profile_name] = profile_data
        if make_default:
            config["default"] = profile_name
        self._write_config(config)

    def delete_profile(
        self,
        profile_name: str,
    ) -> bool:
        """Delete a profile from the configuration file"""
        self._validate_profile_name(profile_name)
        try:
            config = self._load_config()
        except Exception:
            config = tomlkit.TOMLDocument()
        if "platform" not in config:
            config.add("platform", {})
        updated = False
        if config["platform"].pop(profile_name, None):
            updated = True
        if config.get("default", "") == profile_name:
            config.pop("default", None)
            updated = True
        if updated:
            self._write_config(config)
            LOG.debug("Profile removed: %s", profile_name)
        return updated

    def set_default(
        self,
        profile_name: str,
    ):
        """Set the default profile in the configuration file"""
        self._validate_profile_name(profile_name)
        try:
            config = self._load_config()
        except Exception:
            config = tomlkit.TOMLDocument()
        if not config.get("platform", {}).get(profile_name):
            raise ValueError(
                "The specified profile was not found in the configuration file"
            )
        config["default"] = profile_name
        self._write_config(config)
        LOG.debug("Default profile set to: %s", profile_name)

    def list(self) -> ([str], str | None):
        """Return the names of the configured profiles and the default profile name"""
        try:
            config = self._load_config()
            profiles = list(config.get("platform", tomlkit.TOMLDocument()).keys())
            default = config.get("default")
        except Exception:
            profiles = []
            default = None
        return (profiles, default)

    def platform(self) -> (str, str):
        """Return the selected platform configuration"""
        if not self.url:
            raise Exception("No profile loaded")
        return (self.url, self.token)
