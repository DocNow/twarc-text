from twarc_text import text, _textwrap, _border
from click.testing import CliRunner

runner = CliRunner()

def test_text():
    # just make sure it doesn't blow up
    result = runner.invoke(text, ['test-data/noflat.jsonl'])
    assert result.exit_code == 0

def test_textwrap():
    assert _textwrap('the quick brown fox jumps over the lazy dog', 10) == ['the quick ', 'brown fox ', 'jumps over', ' the lazy ', 'dog']

def test_border():
    assert _border('food', 20) == '┃ food             ┃'
