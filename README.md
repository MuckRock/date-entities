# date-entities

This add-on looks through documents for dates, then creates entities and entity occurrences for them.

## Installation

- Clone this repo.
- `python3.9 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt` 

## Running it locally

As of 2023-05-12, the `/api/entities` endpoint isn't in production DocumentCloud. Until it lands, you can run it locally by using the [new-entities-mjk branch](https://github.com/MuckRock/documentcloud/blob/new-entities-mjk/config/urls.py).

Once that's running locally, along with [Squarelet](https://github.com/muckrock/squarelet), you need to:

- In the `documentcloud` pip package (if you set up venv as above, it will be at `venv/lib/site-packages`), edit the file `toolbox.py`. In `requests_retry_session`, right below the line `session = session or requests.Session()`, add the line `session.verify = False`.
  - Here's why we need to do this:
    - Before any of our add-on code runs, because we inherit from `AddOn`, the documentcloud client initializes.
    - When it initializes, it tries to get an access token from squarelet.
    - The local dev version of squarelet uses a self-signed cert.
    - `requests` cannot verify those when it makes http requests. (Seemingly, it can't do it even if you tell it where the cert and key are.)
    - Thus, the add-on run will fail right away.
    - We can prevent this by telling the requests session to not do SSL verification before it makes any http calls. That's what the inserted line is.
      - (Do not do this in any production versions of the add-on.)
- Upload some documents with dates in them to your local documentcloud.
- In the terminal:
  - `export DCUSER=<Your local squarelet username, not your prod username>`
  - `export DCPASS=<Your local squarelet password, not your prod username>`
  - Run `make try`, which will pass those environment variable values to main.py/the documentcloud client.

## Known issues

- Occurrences seem to correctly refer to an entity, but `offset` and `content` values are lost.
- Pages, rather than full text, should probably be used in occurrences to say where the entities are in the document.
