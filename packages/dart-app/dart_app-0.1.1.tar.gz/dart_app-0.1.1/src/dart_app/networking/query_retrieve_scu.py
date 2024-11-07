import time
import re
import logging
from logging import Handler, StreamHandler, FileHandler, Formatter
from typing import List, Dict, Optional, Union
from contextlib import contextmanager
from pydicom.dataset import Dataset
from pynetdicom import AE
from pynetdicom.presentation import build_context
from pynetdicom.sop_class import (
    Verification,
    StudyRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelMove,
)


class QueryRetrieveSCU:
    def __init__(
        self,
        ae_title: str,
        acse_timeout: int = 120,
        dimse_timeout: int = 121,
        network_timeout: int = 122,
        logger: Optional[logging.Logger] = None,
    ):
        self.ae_title = ae_title

        self.ae = AE(self.ae_title)
        self.ae.acse_timeout = acse_timeout
        self.ae.dimse_timeout = dimse_timeout
        self.ae.network_timeout = network_timeout
        self.remote_entities: Dict[str, Dict] = {}  # Remote AEs

        self.ae.add_requested_context(Verification)
        self.ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)
        self.ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
        # Configure logger
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            # Set up a null handler (no output to console or file)
            null_handler = StreamHandler()
            null_handler.setLevel(logging.CRITICAL)
            self.logger.addHandler(null_handler)

    def add_remote_ae(self, name: str, ae_title: str, host: str, port: int):
        """Add a remote AE to the dictionary of managed AEs."""
        if not (
            self.valid_entry(ae_title, "AET")
            and self.valid_entry(port, "Port")
            and self.valid_entry(host, "IP")
        ):
            raise ValueError("Invalid input for AE Title, Host, or Port.")

        if name in self.remote_entities:
            self.logger.warning(f"AE '{name}' already exists. Overwriting AE info.")
        self.remote_entities[name] = {
            "ae_title": ae_title,
            "host": host,
            "port": port,
        }
        self.logger.info(f"Added remote AE '{name}': {ae_title}@{host}:{port}")

    def add_extended_negotiation(self, ae_name: str, ext_neg_items: List):
        """Add extended negotiation items to the remote AE.
        The ext_neg_items parameter should be a list of extended negotiation objects
        (e.g., SOPClassExtendedNegotiation, AsynchronousOperationsWindowNegotiation).
        """
        if ae_name not in self.remote_entities:
            raise ValueError(
                f"Remote AE '{ae_name}' not found. Add it with `add_remote_ae` first."
            )

        rm_ae = self.remote_entities[ae_name]
        rm_ae["ext_neg"] = ext_neg_items

    @contextmanager
    def association_context(self, ae_name: str):
        """Context manager for establishing and releasing an association."""
        assoc = self._establish_association(ae_name)
        try:
            if assoc and assoc.is_established:
                yield assoc
            else:
                yield None
        finally:
            if assoc and assoc.is_established:
                assoc.release()

    def _establish_association(self, ae_name: str, retry_count: int = 3, delay: int = 5):
        """Helper method to establish an association with a remote AE, with retry logic."""
        if ae_name not in self.remote_entities:
            raise ValueError(
                f"Remote AE '{ae_name}' not found. Add it with `add_remote_ae` first."
            )

        rm_ae = self.remote_entities[ae_name]
        ext_neg = rm_ae.get("ext_neg", [])

        for attempt in range(retry_count):
            try:
                assoc = self.ae.associate(
                    rm_ae["host"],
                    rm_ae["port"],
                    ae_title=rm_ae["ae_title"],
                    ext_neg=ext_neg,
                )
                if assoc.is_established:
                    return assoc
            except Exception as e:
                self.logger.error(
                    f"Association attempt {attempt + 1} failed with AE '{ae_name}': {e}"
                )
                time.sleep(delay)

        self.logger.error(f"Failed to associate with AE '{ae_name}' after {retry_count} attempts.")
        return None

    def c_echo(self, ae_name: str):
        """Launch a C-ECHO request to verify connectivity with a remote AE."""
        with self.association_context(ae_name) as assoc:
            if assoc:
                self.logger.info(f"Association established with {ae_name}. Sending C-ECHO...")
                status = assoc.send_c_echo()
                if status.Status == 0x0000:
                    self.logger.info(f"C-ECHO with '{ae_name}' successful.")
                    return True
                else:
                    self.logger.error(f"C-ECHO with '{ae_name}' failed. Status: {status}")
                    return False
            else:
                self.logger.error(f"Failed to associate with {ae_name}.")
                return False

    def c_find(self, ae_name: str, query: Dataset) -> Optional[List[Dataset]]:
        """Perform a C-FIND request using the provided query Dataset."""
        with self.association_context(ae_name) as assoc:
            if assoc:
                self.logger.info(f"Association established with {ae_name}. Sending C-FIND...")
                results = []
                responses = assoc.send_c_find(query, StudyRootQueryRetrieveInformationModelFind)
                for status, identifier in responses:
                    if status and status.Status in (0xFF00, 0xFF01):
                        results.append(identifier)
                return results
            else:
                self.logger.error(f"Failed to associate with {ae_name}.")
                return None

    def c_move(self, ae_name: str, query: Dataset, destination_ae: str):
        """Perform a C-MOVE request to move studies to a specified AE."""
        with self.association_context(ae_name) as assoc:
            if assoc:
                self.logger.info(
                    f"Association established with {ae_name}. "
                    f"Sending C-MOVE to '{destination_ae}'..."
                )
                responses = assoc.send_c_move(
                    query,
                    destination_ae,
                    StudyRootQueryRetrieveInformationModelMove,
                )
                for status, _ in responses:
                    if status.Status == 0x0000:
                        self.logger.info(f"C-MOVE successful to AE '{destination_ae}'.")
                    else:
                        self.logger.error(f"C-MOVE failed. Status: {status}")
            else:
                self.logger.error(f"Failed to associate with {ae_name}.")

    def c_store(self, ae_name: str, dataset: Dataset):
        """Perform a C-STORE request to store a dataset to a remote AE."""
        context = build_context(dataset.SOPClassUID)
        if not any(
            ctx.abstract_syntax == context.abstract_syntax for ctx in self.ae.requested_contexts
        ):
            try:
                self.ae.add_requested_context(context)
            except ValueError:
                self.ae.requested_contexts.pop()
                self.ae.add_requested_context(context)

        with self.association_context(ae_name) as assoc:
            if assoc:
                self.logger.info(f"Association established with {ae_name}. Sending C-STORE...")
                status = assoc.send_c_store(dataset)
                if status.Status == 0x0000:
                    self.logger.info(f"C-STORE with '{ae_name}' successful.")
                else:
                    self.logger.error(f"C-STORE with '{ae_name}' failed. Status: {status}")
            else:
                self.logger.error(f"Failed to associate with {ae_name}.")

    def set_logger(self, new_logger: logging.Logger):
        """Set a new logger for the class, overriding the existing one."""
        self.logger = new_logger

    def add_log_handler(self, handler: Handler):
        """Add an additional handler to the existing logger."""
        self.logger.addHandler(handler)

    def configure_logging(
        self,
        log_to_console: bool = True,
        log_to_file: bool = False,
        log_file_path: str = "query_retrieve_scu.log",
        log_level: int = logging.INFO,
        formatter: Optional[Formatter] = None,
    ):
        """Configure logging with console and/or file handlers.

        Parameters
        ----------
        log_to_console : bool
            Whether to log to the console.
        log_to_file : bool
            Whether to log to a file.
        log_file_path : str
            The path to the log file if `log_to_file` is True.
        log_level : int
            The logging level (e.g., logging.INFO, logging.DEBUG).
        formatter : Optional[Formatter]
            A custom formatter for the log messages. If None, a default formatter is used.
        """
        if formatter is None:
            formatter = Formatter("%(levelname).1s: %(asctime)s: %(name)s: %(message)s")

        if log_to_console:
            console_handler = StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_to_file:
            file_handler = FileHandler(log_file_path)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    @staticmethod
    def valid_entry(input_text: Union[str, int], entry_type: str) -> bool:
        """Checks whether a text input from the user contains invalid characters.

        Parameters
        ----------
        input_text : Union[str, int]
            The text input to a given field.
        entry_type : str
            The type of field where the text was input. The different
            types are:
            * AET
            * Port
            * IP

        Returns
        -------
        bool
            Whether the input was valid or not.
        """
        if entry_type == "AET":
            return isinstance(input_text, str) and not re.search(r'[ "\'*]', input_text)
        elif entry_type == "Port":
            return isinstance(input_text, int) and 1 <= input_text <= 65535
        elif entry_type == "IP":
            ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
            return isinstance(input_text, str) and ip_pattern.match(input_text) is not None
        else:
            return False
