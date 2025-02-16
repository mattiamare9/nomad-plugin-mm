from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser

import json
from nomad_plugin_mm.schema_packages.cams import Run, StepGeneric, Header, GeneralParameters
configuration = config.get_plugin_entry_point(
    'nomad_plugin_mm.parsers:parser_entry_point'
)

def parse_steps(steps_dict:dict) -> list:
    """
    now we are using stepgeneric, but this will be refactored to the specific steps
    that inherits from stepgeneric.
    """
    # steptype2class = {
    #     "Electron Gun" : ElectronGun()
    # }


    steps = []
    for step_no, step in steps_dict.items():
        step_generic = StepGeneric()
        #step = steptype2class[step_type]
        step_header = Header()
        step_general_parameters = GeneralParameters()

        step_header.step_number = step['Header']['Step#']
        step_header.step_type = step['Header']['Step type']
        step_header.description = step['Header']['Description']

        step_general_parameters.description = step['Step General Parameters']['Description']
        step_general_parameters.operator = step['Step General Parameters']['Operator']
        step_general_parameters.wafers = step['Step General Parameters']['Wafers']

        step_generic.header = step_header
        step_generic.general_parameters = step_general_parameters

        steps.append(step_generic)
    return steps


class NewParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('NewParser.parse', parameter=configuration.parameter)


        #data_dict = json.load(mainfile)
        
        with open(mainfile, 'r') as file:
            data_dict = json.load(file)

        
        run = Run()
        run.run_name = data_dict['run_name']
        run.project = data_dict['project']
        run.workpackage = data_dict['workpackage']
        run.run_description = data_dict['run_description']
        run.author = data_dict['author']
        run.cost_model = data_dict['cost_model']
        run.start_date = data_dict['start_date']
        run.generated_on = data_dict['generated_on']        
        
        run.steps = parse_steps(data_dict['steps'])


        archive.data = run

        logger.info("Alles Gut")

