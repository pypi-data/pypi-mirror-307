
import logging
from typing import Optional, List
from sys import stdin
from pathlib import Path
import forgeschema.helpers
from typing_extensions import Annotated

import typer

import forgeschema
import forgeschema.render

from ..validator import SpecCatalog

app = typer.Typer()
catalog = SpecCatalog()


@app.command()
def validate(spec: Annotated[
                        str, 
                        typer.Argument(help="Name of specification. Valid values are " + str(catalog.specs()))
                    ],
            input_file: Annotated[
                        List[Path],
                        typer.Argument(help="Input file(s) to validate. If omitted, waits for input on stdin")
                        ] = None,
            version: Annotated[
                        Optional[str], 
                        typer.Option(help="Version of specification. If omitted, latest will be used")
                        ] = None,
            encoding: Annotated[
                        Optional[str], 
                        typer.Option(help="Encoding to use. If omitted, and multiple encodings are available, the first available will be chosen")
                        ] = None,
            add_schema: Annotated[
                        List[Path],
                        typer.Option(help="Additional supporting schemas to include as part of the validating schema set (e.g. for the contents of TS 103 120 Delivery objects)")
                        ] = None
                        ):
    logging.basicConfig(level = logging.DEBUG)
    versions = catalog.versions(spec)
    if version is None:
        version = versions[-1]
        logging.info(f"No version specified, using latest ({version})")
    elif version not in versions:
        raise typer.BadParameter(f"Invalid version for {spec}. Valid values are {str(versions)}")
    encodings = catalog.encodings(spec, version)
    if encoding is None:
        encoding = encodings[-1]
        logging.info(f"No encoding specified, {len(encodings)} available, using {encoding}")
    elif encoding not in encodings:
        raise typer.BadParameter(f"Invalid encoding specified for {spec} v{version}. Valid values are {str(encodings)}")
    
    schema = catalog.schema_for(spec, version, encoding, additional_schemas = add_schema)
    config = catalog.load_config(spec, version, encoding)
    instance_extension = "xml" if encoding == "xsd" else "json"
    logging.debug(f"config retrieved: {config}")
    logging.debug(f"Input files specified: {input_file}")
                                                               
    if input_file is None:
        logging.debug(f"Taking input from stdin")
        text = stdin.read()
        logging.debug(f"Input: {text}")
        validation_errors = schema.validate_string(text)
        config["instanceDocs"] = ["stdin"]
        validation_errors = {"stdin" : validation_errors}
    else:
        config["instanceDocs"] = [expanded_path for path in input_file for expanded_path in forgeschema.helpers.expand_path(Path(path), ["*." + instance_extension])]
        logging.debug(f"Expanded input files {config['instanceDocs']}")
        validation_errors = {f : schema.validate(Path(f)) for f in config['instanceDocs']}

    forgeschema.render.render_validation_output(schema, validation_errors, config, show_validation=len(config["instanceDocs"]) > 1, hide_build_summary=True)
    # text_to_validate = input_file.read()
    # logging.debug("Text to validate:")
    # logging.debug(text_to_validate)
    # schema.expand_errors = False
    # errors = schema.validate_string(text_to_validate)
    # forgeschema.render.render_single_validation(schema, errors)