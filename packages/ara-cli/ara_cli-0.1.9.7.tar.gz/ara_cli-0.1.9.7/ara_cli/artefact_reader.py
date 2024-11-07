from ara_cli.directory_navigator import DirectoryNavigator
from ara_cli.classifier import Classifier
import os
import re


class ArtefactReader:
    @staticmethod
    def read_artefact(artefact_name, classifier):
        original_directory = os.getcwd()
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            return

        sub_directory = Classifier.get_sub_directory(classifier)
        file_path = os.path.join(sub_directory, f"{artefact_name}.{classifier}")

        file_exists = os.path.exists(file_path)

        if not file_exists:
            print(f"File \"{file_path}\" not found")
            os.chdir(original_directory)
            return None, None

        with open(file_path, 'r') as file:
            content = file.read()

        os.chdir(original_directory)

        return content, file_path

    @staticmethod
    def extract_parent_tree(artefact_content):
        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'Contributes to\s*:*\s*(.*)\s+({title_segment}).*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, artefact_content)
        if not match:
            return None, None

        parent_name = match.group(1).strip()
        parent_type = match.group(2).strip()

        return parent_name, parent_type
