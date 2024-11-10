# [![jason logo](https://jason.co.jp/favicon.ico)](https://jason.co.jp/) jason-json

[![PyPI version](
  <https://img.shields.io/pypi/v/jason-json?color=blue>
  )](
  <https://pypi.org/project/jason-json/>
) [![Maintainability](
  <https://api.codeclimate.com/v1/badges/20d58be4ccf5c4c8e008/maintainability>
  )](
    <https://codeclimate.com/github/eggplants/jason-json/maintainability>
) [![Test Coverage](
  <https://api.codeclimate.com/v1/badges/20d58be4ccf5c4c8e008/test_coverage>
  )](
    <https://codeclimate.com/github/eggplants/jason-json/test_coverage>
  ) [![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/jason-json/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/jason-json/master>
)

[![ghcr latest](
    <https://ghcr-badge.egpl.dev/eggplants/jason-json/latest_tag?trim=major&label=latest>
  )](
    <https://github.com/eggplants/jason-json/pkgs/container/jason-json>
) [![ghcr size](
  <https://ghcr-badge.egpl.dev/eggplants/jason-json/size>
  )](
  <https://github.com/eggplants/jason-json/pkgs/container/jason-json>
)

[Jason](https://jason.co.jp) JSON Builder

## Install

```bash
pip install git+https://github.com/eggplants/jason-json
# or...
pip install jason-json
```

## CLI Usage

You can run this program as `jason-json` or `jason.json` on CLI.

```shellsession
$ jason.json -i 2
{
  "東京都": [
    {
      "name": "足立鹿浜店",
      "address": "東京都足立区鹿浜6-34-19",
      "link": "http://jason.co.jp/wptest/?p=5079",
      "business_time": {
        "begin_sec": 36000,
        "end_sec": 79200,
        "duration_sec": 43200,
        "duration_str": "10:00～22:00"
      }
    },
```

[`jason.json`](https://github.com/eggplants/jason-json/blob/master/jason.json) is the result with running `jason.json -O -s jason.json -i 2`.

### Help

```shellsession
$ jason.json -h
usage: jason-json [-i INDENT] [-O] [-s SAVE] [-u URL] [-V] [-h]

Jason (https://jason.co.jp) JSON Builder.

options:
  -i INDENT, --indent INDENT
                         number of indentation spaces in json (default: 2)
  -O, --overwrite        overwrite if save path already exists (default: False)
  -s SAVE, --save SAVE   save json to given path (default: None)
  -u URL, --url URL      target url (default: https://jason.co.jp/network)
  -V, --version          show program's version number and exit (default: False)
  -h, --help             show this help message and exit
```

### from Docker

Try:

```bash
docker run -it ghcr.io/eggplants/jason-json -h
```

## License

MIT
