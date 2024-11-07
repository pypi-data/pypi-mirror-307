import subprocess


def execute_command(command, mock_input=None):
    # print(f"DEBUG: Executing command: {command}")
    if mock_input:
        # print(f"DEBUG: Mock input provided: {mock_input}")
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = process.communicate(input=mock_input.encode())

        # print(f"DEBUG: Command stdout: {stdout_data.decode().strip()}")
        # print(f"DEBUG: Command stderr: {stderr_data.decode().strip()}")
    else:
        # print(f"DEBUG: No Mock input provided")
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return process

class Artefact:
    def __init__(self, name, classifier):
        self.name = name
        self.classifier = classifier
        # print(f"DEBUG: Initialized Artefact with name='{name}' and classifier='{classifier}'")

    def create(self):
        command = f"ara create {self.classifier} {self.name}"
        # print(f"DEBUG: Creating artefact with command: {command}")
        result = execute_command(command, mock_input="y")
        if result.returncode != 0:
            # print(f"DEBUG: Error encountered during artefact creation.")
            pass
        else:
            # print(f"DEBUG: Artefact created successfully.")
            pass
        return result

    def delete(self):
        command = f"ara delete {self.classifier} {self.name}"
        # print(f"DEBUG: Deleting artefact with command: {command}")
        result = execute_command(command, mock_input="y")
        if result.returncode != 0:
            # print(f"DEBUG: Error encountered during artefact deletion.")
            pass
        else:
            # print(f"DEBUG: Artefact deleted successfully.")
            pass
        return result
