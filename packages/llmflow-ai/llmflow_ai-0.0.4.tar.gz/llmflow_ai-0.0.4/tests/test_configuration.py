from pathlib import Path

from llmflow_ai.configuration.enrichment import read_configuration

TEST_CONFIG_DIR_PATH = Path("tests/test_config_dir")


def test_read_configuration():
    config_file = (TEST_CONFIG_DIR_PATH / "config.yaml").as_posix()
    yaml_config = read_configuration(config_file)
    assert len(yaml_config["datasets"]) == 1
    assert len(yaml_config["enrichments"]) == 2
