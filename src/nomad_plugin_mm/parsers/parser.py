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
from nomad_plugin_mm.schema_packages.cams import Run
configuration = config.get_plugin_entry_point(
    'nomad_plugin_mm.parsers:parser_entry_point'
)


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

        archive.data = run

        logger.info("Alles Gut")

