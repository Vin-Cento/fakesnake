from click.testing import CliRunner
from fakesnake.main import database


def test_regular_table():
    runner = CliRunner()
    result = runner.invoke(database, ["describe", "users"])
    print("")
    print(result.output)
    assert result.output != "Table not found\n"
    assert result.exit_code == 0


def test_missing_table():
    runner = CliRunner()
    result = runner.invoke(database, ["describe", "missing"])
    print("")
    print(result.output)
    assert result.output == "Table not found\n"
    assert result.exit_code == 0


# TODO: Relationship Test
# def test_relationship_table():
#     runner = CliRunner()
#     result = runner.invoke(database, ["describe", "users"])
#     print("")
#     print(result.output.split('Relationship'))
#     assert result.output != "Table not found\n"
#     assert result.exit_code == 0
