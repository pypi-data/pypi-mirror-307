"""Main entry point for the Duet SimplyPrint connector."""
import logging

from simplyprint_ws_client.cli import ClientCli
from simplyprint_ws_client.client import ClientApp, ClientMode, ClientOptions
from simplyprint_ws_client.client.config import ConfigManagerType
from simplyprint_ws_client.client.logging import ClientHandler
from simplyprint_ws_client.helpers.url_builder import SimplyPrintBackend

from . import __version__
from .cli.autodiscover import AutoDiscover
from .cli.install import install_as_service
from .virtual_client import VirtualClient, VirtualConfig


def main():
    """Initiate the connector as the main entry point."""
    client_options = ClientOptions(
        name="DuetConnector",
        version=__version__,
        mode=ClientMode.MULTI_PRINTER,
        client_t=VirtualClient,
        config_t=VirtualConfig,
        allow_setup=True,
        config_manager_type=ConfigManagerType.JSON,
        backend=SimplyPrintBackend.PRODUCTION,
    )

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(name)s.%(funcName)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            ClientHandler.root_handler(client_options),
        ],
    )

    app = ClientApp(client_options)
    cli = ClientCli(app)

    autodiscover = AutoDiscover(app)

    cli.add_command(autodiscover.autodiscover)
    cli.add_command(install_as_service)
    cli.start_client = lambda: app.run_blocking()
    cli(prog_name="python -m meltingplot.duet_simplyprint_connector")


if __name__ == "__main__":
    main()
