# Contextal Python Package

This package provides a simple way to interact with Contextal Platform via API. It includes a Python library and command-line tools to perform essential tasks such as file uploads, scenario management, and retrieval of analysis results.

## Installation
```
pip install contextal
```

## Usage

### Library example
Here's an example of how to use the library to upload a file and obtain the results from scenarios (if any):
```python
from contextal import Config, Platform
from time import sleep

config = Config()
config.url = "http://contextal.my_company.lan"
#config.token = "my_token"
platform = Platform(config)
file = open("my_sample", "rb")
work = platform.submit_work(file)
sleep(1)
actions = platform.get_actions(work["work_id"])
print(actions)
```

### Command line examples
```bash
# create default profile
ctx config create local_cloud http://contextal.my_company.lan --set-default
# create additional profile
ctx config create public_cloud https://contextal.my_company.com --token glpat-my-token
# upload file
ctx work submit my_sample --profile public_cloud
#upload file using default profile
ctx work submit my_sample
# check work results
ctx work graph MY_WORK_ID --pretty
# check scenarios results (i.e. the recommended actions) for a work
ctx work actions MY_WORK_ID --pretty
```
Add a new scenario:
```bash
ctx scenario add "-"<<EOF
{
    "action": "BLOCK",
    "creator": "me@my_company.com",
    "context": null,
    "description": "Block all mails containing windows link files",
    "local_query": "object_type=\"LNK\" && @has_root(object_type == \"Email\")",
    "max_ver": null,
    "min_ver": 1,
    "name": "MAIL_WITH_LNK"
}
EOF
# call the reload option to make Contextal Platform start using any new scenarios
ctx scenario reload
```
Scenarios can be downloaded and used as a backup or template for new ones:
```bash
ctx scenario details SCENARIO_ID > scenario1.backup
# modify scenario using jq command
cat scenario1.backup | jq '.name="MAIL_WITH_PE"|.local_query="object_type=\"PE\" && @has_root(object_type == \"Email\")"' > scenario2
# add scenario2
ctx scenario add scenario2
# call the reload option to make Contextal Platform start using any new scenarios
ctx scenario reload

```

## License
This package is distributed under the MIT License. See the LICENSE.txt file for more details.
