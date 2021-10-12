from twarc_text import text 
from click.testing import CliRunner

runner = CliRunner()

def test_text():
    # let's just make sure it doesn't blow up ok?
    result = runner.invoke(text, ['test-data/noflat.jsonl'])
    assert result.exit_code == 0
