# MPR-sharepoint-utils

[![Deploy](https://github.com/mathematica-org/MPR-sharepoint-utils/actions/workflows/pypi-deploy.yml/badge.svg)](https://github.com/mathematica-org/MPR-sharepoint-utils/actions/workflows/pypi-deploy.yml)

## Installing the package

There are different ways to install the package because different features require different package imports. Rather than being forced to install a dependency for a part of this code you won't actually use, you can select which version to use. There are currently 3 versions available:
- standard
- [pandas]
- [openpyxl]

You can specify which you'd like to use by adding the version to the import statement, like:
```bash
pipenv install mpr-sharepoint-utils[pandas]
```

If you'd like to use multiple "extras", you can specify both versions separated by commas, like;
```bash
pipenv install mpr-sharepoint-utils[pandas, openpyxl]
```


## Using the package:

First, you must establish a `SharePointConnection`, which takes the following arguments:

- `client_id`, the ID portion of your user (or service) account credentials
- `client_secret`, the secret string of your user (or service) credentials
- `site_id`, the ID of the SharePoint site you wish to access
- `tenant`, the name of your organization (you can find this in a SharePoint URL, like "tenant.sharepoint.com")

Once you've established a connection, you can pass that to any of the utility functions to perform operations in SharePoint.

### Example usage

```python
from sharepoint_utils import SharePointConnection, get_txt

sharepoint_ctx = SharePointConnection(
  client_id="<YOUR CLIENT ID>",
  client_secret="<YOUR CLIENT SECRET>",
  site_id="<YOUR SITE ID>",
  tenant="<YOUR TENANT>"
)

txt_str = get_txt(
  sharepoint_ctx,
  drive="Documents",
  file_path="path/to/file"
)
```

In order to reduce unnecessary bloat, utility functions that depend on large packages such as `pandas` live in separate modules. These packages are _not_ dependencies of `mpr-sharepoint-utils` and therefore need to be installed directly into your project.

### Example usage

```python
from sharepoint_utils import SharePointConnection
from sharepoint_utils.spreadsheet_utils import get_csv_as_df

sharepoint_ctx = SharePointConnection(
  client_id="<YOUR CLIENT ID>",
  client_secret="<YOUR CLIENT SECRET>",
  site_id="<YOUR SITE ID>",
  tenant="<YOUR TENANT>"
)

df = get_csv_as_df(
  sharepoint_ctx,
  drive="Documents",
  file_path="path/to/file"
)
```

## FAQs

**Q:** How do
I know what my site ID is?

**A:** First, get your access token with the first command below; then, plug that into the second command below to get your site ID.

Get access token (can use to get site id given hostname and path (site/subsite)):

```
curl --location --request POST 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=INSERT_CLIENT_ID' \
--data-urlencode 'scope=https://graph.microsoft.com/.default' \
--data-urlencode 'client_secret=INSERT_CLIENT_SECRET' \
--data-urlencode 'grant_type=INSERT_CLIENT_CREDENTIALS'
```

Get site ID

```
curl --location --request GET 'https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{path}?$select=id' \
--header 'Authorization: Bearer access_token' \
--data
```

## Development

### Beta Releases
In lieu of classic testing, beta releases on [test pypi](https://test.pypi.org/) allow you to confirm that newly PR'd code works as expected. In order to initiate a beta release of the package based on a new PR, you can follow these steps:
1. Open a PR in the Github repo with new changes
2. Comment on the PR: making a new comment like "beta-release-bot: {/d+}" where '{/d+}' is replaced by any number of digits will initiaite a Github action workflow that pushes the code in the PR. The digits in your comment (which may reflect a Jira ticket number) will be appended to the version number in your PR's pytproject.toml file as a label for the test pypi release.
3. To test your changes in an existing repo that already uses the sharepoint utils package, download and use your new beta release by adding this to your Pipfile:
```
[[source]]
url = "https://test.pypi.org/simple"
verify_ssl = true
name = "testpypi"
```
and then run `pipenv install mpr-sharepoint-utils=={branched version number}.dev{\d+} --index testpypi` where {/d+} matches the digits in your comment from step 2.

### Setup

This repo follows the [Angular format](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines) for commit messages.
We use a pre-commit hook and commitlint to enforce this format.  When first downloading the repo, please run this command:
`pipenv run pre-commit install --hook-type commit-msg` to set up the pre-commit hook. This hook will then check the message for each commit
and reject commits that don't follow the correct format.

## Maintainers

- Claire McShane
- Holden Huntzinger
- Tess Martinez
- Max Grody
