<p align="center">
    <img src="https://github.com/opensourceworks-org/deltalake-tools/blob/main/img/deltalake-tools-lg.png?raw=true" alt="deltalake-tools logo" height="200">
</p>

<p align="center">
  <a href="https://pypi.python.org/pypi/deltalake-tools">
    <img alt="deltalake-tools license" src="https://img.shields.io/pypi/l/deltalake-tools?style=flat-square&color=00ADD4&logo=apache">
  </a>
  <a href="https://github.com/opensourceworks-org/deltalake-tools/actions/workflows/publish.yml">
    <img alt="deltalake-tools pipelines" src="https://github.com/opensourceworks-org/deltalake-tools/actions/workflows/publish.yml/badge.svg">
  </a>
  <a href="https://pypi.python.org/pypi/deltalake-tools">
    <img alt="deltalake-tools pipelines" src="https://img.shields.io/pypi/dm/deltalake-tools?label=Downloads&color=blue&style=flat-square">
  </a>
  <a href="https://pypi.python.org/pypi/deltalake-tools">
    <img alt="deltalake-tools" src="https://img.shields.io/pypi/pyversions/deltalake-tools?style=flat-square&color=00ADD4&logo=python">
  </a>
  <a href='https://deltalake-tools.readthedocs.io/en/latest/?badge=latest'>
      <img src='https://readthedocs.org/projects/deltalake-tools/badge/?version=latest' alt='Documentation Status' />
  </a>
</p>

# Deltalake Tools

## Introduction

A set of easy to use commands for deltalake, with a command line interface.

You probably don't need this, especially if you're already using delta-rs (deltalake). Just like you don't need awscli when you already have a boto3 client.
It's useful as a delta cli ie. as a cron job.

Also working on a Rust implementation, with python bindings using [PYO3/maturin](https://github.com/PyO3/maturin).

#### Delta Table Commands currently supported

- [x] compact
- [x] vacuum
- [x] create-checkpoint
- [x] table-version
- [ ] delete-table
- [ ] create-test-table
- [x] parquet-to-delta <sup>1</sup>
- [ ] ...

<sup>1</sup>: currently limited to inplace and local storage

#### Storage services currently supported

- [x] local storage
- [x] AWS S3 (virtual and path addressing style)
- [x] IBM COS (virtual and path addressing style)
- [ ] Azure blob storage
- [ ] Google cloud storage
- [ ] ...

#### Platforms supported

|         | arm64              | amd64              |
| ------- | ------------------ | ------------------ |
| linux   | <center>x</center> | <center>x</center> |
| mac     | <center>x</center> | <center>x</center> |
| windows |                    |                    |

#### Minimal Python version

3.10

## Getting started

Install

```shell
pip install deltalake-tools
```

**check out [astral's](https://astral.sh/) rye, uv and ruff projects**

(uv is a blazingly fast drop-in replacement for pip.)

```shell
uv install deltalake-tools
```

If you prefer rye:

```shell
rye add deltalake-tools
```

## Usage

help

```shell
$ deltalake-tools -h
Usage: deltalake-tools [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  compact
  create-checkpoint
  table-version
  vacuum
$
```

Consider the following test table:

```
/tmp/test_delta_table
├── 0-ed28f60b-7569-47fc-90fa-9cbaad8ccd27-0.parquet
├── 1-dde22814-9070-4df6-be8c-5ec564c8cfd3-0.parquet
├── 10-eafcb45c-6fdd-467b-b35d-d8bf127ae243-0.parquet
├── 2-7bcb5e5d-d2e6-4975-a2d6-a399413b2883-0.parquet
├── 3-7412d097-1b4c-4d45-9ac1-7bc312f20f62-0.parquet
├── 4-9a5bd960-08fb-4b8f-8e94-8f81574799e5-0.parquet
├── 5-a2182ca3-c334-43be-8935-210fc839ff77-0.parquet
├── 6-f9f4597c-9709-4029-a0ee-a11d757072bf-0.parquet
├── 7-a3c8fbef-27eb-4ee1-ae2a-2a30c9964fbc-0.parquet
├── 8-8221beb7-9a14-4ce5-a205-c5b862cbce0d-0.parquet
├── 9-63ec9854-d58c-4d48-b3cf-9c18c43e2d17-0.parquet
└── _delta_log
    ├── 00000000000000000000.json
    ├── 00000000000000000001.json
    ├── 00000000000000000002.json
    ├── 00000000000000000003.json
    ├── 00000000000000000004.json
    ├── 00000000000000000005.json
    ├── 00000000000000000006.json
    ├── 00000000000000000007.json
    ├── 00000000000000000008.json
    ├── 00000000000000000009.json
    └── 00000000000000000010.json
```

table-version

```shell
$ deltalake-tools table-version /tmp/test_delta_table
10
```

compact

- increments version
- rewrites the date into 1 file. Here, 11 files are replaced by 1. This has a considerable beneficial effect on read performance.

```shell
$ deltalake-tools table-version /tmp/test_delta_table
10
$ deltalake-tools compact /tmp/test_delta_table
{'numFilesAdded': 1, 'numFilesRemoved': 11, 'filesAdded': '{"avg":1034.0,"max":1034,"min":1034,"totalFiles":1,"totalSize":1034}', 'filesRemoved': '{"avg":909.3636363636364,"max":913,"min":873,"totalFiles":11,"totalSize":10003}', 'partitionsOptimized': 1, 'numBatches': 11, 'totalConsideredFiles': 11, 'totalFilesSkipped': 0, 'preserveInsertionOrder': True}
$ deltalake-tools table-version /tmp/test_delta_table
11
```

vacuum

- increments version
- by default, the minimal retention hours is 168. This can be overridden, but read the [docs](https://docs.delta.io/0.4.0/delta-utility.html) first.

arguments:

- --retention-hours: how long do you want to keep, for time travelling. Default: 168 (1 week)
- --disable-retention-duration: disable the safety check
- --force: by default, this is a dry-run operation. Use this to actually perform the vacuum command.

These safety features are implemented intentionally. Read the [docs](https://docs.delta.io/0.4.0/delta-utility.html) for more information.

```shell
$ deltalake-tools table-version /tmp/test_delta_table
11
$deltalake-tools vacuum /tmp/test_delta_table --retention-hours 0 --disable-retention-duration --force
['3-7412d097-1b4c-4d45-9ac1-7bc312f20f62-0.parquet', '6-f9f4597c-9709-4029-a0ee-a11d757072bf-0.parquet', '5-a2182ca3-c334-43be-8935-210fc839ff77-0.parquet', '2-7bcb5e5d-d2e6-4975-a2d6-a399413b2883-0.parquet', '1-dde22814-9070-4df6-be8c-5ec564c8cfd3-0.parquet', '8-8221beb7-9a14-4ce5-a205-c5b862cbce0d-0.parquet', '9-63ec9854-d58c-4d48-b3cf-9c18c43e2d17-0.parquet', '7-a3c8fbef-27eb-4ee1-ae2a-2a30c9964fbc-0.parquet', '0-ed28f60b-7569-47fc-90fa-9cbaad8ccd27-0.parquet', '10-eafcb45c-6fdd-467b-b35d-d8bf127ae243-0.parquet', '4-9a5bd960-08fb-4b8f-8e94-8f81574799e5-0.parquet']
$ deltalake-tools table-version /tmp/test_delta_table
12
```

create-checkpoint

- does not increment version
- use this if your deltalake clients require this \_last_checkpoint file, as it is not written by default. Not by spark, not by delta-rs.

```shell
$ deltalake-tools table-version /tmp/test_delta_table
13
$ deltalake-tools create-checkpoint /tmp/test_delta_table
Checkpoint created successfully.
$ deltalake-tools table-version /tmp/test_delta_table
13
```

## Contribute

### Test

- pytest
- moto[server]: needs to be started before initializing any clients (boto3, delta)

Running tests:

```shell
rye run pytest tests
```

### management

- [rye](https://rye.astral.sh/)
- make

### changelog

- [git-cliff](https://git-cliff.org/)
