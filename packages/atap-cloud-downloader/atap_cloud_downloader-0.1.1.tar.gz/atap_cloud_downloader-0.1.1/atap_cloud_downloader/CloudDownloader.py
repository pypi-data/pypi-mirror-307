from os.path import normpath, sep
from typing import Callable

import gdown
import panel
import panel as pn
from gdown.exceptions import FileURLRetrievalError, FolderContentsMaximumLimitError
from panel.theme import Fast
from panel.viewable import Viewer

pn.extension(notifications=True, design=Fast)


class CloudDownloader(Viewer):
    def __init__(self, download_directory: str = '.', **params):
        """
        :param download_directory: The directory that the downloaded files will be written to. Defaults to current working directory
        :type download_directory: str
        :param params: passed onto the text_field.viewable.Viewer super-class
        """
        super().__init__(**params)
        self.download_directory: str = self._sanitise_dir(download_directory)
        self.text_field = pn.widgets.TextInput(name='File share URL', placeholder='Paste file share URL here')
        self.download_button = pn.widgets.Button(name='Download', button_type='primary', align='center')

        self.panel = pn.Row(self.text_field, self.download_button)

        self.download_button.on_click(self.download_file)

        self.url_prefix_map: dict[str, Callable] = {
            'https://drive.google.com/file/': self._download_google_file
        }

    def __panel__(self):
        return self.panel

    @staticmethod
    def display_error(error_msg: str):
        panel.state.notifications.error(error_msg, duration=0)

    @staticmethod
    def display_success(success_msg: str):
        panel.state.notifications.success(success_msg)

    @staticmethod
    def _sanitise_dir(directory: str) -> str:
        if not isinstance(directory, str):
            raise TypeError(f"Expected directory to be str, got {type(directory)}")
        sanitised_directory = normpath(directory)

        if not sanitised_directory.endswith(sep):
            sanitised_directory += sep

        return str(sanitised_directory)

    def _download_google_file(self, gdrive_url: str):
        try:
            gdown.download(url=gdrive_url, output=self.download_directory, fuzzy=True)
        except FileURLRetrievalError:
            self.display_error("Failed to retrieve file url: Cannot retrieve the public link of the file.\nYou may need to change the permission to 'Anyone with the link', or have had many accesses.")
            return
        except FolderContentsMaximumLimitError as e:
            self.display_error(str(e))
            return
        except Exception as e:
            self.display_error(f"Unexpected error while downloading: {str(e)}")
            return
        self.display_success("File(s) downloaded successfully")

    def download_file(self, *_):
        file_url: str = self.text_field.value
        if not file_url:
            self.display_error("File share URL field is empty. Provide a file share URL and click 'Download'")
            return

        for url_prefix in self.url_prefix_map:
            if file_url.startswith(url_prefix):
                download_method: Callable = self.url_prefix_map[url_prefix]
                download_method(file_url)
                return

        self.display_error("File share URL doesn't match any supported file share hosts")
