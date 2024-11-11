from enum import StrEnum
from pathlib import Path
from json import loads

from importlib.resources import files
# creates dependency on python 3.10, can use importlib_resources backport instead if needed
# https://setuptools.pypa.io/en/latest/userguide/datafiles.html

from semver import Version

import forgeschema


class SpecCatalog:
    def __init__(self):
        self.data_path = files("tclivalidator.data").joinpath("spec")

    def _get_subdir_names(self, subdirs : list) -> list:
        path = self.data_path
        for subdir in subdirs:
            path = path.joinpath(subdir)
        retval = []
        for thing in path.iterdir():
            if not thing.is_dir():
                continue
            if thing.name.startswith("__"):
                continue
            p = Path(thing)
            retval.append(p.name)
        return retval

    def specs(self) -> list:
        return sorted(self._get_subdir_names([]))
    
    def versions(self, spec: str) -> list:
        vpaths = self._get_subdir_names([spec])
        versions = [Version.parse(s) for s in vpaths]
        versions = sorted(versions)
        return  [str(v) for v in versions]
    
    def encodings(self, spec, version: str) -> list:
        return sorted(self._get_subdir_names([spec, version]))

    def load_config(self, spec: str, version: str, encoding: str):
        data_path = self.data_path.joinpath(spec).joinpath(version).joinpath(encoding)
        config = data_path.joinpath("config.json")
        config_json = loads(config.read_text())
        config_json["coreSchema"] = Path(data_path.joinpath(config_json["coreSchema"]))
        config_json["supportingSchemas"] = [Path(data_path.joinpath(p)) for p in config_json["supportingSchemas"]]
        return config_json
    
    def schema_for(self, spec: str, version: str, encoding: str, additional_schemas = None):
        config = self.load_config(spec, version, encoding)
        if additional_schemas:
            for add_schema in additional_schemas:
                config["supportingSchemas"].append(add_schema)
        if encoding == "xsd":
            schema = forgeschema.XSDSchema(config["coreSchema"], config["supportingSchemas"])
        elif encoding == "json":
            schema = forgeschema.JSONSchema(config["coreSchema"], config["supportingSchemas"])
        schema.build()
        if not schema.built_ok:
            print(schema.build_errors)
            raise Exception(f"Could not build {encoding} schema for {spec} v{version}")
        return schema