# Sharepoint Wrapper

## Create Cofiguration

```python
from sharepoint_wrapper import SharePointConfig

config = SharePointConfig(
    tenant="<tenant>",
    tenant_domain="<tenant_domain>",
    client_id="<client_id>",
    client_secret="<client_secret>",
    site="<site_name>",
)
```

## Get Folders

```python
from sharepoint_wrapper import get_folders

folders_at_root = get_folders(config)
# or 
# ensure your path starts with a slash "/"
folders_at_path = get_folders(config, "/my/path") 
```

## Get Files

```python
from sharepoint_wrapper import get_files

files_at_root = get_files(config)
# or 
# ensure your path starts with a slash "/"
files_at_path = get_files(config, "/my/path") 
```

## Get File Content

```python
from sharepoint_wrapper import get_file_content
from io import BytesIO

file_name = "my_file.pdf"

# returns a BytesIO file

file_at_root: BytesIO = get_file_content(config, file_name)
# or 
# ensure your path starts with a slash "/"
file_at_path: BytesIO = get_file_content(config, file_name, "/my/path") 
```

## Upload a file

:warning: **Note**: Upload response will only be returned in case of success if upload fails, an exception will be raised

```python
from sharepoint_wrapper import upload_file
from io import BytesIO

with open('path/to/your/file', 'rb') as file:
    file_content = file.read()

# Note: Upload response will only be returned in case of success
# if upload fails, an exception will be raised

upload_response: dict = upload_file(config, file_content, "file_name.txt")
# or 
# ensure your path starts with a slash "/"
upload_response: dict = upload_file(config, file_content, "file_name.txt", "/my/path") 
```
