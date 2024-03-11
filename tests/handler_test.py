from click.testing import CliRunner
from fakesnake.handler import *
import json


def test_gen_shape():
    runner = CliRunner()
    result = runner.invoke(shape, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_gen_geojson():
    runner = CliRunner()
    result = runner.invoke(geojson, ["-n", "10"])
    assert result.exit_code == 0
    try:
        json.loads(result.output)
        assert True
    except:
        assert False


def test_gen_name():
    runner = CliRunner()
    result = runner.invoke(name, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_gen_email():
    runner = CliRunner()
    result = runner.invoke(email, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_gen_address():
    runner = CliRunner()
    result = runner.invoke(address, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_gen_password():
    runner = CliRunner()
    result = runner.invoke(password, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_gen_number():
    runner = CliRunner()
    result = runner.invoke(number, ["-n", "10"])
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 10


def test_gen_text():
    runner = CliRunner()
    result = runner.invoke(text, ["-n", "10"])
    assert result.exit_code == 0
    # assert len(result.output.splitlines()) == 10


def test_db_shows():
    runner = CliRunner()
    result = runner.invoke(db_shows)
    assert result.exit_code == 0
    assert len(result.output.splitlines()) > 0


def test_table_show():
    runner = CliRunner()
    result = runner.invoke(table_show, ["users"])
    print(result.output)
    assert result.exit_code == 0


def test_tables_show():
    runner = CliRunner()
    result = runner.invoke(tables_show)
    assert result.exit_code == 0


def test_table_describe():
    runner = CliRunner()
    result = runner.invoke(table_describe, ["users"])
    assert result.exit_code == 0
    print(result.output)
