import re
import json
import maya
import click

from wcwidth import wcswidth
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
                fg='yellow'
            ),
            width
        )
    )

    # blank line
    body.append(_border('', width))

    # add the text of the tweet
    tweet_text = tweet['text']
    body.extend(
        map(
            lambda s: _border(s, width), 
            _textwrap(
                tweet_text,
                width=width - 4
            )
        )
    )

    # blank line
    body.append(_border('', width))

    # the date
    created = str(maya.parse(tweet['created_at']))
    m = tweet['public_metrics']
    metrics = f'♡ {m["like_count"]}  ♺ {m["retweet_count"]}  ↶ {m["reply_count"]}  « {m["quote_count"]}'

    padding = (width - 4 - wcswidth(created + metrics)) * ' '

    body.append(
        _border(
            click.style(
                created + 
                padding + 
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
    margin = (width - wcswidth(text_no_colors) - 4) * ' '
    return f'┃ {text}{margin} ┃'

def _textwrap(s, width):
    # would be nice to use textwrap module here but we need to factor in
    # the actual terminal display of unicode characters when splitting
    if '\n' in s:
        parts = s.split('\n', 1)
        return _textwrap(parts[0], width) + [''] + _textwrap(parts[1], width)

    words = re.split(r'(\s+)', s)
    lines = []
    line = ''
    while len(words) > 0:
        word = words.pop(0)
        if wcswidth(line) + wcswidth(word) > width:
            lines.append(line)
            line = word
        elif line == '':
            line = word
        else:
            line += word

    if line != '':
        lines.append(line)

    return lines

