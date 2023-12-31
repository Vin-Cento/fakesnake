![FakeSnake_Logo](https://raw.githubusercontent.com/Vin-Cento/fakesnake/master/assets/banner.png)

## Usages

### Generate Fake Data

![generate demo](https://raw.githubusercontent.com/Vin-Cento/fakesnake/master/assets/generate_demo.gif)

```bash
fakes --help
```

    Usage: fakes [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      address
      config
      email
      init
      insert
      name
      number
      password
      shape

### Insert Data to DB

![insert demo](https://raw.githubusercontent.com/Vin-Cento/fakesnake/master/assets/insert_demo.gif)

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
