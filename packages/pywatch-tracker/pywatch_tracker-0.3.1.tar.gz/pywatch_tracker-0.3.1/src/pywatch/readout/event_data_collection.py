import json
import typing
from typing import Dict, Union, List, Tuple

import pandas as pd

from .hit_data import HitData


__all__ = ["EventData", "EventDataCollection", "load_event_data_collection_from_csv",
           "load_event_data_collection_from_json", "from_dataframe"]


class EventData(dict):
    """
    Dictionary that stores ``HitData`` objects with detector indices as keys.

    """

    def to_dict(self) -> Dict[int, Dict[str, Union[int, float]]]:
        """
        Create a dictionary, where the ``HitData`` objects are converted into dictionaries.

        :return: Data registered in an event
        :rtype: Dict[int, Dict[str, Union[int, float]]]
        """
        new_dct = dict()
        for key, value in self.items():
            new_dct[key] = value.__dict__

        return new_dct


class EventDataCollection:
    """
    Class for storing data registered in detector events

    The Data is stored a Pandas ``DataFrame`` where every row contains hit data with the index of the detector
    that recorded the data and the index of the event. Data can be accessed via the ``DataFrame``, which
    allows access to individual hit data that is not grouped by the event index. The ``EventData``
    of an event can be accessed by indexing the ``EventDataCollection`` object.

    Example:
    --------
    >>> # Load a stored EventDataCollection
    >>> data = load_event_data_collection_from_csv("data.csv")
    >>>
    >>> # Access the DataFrame
    >>> dataframe = data.df
    >>>
    >>> # print the first registered event
    >>> print(data[0])

    """

    def __init__(self):
        self.df = pd.DataFrame(
            columns=["index", "detector_index", "comp_time", "ard_time", "amplitude", "sipm_voltage", "dead_time",
                     "temp"])

        # Tracks which at which index an event starts in the dataframe and when it ends
        self._meta: List[Tuple[int, int]] = []

        self._len = 0
        self._index = 0  # Index needed for the Iterator
        self._dataframe_index = 0

    @property
    def len(self) -> int:
        return self._len

    def add_event(self, data: EventData) -> None:
        """Append an ``EventData`` object to the end of the DataFrame."""

        # Check if data has the right type
        if not isinstance(data, dict):
            raise TypeError("data added to EventDataCollection must be a dict")

        type_key = set([type(key) for key in data.keys()])
        type_value = set([type(value) for value in data.values()])

        if type_key != {int} or type_value != {HitData}:
            raise TypeError("data added to EventDataCollection must be a dict with "
                            "integer keys and HitData as values.")

        self._meta.append((len(self.df), len(data) + len(self.df)))
        for dt_index, hit in data.items():
            self.df.loc[self.df.__len__()] = [self._len, dt_index, *(hit.__dict__.values())]

        self._len += 1

    def get_df_list(self) -> List[pd.DataFrame]:
        """

        Return the data grouped by the event index.

        :return: List, where every element is event data stored as a ``DataFrame``
        :rtype: List[pd.DataFrame]

        """
        return [row.drop("index", axis=1) for _, row in self.df.groupby(["index"], as_index=True, group_keys=False)]

    def clear(self) -> None:
        """Clear all the data from memory."""

        del self.df
        self.df = pd.DataFrame(
            columns=["index", "detector_index", "comp_time", "ard_time", "amplitude", "sipm_voltage", "dead_time",
                     "temp"])
        self._len = 0

    def to_json(self, file_path: str) -> None:
        raise NotImplementedError
        # with open(file_path, "w") as file:
        #     dct = {
        #         "event_count": len(self._events),
        #         "data"       : [x.to_dict() for x in self._events]
        #     }
        #     json.dump(dct, file, indent=4)

    def save(self, file_path: str) -> None:
        """

        Save the data as a .csv file.

        :param type str file_path: File path to save the data.

        """
        self.df.to_csv(file_path, index=False)

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, index: int) -> EventData:
        # items = self.df.query(f"index == {index}")
        df_index_start, df_index_end = self._meta[index]
        items = self.df.iloc[df_index_start: df_index_end]

        event = EventData()

        for index, row in items.iterrows():
            event[int(row.iloc[1])] = HitData(*row.iloc[2:].values)

        return event

    def __iter__(self) -> "EventDataCollection":
        self._index = 0
        self._dataframe_index = 0
        return self

    def __next__(self):
        if self._index >= self._len:
            raise StopIteration

        event = EventData()
        current_row = self.df.loc[self._dataframe_index]

        while current_row["index"] == self._index:
            event[int(current_row.iloc[1])] = HitData(*current_row.iloc[2:].values)

            self._dataframe_index += 1
            if self._dataframe_index >= self.df.__len__():
                break
            current_row = self.df.loc[self._dataframe_index]

        self._index += 1

        return event


# TODO HANDLE EXCEPTIONS
def load_event_data_collection_from_json(file_path: str) -> EventDataCollection:
    """

    Loads the EventData made in a measurement into an EventDataCollection object.

    The file located in ``file_path`` should be a .json file with the following structure:
        {
            "event_count": Number of Events,
            "data": List of Event Data as dictionaries
        }

    :param str file_path: Path to the .json file

    :return: Data of a coincidence measurement
    :rtype: EventDataCollection

    """
    # TODO Change for new EventDataCollection
    with open(file_path, "r", encoding="utf-8") as file:
        raw = json.load(file)["data"]

    collection = EventDataCollection()
    for data in raw:
        event = EventData()
        for key, value in data.items():
            event[int(key)] = HitData(**value)

        collection.add_event(event)

    return collection


def from_dataframe(df: pd.DataFrame) -> EventDataCollection:
    """

    Create an ``EventDataCollection`` object from a pandas dataframe.

    :param type DataFrame df: data from measurement
    :return: Data as a ``EventDataCollection`` object
    :rtype: EventDataCollection

    """
    collection = EventDataCollection()
    collection.df = df
    collection._len = 0
    # event = EventData()
    event_index = 0
    current_index = 0

    for index, row in df.iterrows():
        if row["index"] != current_index:
            current_index += 1
            collection._meta.append((event_index, index))
            event_index = index

    collection._len = current_index + 1
    collection._meta.append((event_index, collection.df.__len__()))

    return collection


def load_event_data_collection_from_csv(file_path: str) -> EventDataCollection:
    """

    Load the measurement data from a csv file.

    :param type str file_path: Path to the csv file

    :return: Data as a ``EventDataCollection`` object
    :rtype: EventDataCollection

    """
    csv_data = pd.read_csv(file_path)

    return from_dataframe(csv_data)
