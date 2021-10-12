import re
import json
import maya
import click
import textwrap

from wcwidth import wcswidth
from emoji import emoji_count
from twarc import ensure_flattened

@click.command('text')
@click.option('--width', 'width', default=75)
@click.argument('infile', type=click.File('r'), default='-')
@click.argument('outfile', type=click.File('w'), default='-')
def text(infile, outfile, width):
    """
    Print out tweets as text for debugging & data spelunking.
    """
    for line in infile:

        # ignore blank lines
        line = line.strip()
        if line == "":
            continue

        # get a list of tweets, whether flatened or not
        for tweet in ensure_flattened(json.loads(line)):
            print(_text(tweet, width))

def _text(tweet, width):

    # the top line
    body = ['┏' + '━' * (width - 2) + '┓']

    # add author
    body.append(
        _border(
            click.style(
                '@' + tweet['author']['username'] + 
                ' - ' + 
                tweet['author']['name'], 
                fg='green'
            ),
            width
        )
    )

    # blank line
    body.append(_border('', width))

    # add the text of the tweet
    tweet_text = tweet['text']
    extra_width = wcswidth(tweet_text) - len(tweet_text)
    body.extend(
        map(
            lambda s: _border(s, width), 
            textwrap.wrap(
                tweet_text,
                width=width - 4
            )
        )
    )

    # blank line
    body.append(_border('', width))

    # the date
    created = maya.parse(tweet['created_at'])
    m = tweet['public_metrics']
    metrics = f'  ♡ {m["like_count"]}  ♺ {m["retweet_count"]}  ↶ {m["reply_count"]}  "" {m["quote_count"]}'
    body.append(
        _border(
            click.style(
                str(created) + 
                ' ' +  
                metrics,
                fg='green'
            ),
            width
        )
    )

    # the bottom line
    body.append('┗' + '━' * (width - 2) + '┛')
    return '\n'.join(body)

def _border(text, width):
    text_no_colors = click.unstyle(text)
    margin = (width - len(text_no_colors) - 4 - emoji_count(text_no_colors)) * ' '
    return f'┃ {text}{margin} ┃'
