import os
import time
import tempfile
import tarfile
import logging

from blackboxai import urls
from blackboxai.coders import Coder
from blackboxai.dump import dump  # noqa: F401
from blackboxai.io import InputOutput
from blackboxai.main import create_coder
from blackboxai.scrape import Scraper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CaptureIO(InputOutput):
    lines = []

    def tool_output(self, msg, log_only=False):
        if not log_only:
            self.lines.append(msg)
        super().tool_output(msg, log_only=log_only)

    def tool_error(self, msg):
        self.lines.append(msg)
        super().tool_error(msg)

    def tool_warning(self, msg):
        self.lines.append(msg)
        super().tool_warning(msg)

    def get_captured_lines(self):
        lines = self.lines
        self.lines = []
        return lines


class UserState:
    def __init__(self):
        self.messages: List[Dict] = []
        self.input_history: List[str] = []
        self.initial_inchat_files: List[str] = []
        self.scraper: Optional[Scraper] = None


class Session:
    last_active_ts: int = 0
    is_alive: bool = True
    
    def __init__(self, sid: str, repository):
        self.sid = sid
        self.last_active_ts = int(time.time())
        self.coder = self._initialize_coder(repository)
        self.state = self._initialize_state()

    def _initialize_coder(self, repository) -> Coder:
        work_dir, all_files = self.add_repository(repository)
        self.work_dir = work_dir
        coder = create_coder(argv=[], return_coder=True, files=all_files)
        if not isinstance(coder, Coder):
            raise ValueError(coder)

        io = CaptureIO(
            pretty=False,
            yes=True,
            dry_run=coder.io.dry_run,
            encoding=coder.io.encoding,
        )
        coder.sid = self.sid
        coder.commands.io = io

        coder.yield_stream = True
        coder.stream = True
        coder.pretty = False

        return coder

    def _initialize_state(self) -> UserState:
        state = UserState()
        state.messages = []
        state.initial_inchat_files = self.coder.get_inchat_relative_files()
        state.input_history = list(self.coder.io.get_input_history())
        return state

    def add_repository(self, content):
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, "workdir.tar")
        
        # Save the uploaded file content to the tar file
        with open(temp_file_path, "wb") as buffer:
            buffer.write(content)
        
        # Extract the tar file
        with tarfile.open(temp_file_path, "r:*") as tar:
            tar.extractall(path=temp_dir)

        # clean
        os.remove(temp_file_path)
        
        # Get all file names
        all_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                all_files.append(file_path)
        
        logger.info(f"Created temporary directory: {temp_dir}")
        logger.info(f"Extracted files: {all_files}")

        return temp_dir, all_files

    async def close(self):
        """Clean up session resources and prepare for deletion"""
        if self.coder:
            # Clear coder's references
            if hasattr(self.coder, 'commands') and self.coder.commands:
                self.coder.commands.io = None
                self.coder.commands = None
            
            if hasattr(self.coder, 'io') and self.coder.io:
                self.coder.io.lines = []
                self.coder.io = None

            # Clear message history
            if hasattr(self.coder, 'done_messages'):
                self.coder.done_messages = []
            if hasattr(self.coder, 'cur_messages'):
                self.coder.cur_messages = []

            self.coder = None

        if self.state:
            # Clear state data
            self.state.messages = []
            self.state.input_history = []
            self.state.initial_inchat_files = []
            if self.state.scraper:
                self.state.scraper = None
            self.state = None
