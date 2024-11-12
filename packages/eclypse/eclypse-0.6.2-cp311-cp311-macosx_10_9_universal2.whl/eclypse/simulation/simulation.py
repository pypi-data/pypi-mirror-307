from typing import (
    Optional,
    Union,
)

from eclypse.core.simulation import SimulationEngine
from eclypse.core.utils.tools import shield_interrupt
from eclypse.graph.application import Application
from eclypse.graph.infrastructure import Infrastructure
from eclypse.placement.strategies.placement_strategy import PlacementStrategy
from eclypse.remote.bootstrap.bootstrap import RemoteBootstrap
from eclypse.simulation.config import SimulationConfig


class Simulation(SimulationEngine):

    def __init__(
        self,
        infrastructure: Infrastructure,
        simulation_config: Optional[SimulationConfig] = None,
        remote: Union[bool, RemoteBootstrap] = False,
    ):
        """Create a new Simulation. It instantiates a Simulator or RemoteSimulator based
        on the simulation configuration, than can be either local or remote.

        It also registers an exit handler to ensure the simulation is properly closed
        and the reporting (if enabled) is done properly.

        Args:
            infrastructure (Infrastructure): The infrastructure to simulate.
            simulation_config (SimulationConfig, optional): The configuration of the \
                simulation. Defaults to SimulationConfig().

        Raises:
            ValueError: If all services do not have a logic when including them in a remote
                simulation.
        """
        super().__init__(infrastructure, simulation_config, remote)

    def start(self, blocking: bool = True):
        """Start the simulation.

        Args:
            blocking (bool, optional): If True, the simulation will block until it is \
                finished. Defaults to True.
        """
        super().start(blocking)

    def trigger(self, event_name: str, blocking: bool = True):
        """Trigger an event in the simulation.

        Args:
            event_name (str): The name of the event to trigger.
            blocking (bool, optional): If True, the simulation will block until it is \
                finished. Defaults to True.
        """
        return super().trigger(event_name, blocking)

    def feed(self, event_name: str):
        """Feed the simulation with events.

        Args:
            event (str): The event to feed.
        """
        return super().feed(event_name)

    def tick(self, blocking: bool = True):
        """Tick the simulation.

        Args:
            blocking (bool, optional): If True, the simulation will block until it is \
                finished. Defaults to True.
        """
        return super().tick(blocking)

    @shield_interrupt
    def wait(self):
        """Wait for the simulation to finish.

        This method is blocking and will wait until the simulation is finished. It can
        be interrupted by pressing `Ctrl+C`.
        """
        super().wait()

    def register(
        self,
        application: Application,
        placement_strategy: Optional[PlacementStrategy] = None,
    ):
        """Include an application in the simulation.

        Args:
            application (Application): The application to include.
            placement_strategy (PlacementStrategy): The placement strategy to use \
                to place the application on the infrastructure.

        Raises:
            ValueError: If all services do not have a logic when including them \
                in a remote simulation.
        """
        super().register(application, placement_strategy)

    @property
    def applications(self):
        """Get the applications in the simulation.

        Returns:
            List[Application]: The applications in the simulation.
        """
        return super().applications

    @property
    def logger(self):
        """Get the logger of the simulation.

        Returns:
            Logger: The logger of the simulation.
        """
        return super().logger

    @property
    def status(self):
        """Get the status of the simulation.

        Returns:
            str: The status of the simulation.
        """
        return super().status

    @property
    def report(self):
        """Get the report of the simulation.

        Returns:
            Report: The report of the simulation.
        """
        return super().report
