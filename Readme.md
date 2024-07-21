# Document-service Installation guide

#### Apt update
```sh
apt install python3-pip

sudo apt install libreoffice
libreoffice --version
```

#### Generating new sentence DB
1. Copy original sentence db to `_db.yaml`
2. Run `python tool_generate_sdb.py` to generate AI refactored sentences
3. Manually refactor _sdb_chunks/chunk{i}.txt files to have normalized format
4. Run `python tool_sdb_yaml.py` to generate yaml file. It's saved in `_db_new.yaml`
6. Run check using `python tool_sdb_check.py`.
7. Copy the content of `_db_new.yaml` to appropriate db file in `assets/sentences/**.yaml` file.