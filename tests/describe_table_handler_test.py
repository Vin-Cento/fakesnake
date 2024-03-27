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


def test_relationship_table():
    runner = CliRunner()
    runner.invoke(database, ["exec", "create table student (id serial primary key, name text)"])
    runner.invoke(
        database,
        [
            "exec",
            "create table class (id serial primary key, class text,student_id integer references student(id))",
        ],
    )
    runner.invoke(database, ["insert", "student"])
    runner.invoke(database, ["insert", "class"])
    result = runner.invoke(database, ["describe", "student"])
    result2 = runner.invoke(database, ["describe", "class"])
    print("")
    print(result.output)
    print(result2.output)
    assert result.exit_code == 0
    assert result2.exit_code == 0
