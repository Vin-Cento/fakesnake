from click.testing import CliRunner
from fakesnake.main import database


def test_insert():
    runner = CliRunner()
    runner.invoke(
        database, ["exec", "create table student (id serial primary key, name text)"]
    )
    result = runner.invoke(database, ["insert", "student"])
    runner.invoke(database, ["exec", "truncate student"])
    print("")
    assert result.exit_code == 0


def test_insert_relationship():
    runner = CliRunner()
    # create student table
    runner.invoke(
        database, ["exec", "create table student (id serial primary key, name text)"]
    )
    # create class table with foreign key to student
    runner.invoke(
        database,
        [
            "exec",
            "create table class (id serial primary key, class text,student_id integer references student(id))",
        ],
    )
    runner.invoke(database, ["insert", "student"])
    runner.invoke(database, ["insert", "class"])
    result = runner.invoke(database, ["describe", "users"])

    runner.invoke(database, ["exec", "truncate student"])
    runner.invoke(database, ["exec", "truncate class"])
    print("")
    print(result.output)
    assert result.output != "Table not found\n"
    assert result.exit_code == 0
