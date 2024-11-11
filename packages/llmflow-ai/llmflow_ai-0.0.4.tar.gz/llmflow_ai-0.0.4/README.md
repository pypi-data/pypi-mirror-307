
Welcome to LLMFlow, a framework for large language model interaction flows.

***


To work on development of LLMFlow, clone the repository and install with the `-e` flag and `[dev]` optional dependencies:

```bash
$ git clone https://github.com/bjelkenhed/flow_ai.git
$ cd flow_ai
$ pip install -e ".[dev]"
```

Optionally install pre-commit hooks via
```bash
make hooks
```

Run linting, formatting, and tests via
```bash
make check
make test
```