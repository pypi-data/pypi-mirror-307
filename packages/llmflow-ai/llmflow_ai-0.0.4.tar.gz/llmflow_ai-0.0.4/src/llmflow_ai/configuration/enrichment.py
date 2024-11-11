import imp
import json
import logging

import yaml

# from .dataset_utils import get_dataset
# from .evallog_utils import get_dataset_from_eval_log

logger = logging.getLogger(__name__)


class Enrichment:
    """
    Config of enrichments and datasets.

    The enrichment class is used to hold data about a particular enrichment such as the name, template and dataset used.
    """

    def __init__(self, name, config) -> None:
        self.enrichment_config = self.get_enrichment_config(name, config)
        self.name = self.enrichment_config["name"]
        self.index_pattern = self.enrichment_config["dataset_config"]["index_pattern"]
        self.template = self.get_param("template")
        self.selected_phone = self.get_param("selected_phone")
        self.group_by = self.get_param("group_by")
        self.filter_by_element = self.get_param("filter_by_element")
        self.filter_values = self.get_param("filter_values")
        self.dataset_config = self.get_param("dataset_config")
        self.ref_enrichment = self.get_param("ref_enrichment")
        self.schema_path = self.get_param("schema_path")
        self.persist = self.get_param("persist")

    """
    def get_dataset(self):
        if self.dataset_config:
            return get_dataset(self.dataset_config)
        if self.ref_enrichment:
            return get_dataset_from_eval_log(self.ref_enrichment, self.group_by, self.filter_by_element, self.filter_values)
    """

    def get_schema_pydantic_object(self):
        if self.schema_path is None:
            return None
        mod_name, class_name = self.schema_path.split(".")
        file_path = mod_name + ".py"
        print(mod_name, file_path, class_name)

        py_mod = imp.load_source(mod_name, file_path)
        if hasattr(py_mod, class_name):
            pydantic_object = getattr(py_mod, class_name)
        return pydantic_object

    def get_param(self, param_name: str) -> str:
        return (
            self.enrichment_config[param_name]
            if param_name in self.enrichment_config
            else None
        )

    def get_enrichment_config(self, name: str, config: dict):
        for enrichment in config["enrichments"]:
            enrichment_name = list(enrichment.keys())[0]
            if enrichment_name == name:
                enrichment_config = enrichment[enrichment_name]
                enrichment_config["name"] = enrichment_name

                if "dataset" in enrichment[enrichment_name]:
                    dataset_name = enrichment[enrichment_name]["dataset"]
                    enrichment_config["dataset_config"] = self.get_dataset_config(
                        dataset_name, config
                    )

                # Enrichment refers to another enrichment as input
                if "enrichment" in enrichment[enrichment_name]:
                    ref_enrichment_name = enrichment[enrichment_name]["enrichment"]
                    enrichment_config["ref_enrichment"] = ref_enrichment_name
                return enrichment_config

    def get_dataset_config(self, name, config):
        for dataset in config["datasets"]:
            dataset_name = list(dataset.keys())[0]
            if dataset_name == name:
                dataset_config = dataset[dataset_name]
                return dataset_config

    def __str__(self):
        return json.dumps(self.enrichment_config, indent=2, default=str)


def read_configuration(path: str) -> dict:
    with open(path, encoding="utf-8") as file:
        config = yaml.safe_load(file)
        return config


def get_enrichment_list(config_file: str) -> list[Enrichment]:
    # logger.debug(f'open configuration file: {config_file}')
    config = read_configuration(path=config_file)
    # logger.debug(json.dumps(config, indent=2, default=str))
    return list_enrichments(config)


def list_enrichments(config: dict) -> list[Enrichment]:
    enrichment_list = []
    for enrichment_name in list_enrichment_names(config):
        enrichment_list.append(Enrichment(enrichment_name, config))
    return enrichment_list


def list_enrichment_names(config) -> list[str]:
    enrichment_names = []
    for enrichment in config["enrichments"]:
        enrichment_name = list(enrichment.keys())[0]
        enrichment_names.append(enrichment_name)
    return enrichment_names
