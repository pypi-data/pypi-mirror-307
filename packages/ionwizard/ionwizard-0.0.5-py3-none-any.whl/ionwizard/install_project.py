import sys
import copy
import subprocess
import toml
from ionwizard.validate import read_config_libraries
from ionwizard.library_wizard import IonWorksPipWizard
import tempfile
from pathlib import Path


class IonWorksInstallWizard(IonWorksPipWizard):
    """
    Install a project from a pyproject.toml file, while installing ionworks
    dependencies separately.
    """

    def collect_libraries_to_install(self):
        if len(sys.argv) > 1:
            if ".yml" in sys.argv[1]:
                config_file = sys.argv[1]
                processed_config = self.process_config(config_file)
                self.save_config(processed_config)
        libraries = read_config_libraries()
        return libraries

    @staticmethod
    def copy_local_pyproject_file():
        with open("pyproject.toml") as f:
            original_pyproject_toml = toml.load(f)
        return copy.deepcopy(original_pyproject_toml)

    def install_libraries_from_config(self, libraries):
        pyproject_file = self.copy_local_pyproject_file()
        remaining_dependencies = []
        local_dependencies = []
        lib_names = [lib["library"] for lib in libraries]
        for dep in pyproject_file["project"]["dependencies"]:
            if dep.split("==")[0] in lib_names:
                local_dependencies.append(dep)
            else:
                remaining_dependencies.append(dep)

        for dep in local_dependencies:
            for library in libraries:
                if dep.startswith(library["library"]):
                    addr = IonWorksPipWizard.get_address(library["key"])
                    IonWorksPipWizard.install_library(dep, addr)

        pyproject_file["project"]["dependencies"] = remaining_dependencies
        return pyproject_file

    @staticmethod
    def install_from_pyproject(pyproject_file):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_config = Path(temp_dir) / "pyproject.toml"
            with open(temp_config, "w") as f:
                toml.dump(pyproject_file, f)
            cmd = [
                "pip",
                "install",
                "-e",
                ".",
                f"--config-settings=pyproject_toml={temp_config}",
            ]
            subprocess.run(cmd)


def run():
    libraries = IonWorksInstallWizard().collect_libraries_to_install()
    new_pyproject = IonWorksInstallWizard().install_libraries_from_config(libraries)
    IonWorksInstallWizard.install_from_pyproject(new_pyproject)


if __name__ == "__main__":
    run()
