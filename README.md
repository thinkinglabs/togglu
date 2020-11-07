# Togglu

A command-line interface for toggl.com

Still work in progress.

## Run tests

To run the tests:

```bash
make test
```

## List all workspaces

```bash
./bin/togglu workspaces
```

## Get a timesheet

```bash
./bin/togglu timesheet --workspace-id <workspace_id> --since 2019-10-01 --until 2019-10-31
```
