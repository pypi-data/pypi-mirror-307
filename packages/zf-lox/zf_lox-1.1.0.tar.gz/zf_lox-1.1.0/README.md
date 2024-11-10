# Lox

[![PyPI version](https://badge.fury.io/py/zf-lox.svg)](https://badge.fury.io/py/zf-lox)

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/lox-logo128.png" alt="Perse"/>
</p>

Lox is a tool for generating leads from LinkedIn. It can open linkedin pages, parse content and extract email.
It integrates with Notion and capable of saving the extracted leads into a Notion database.

### Usage

```bash
lox --url {linkedin-post-url}
```

### Features

It's core features includes:

- Ability to scrape data from LinkedIn posts or feed
- Automatic creation of data model from Notion datbase
- Integration with Notion to save the extracted data

You can install Perse using pip:

```bash
pip install zf-lox

mkdir -p ~/.lox
```

Create a `config` file with the following:

```bash
[linkedin]
email = {your-linkedin-email}
password = {your-linkedin-password}

[openai]
api_key = {your-openai-api-key}

[notion]
api_key = {your-notion-api-key}
database_id = {your-notion-database-id}
```

Export cookies from LinkedIn using [EditThisCookies](https://chromewebstore.google.com/detail/editthiscookies/hlgpnddmgbhkmilmcnejaibhmoiljhhb) and save it in `~/.lox/cookies.json`

## License

[MIT License](./LICENSE)

