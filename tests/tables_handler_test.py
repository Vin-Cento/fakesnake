from click.testing import CliRunner
from fakesnake.main import database


def test_tables_handler():
    runner = CliRunner()
    result = runner.invoke(database, ["tables"])
    print("")
    print(result.output)
    assert result.exit_code == 0
