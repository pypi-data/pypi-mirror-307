# MeerkatIO Python Package

[![Downloads](https://static.pepy.tech/badge/meerkatio)](https://pepy.tech/project/meerkatio)

## Introduction

[MeerkatIO](https://www.meerkatio.com/) is the personal notification platform for software engineers and data scientists that allows you to use the notification channels that fit your workflow. This one package immediately opens the door to any notification method you need to save time in your day, integrating with all of the built in tools already at your fingertips.

Get started with just 2 lines of code!

## Available Notification Channels

The MeerkatIO Python package supports the following notification channels:
- Ping
- System
- Slack Direct Message
- Microsoft Teams
- Google Chat
- SMS
- Email

## Installation

```bash
$ pip3 install meerkatio
```

## Authenticating
No account or authentication is required to use the Ping or System notifications, and all other communication channels can be easily enabled with a [MeerkatIO Account](http://meerkatio.com/register) or through the MeerkatIO Command Line Interface tool.

### CLI Account Registration
This package provides a convenient way to get up and running. The `register` command will prompt you for a username and password to start your free account, and on success your environment will be set up for you so you can skip the Authentication Token Setup steps.

```bash
$ meerkat register
```

### Authentication Token Setup
Using your username and password from [MeerkatIO](https://meerkatio.com):

```bash
$ meerkat login
```

Or manually set the MeerkatIO token with one of the following examples:

```bash
# Option 1: Environmental Variable
$ export MEERKAT_TOKEN=token

# Option 2: Cache File
$ echo "token" > ~/.meerkat
```

## Code Examples

```python
import meerkat

# Ping when script gets to checkpoint
meerkat.ping()

# Send a confirmation a function has run
output = build_model()
meerkat.email(output)

# Send Slack message to document model performance
perf = get_model_performance(output)
meerkat.slack(perf)

# Send SMS message when the script is finished
meerkat.sms("Script completed!")
```

### Jupyter Notebook Example

```python
import meerkat

# Ping when cell hits a debug checkpoint
%ping

# Send a confirmation that a cell has run
output = build_model()
%email output

# Send Slack message to document model performance
perf = get_model_performance(output)
%slack perf

# Send SMS message when the cell reaches the end
%sms "Cell completed!"
```

![MeerkatIO Jupyter Notebook personal notification example alerting options](docs/jupyter_example.png)

## MeerkatIO CLI Tool
Access all of the same communication methods from your command prompt to integrate with any workflow.

```bash
$ meerkat ping
$ meerkat email "Bash script output: $1"
$ meerkat sms "Firmware build completed."
$ meerkat slack "Bash script complete"
```

Here is an example of how to use Meerkat with any script running from a terminal in order to ping youself when the script is finished running.

```bash
$ make build && meerkat email "Build succeeded" || meerkat sms "Build failed"
```