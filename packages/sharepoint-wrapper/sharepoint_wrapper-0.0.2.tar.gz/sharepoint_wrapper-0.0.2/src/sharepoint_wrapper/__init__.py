from dataclasses import dataclass
from io import BytesIO

from sharepoint_wrapper._raw import (
    get_children,
    get_drives,
    get_file,
    get_graph_token,
    get_site,
    write_file,
)
from datetime import datetime, timedelta


@dataclass
class SharePointConfig:
    tenant: str
    tenant_domain: str
    client_id: str
    client_secret: str
    site: str

    _token: str = None
    _token_expiry = None
    _site_id: str = None
    _drive: str = None

    @property
    def token(self):
        now = datetime.now() - timedelta(minutes=5)
        if (
            self._token is not None
            and self._token_expiry is not None
            and now < self._token_expiry
        ):
            return self._token
        self._token, self._token_expiry = get_graph_token(
            self.tenant_domain, self.client_id, self.client_secret
        )
        return self._token

    @property
    def site_id(self):
        if self._site_id is not None:
            return self._site_id
        self._site_id = get_site(self.tenant, self.site, self.token)
        return self._site_id

    @property
    def drive(self):
        if self._drive is not None:
            return self._drive
        all_drives = get_drives(self.site_id, self.token)
        self._drive = all_drives[0][0]

        return self._drive


def get_folders(config: SharePointConfig, path: str | None = None):
    return get_children(config.drive, config.token, path, "folder")


def get_files(config: SharePointConfig, path: str | None = None):
    return get_children(config.drive, config.token, path, "file")


def get_file_content(config: SharePointConfig, file_name: str, path: str | None = None):
    return get_file(config.drive, config.token, file_name, path)


def upload_file(
    config: SharePointConfig,
    file_content: BytesIO,
    file_name: str,
    path: str | None = None,
):
    return write_file(config.drive, config.token, file_content, file_name, path)
