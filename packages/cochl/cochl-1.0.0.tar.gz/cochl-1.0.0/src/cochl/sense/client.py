import os

from . import config, check_latest_lib_version
from .event import EventClient
from .result import Result
from .speaker import SpeakerClient


class Client:
    """Client is used to predict an audio file with Cochl.Sense."""

    def __init__(
        self,
        api_project_key: str,
        api_config: config.APIConfig = None,
    ):
        if not api_project_key:
            raise ValueError(f'invalid project key "{api_project_key}"')
        if api_config is None:
            api_config = config.APIConfig()  # use default APIConfig

        self.project_key: str = api_project_key
        self.api_config: config.APIConfig = api_config

        # check client library version
        check_latest_lib_version(self.api_config.get_host())

    def predict(self, file_path: str) -> Result:
        """
        Predicts the given file.

        Args:
            file_path: Path to the file. For example, '/Users/user/file.mp3'
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        result = Result()

        event_client = EventClient(self.project_key, self.api_config)
        result.events = event_client.predict(file_path)

        if not self.api_config.speaker_recognition:
            return result

        if '[Speech]' not in result.events.to_summarized_result():
            return result

        speaker_client = SpeakerClient(self.project_key, self.api_config)
        result.speakers = speaker_client.recognize(file_path)

        return result
