from click.testing import CliRunner
from fakesnake.handler import *
import json


def test_shape_handler():
    runner = CliRunner()
    result = runner.invoke(shape_handler, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_geojson_handler():
    runner = CliRunner()
    result = runner.invoke(geojson_handler, ["-n", "10"])
    assert result.exit_code == 0
    try:
        json.loads(result.output)
        assert True
    except:
        assert False


def test_name_handler():
    runner = CliRunner()
    result = runner.invoke(name_handler, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_email_handler():
    runner = CliRunner()
    result = runner.invoke(email_handler, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_address_handler():
    runner = CliRunner()
    result = runner.invoke(address_handler, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_password_handler():
    runner = CliRunner()
    result = runner.invoke(password_handler, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_number_handler():
    runner = CliRunner()
    result = runner.invoke(number_handler, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_text_handler():
    runner = CliRunner()
    result = runner.invoke(text_handler, ["-n", "10"])
    assert result.exit_code == 0


def test_db_shows_handler():
    runner = CliRunner()
    result = runner.invoke(db_shows)
    assert result.exit_code == 0
    assert len(result.output.splitlines()) > 0


def test_show_table_handler():
    runner = CliRunner()
    result = runner.invoke(show_table_handler, ["users"])
    print(result.output)
    assert result.exit_code == 0


def test_show_tables_handler():
    runner = CliRunner()
    result = runner.invoke(show_tables_handler)
    assert result.exit_code == 0


def test_describe_table():
    runner = CliRunner()
    result = runner.invoke(describe_table_handler, ["users"])
    assert result.exit_code == 0
    print(result.output)
