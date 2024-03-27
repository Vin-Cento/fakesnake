from click.testing import CliRunner
from fakesnake.main import database


def test_table_handler():
    runner = CliRunner()
    result = runner.invoke(database, ["table", "users"])
    print("")
    print(result.output)
    assert result.exit_code == 0
