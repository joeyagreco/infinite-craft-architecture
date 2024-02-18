from abc import ABC, abstractmethod


class Alivable(ABC):
    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the alivable.
        """
        ...

    @abstractmethod
    def alive(self) -> bool:
        """
        Returns whether or not the connection test succeeded.
        """
        # TODO: possible add a parameter for number of retries?
        ...
