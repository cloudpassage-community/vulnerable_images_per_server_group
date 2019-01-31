# Vulnerable images per server group

Place a CSV describing vulnerable AMIs per group in Google sheets, where you
can feed it into Data Studio. This tool updates `sheet1`

## Requirements

* Docker engine
* CloudPassage Halo account
* Deployed ServerSecure agents in an AWS environment
* Google apps service account OAuth json, configured as described
[here](https://pygsheets.readthedocs.io/en/stable/authorization.html).

## Running

* Build: `docker build -t vulnimages:latest .`
* Set environment variables:

| Variable            | Purpose                                              |
|---------------------|------------------------------------------------------|
| HALO_API_KEY        | Read-only CloudPassage Halo API key.                 |
| HALO_API_SECRET_KEY | API secret for `HALO_API_KEY`.                       |
| WORKBOOK_ID         | ID for workbook (get this from the URL).             |
| G_SVC_ACCT_JSON     | Base64-encoded auth json for Google service account. |

* Run the container!

```
docker run -it --rm \
    -e HALO_API_KEY=${HALO_API_KEY} \
    -e HALO_API_SECRET_KEY=${HALO_API_SECRET_KEY} \
    -e WORKBOOK_ID=${WORKBOOK_ID} \
    -e G_SVC_ACCT_JSON=${G_SVC_ACCT_JSON} \
    vulnimages:latest
```
