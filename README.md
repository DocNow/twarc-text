# twarc-text

This module extends [twarc] to allow you to print out tweets as text for easy
testing on the command line. It's really just a gimmick. Send a PR to make it
better!

![twarc-text](./images/screencap.gif)

## Install

    pip install twarc-text

## Use

If you've got a file of tweets that you've previously collected you can print
them out:

    twarc2 text tweets.jsonl

Also you can pipe directly, for example displaying the sample stream:

    twarc2 sample | twarc2 text

[twarc]: https://github.com/docnow/twarc
