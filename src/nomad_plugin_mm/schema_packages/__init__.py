from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_plugin_mm.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='NewSchemaPackage',
    description='New schema package entry point configuration.',
)

class CAMSEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugin_mm.schema_packages.cams import m_package

        return m_package
    
cams_entry_point = CAMSEntryPoint(
    name='CAMSPackage',
    description='CAMSPackage entry point configuration.',
)