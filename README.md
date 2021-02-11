# sars-cov-2-typing

## Usage

> will list all files related to covid-wgs for specified bucket

```python
./hcp_covid.py -ep <endpoint-url> -aki <aws_access_key_id> -sak <aws_secret_access_key> -b orebro --listfiles
```

> upload one file

```python
./hcp_covid.py -ep <endpoint-url> -aki <aws_access_key_id> -sak <aws_secret_access_key> -b <bucketname> -f <single-file>
```

> upload files by giving path to directory (files containing "R2")

```python
./hcp_covid.py -ep <endpoint-url> -aki <aws_access_key_id> -sak <aws_secret_access_key> -b <bucketname> -p "path/to/files*R2*"
```

> downloading a single file

```python
./hcp_covid.py -ep <endpoint-url> -aki <aws_access_key_id> -sak <aws_secret_access_key> -b <bucketname> -f <filename on HCP> -o <path/to/outputdir> --download
```

> search for files in bucket (will print)

```python
./hcp_covid.py -ep <endpoint-url> -aki <aws_access_key_id> -sak <aws_secret_access_key> -b <bucketname> -q <query> 
```

> downloading several files by using query function

```python
./hcp_covid.py -ep <endpoint-url> -aki <aws_access_key_id> -sak <aws_secret_access_key> -b <bucketname> -q <query> -o <path/to/outputdir> --download
```
