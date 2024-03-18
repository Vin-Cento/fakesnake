![FakeSnake_Logo](https://raw.githubusercontent.com/Vin-Cento/fakesnake/master/assets/banner.png)

## Usages

```bash
fakes --help
```

    Usage: fakes [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      db   subcommand for database interaction
      gen  subcommand for generating data

### Generate Fake Data

![generate demo](https://raw.githubusercontent.com/Vin-Cento/fakesnake/development/assets/fakesnake_gen_demo.gif)

```bash
fakes gen --help
```

    Usage: fakes gen [OPTIONS] COMMAND [ARGS]...

      subcommand for generating data

    Options:
      --help  Show this message and exit.

    Commands:
      address   generate a list of address
      email     generate a list of email
      geojson   generate a list of geojson
      name      generate a list of name
      number    generate a list of number
      password  generate a list of password
      shape     generate a list of shape
      text      generate a list of text

### Insert Fake Data to Database

##### (\*postgres only... other databases coming soon)

![insert demo](https://raw.githubusercontent.com/Vin-Cento/fakesnake/development/assets/fakesnake_db_demo.gif)

```bash
fakes db --help
```

    Usage: fakes db [OPTIONS] COMMAND [ARGS]...

      subcommand for database interaction

    Options:
      --help  Show this message and exit.

    Commands:
      config    show the database config
      describe  describe the current database
      exec      execute a sql command
      insert    insert random data into table
      table     show all columns the table
      tables    show all tables the database

## Install

```bash
pip install fakesnake
```

## Postgres

Need to have the psycopg2-binary to connect to POSTGRES server. To install it, you need install postgres-client and postgres-dev.

```bash
# alpine
apk add postgres-client postgres-dev

# ubuntu
apt install postgres-client postgres-dev
```

```bash
pip install psycopg2-binary
```

## FAQ

1.  Q: Where to report problems?

    A: Open up an [issue](https://github.com/Vin-Cento/fakesnake/issues/new)
