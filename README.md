# Togglu

A command-line interface for toggl.com

Still work in progress.

License: still to be defined.

## Run tests

To run the tests, [mountepy](https://pypi.org/project/mountepy/) requires 
Mountebank.

```bash
npm install -g mountebank --production
```

To run the tests:

```bash
python -m unittest discover
```

## List all workspaces

```bash
python -m togglu.togglu workspaces
```

## Get a timesheet

```bash
python -m togglu.togglu timesheet --workspace-id <workspace_id> --since 2019-10-01 --until 2019-10-31
```

