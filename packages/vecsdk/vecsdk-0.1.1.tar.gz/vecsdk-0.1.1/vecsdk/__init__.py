import grpc
import numpy as np
from dataclasses import dataclass
from vectorization_pb2 import VectorizeRequestSet, KeyValuePairSet, KeyValuePair, StringOrFloatValue, Setting
from vectorization_pb2_grpc import VectorizationServiceStub
from typing import Dict, List, Union, Callable, Set, Tuple, Any
from itertools import chain, starmap
from grpc import RpcError

@dataclass
class VectorProperty:

    index: str
    vector: np.ndarray
    value: Union[str, float]

    def __repr__(self):
        return f"VectorProperty(index={self.index}, vector=[...], value={self.value})"

    def aggregate(self, weights: Dict[str, float] = {}) -> np.ndarray:
        return self.vector * weights.get(self.index, 1.0)
    
    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the property.
        """
        return {
            "index": self.index,
            "value": self.value,
            "vector": self.vector.tolist()
        }

@dataclass
class VectorGroup:

    index:  Union[int, str]
    values: List[Union["VectorGroup", VectorProperty]]

    def aggregate(
        self, 
        weights: Dict[str, float] = {}, 
        aggregator: Callable[[np.ndarray], np.ndarray] = lambda x: np.mean(x, axis=0)
    ) -> np.ndarray:
        """
            Aggregates the vectors of the group. It will aggregate the vectors of the subgroups and the properties recursively.

            Args:
                weights: A dictionary with the weights for each property (default 1.0).
                agg: The aggregation function to be used.

            Returns:
                A VectorProperty with the aggregated vector.
        """
        return aggregator(
            np.array(
                list(
                    filter(
                        lambda x: not np.isnan(x).any(), 
                        chain(
                            map(
                                lambda x: x.aggregate(weights),
                                filter(
                                    lambda x: issubclass(x.__class__, VectorGroup),
                                    self.values
                                ),
                            ),
                            map(
                                lambda x: x.aggregate(weights),
                                filter(
                                    lambda x: issubclass(x.__class__, VectorProperty),
                                    self.values
                                )
                            )
                        )
                    )
                )
            )
        ) * weights.get(self.index, 1.0)

@dataclass
class VectorizationSettings:
    key_coefficient:        int = 1
    string_val_coefficient: int = 1
    float_val_coefficient:  int = 1

    def to_proto(self) -> Setting:
        return Setting(
            key_coefficient=self.key_coefficient,
            string_val_coefficient=self.string_val_coefficient,
            float_val_coefficient=self.float_val_coefficient
        )

@dataclass
class VectorizationServer:

    host: str
    port: int

    def __post_init__(self):
        if not self.is_ready(self.connection_string()):
            raise ValueError(f"Connection to {self.connection_string()} failed.")

    def connection_string(self):
        return f"{self.host}:{self.port}"
    
    @staticmethod
    def check_value(value: Any) -> Union[str, float]:
        """
            Only "allowed" leaf values are strings and floats.
            If the value is not a string or a float, we'll raise a ValueError.
        """
        if not isinstance(value, (str, float)):
            raise ValueError(f"Invalid value type: {type(value)}")
        return value
    
    @classmethod
    def dict_leafs(cls, d: Union[Dict, List]) -> Set[Tuple[str, Union[float, str]]]:
        """
        Return the leaf key-value pairs of a dictionary, handling both dictionaries and lists.
        """
        leafs = set()
        
        if isinstance(d, dict):
            # Iterate through dictionary items
            for k, v in d.items():
                if isinstance(v, dict) or isinstance(v, list):
                    # Recursively process nested dictionaries and lists
                    leafs.update(cls.dict_leafs(v))
                else:
                    # Add leaf node to the result
                    # NOTE check_value may raise a ValueError
                    leafs.add((k, cls.check_value(v)))
                    
        elif isinstance(d, list):
            # Iterate through each element in the list
            for item in d:
                if isinstance(item, dict) or isinstance(item, list):
                    # Recursively process nested dictionaries and lists
                    leafs.update(cls.dict_leafs(item))
        
        return leafs
        
    def build_vector_group(self, name: str, data: dict, leaf_vectors: Dict[tuple, np.ndarray]) -> Union[VectorGroup, VectorProperty]:
        if isinstance(data, dict):
            return VectorGroup(
                index=name,
                values=[
                    self.build_vector_group(k, v, leaf_vectors) for k, v in data.items()
                ]
            )
        elif isinstance(data, list):
            return VectorGroup(
                index=name,
                values=[
                    self.build_vector_group(i, v, leaf_vectors) for i, v in enumerate(data)
                ]
            )
        else:
            return VectorProperty(
                index=name,
                vector=leaf_vectors[(name, data)],
                value=data
            )
        
    def is_ready(self, timeout: int = 1) -> bool:
        """
        Checks if a gRPC service is up and running at the specified address.
        
        Parameters:
            address (str): The address of the gRPC service (e.g., 'localhost:50051').
            timeout (int): How long to wait for the connection to be ready (in seconds).
        
        Returns:
            bool: True if the service is up, False otherwise.
        """
        try:
            with grpc.insecure_channel(self.connection_string()) as channel:
                stub = VectorizationServiceStub(channel)
                stub.Vectorize(VectorizeRequestSet())
            return True
        except TypeError as e:
            print(f"TypeError encountered: {e}")
            return False
        except RpcError:
            return False

    def __call__(self, data: dict, index: str = "", settings: VectorizationSettings = VectorizationSettings()) -> VectorGroup:

        leafs = sorted(self.dict_leafs(data))
        with grpc.insecure_channel(self.connection_string()) as channel:
            stub = VectorizationServiceStub(channel)
            response = stub.Vectorize(
                VectorizeRequestSet(
                    key_value_pairs=KeyValuePairSet(
                        key_values=list(
                            starmap(
                                lambda k, v: KeyValuePair(
                                    key=k,
                                    value=StringOrFloatValue(
                                        string_value=v if isinstance(v, str) else None,
                                        float_value=v if isinstance(v, float) else None
                                    )
                                ),
                                leafs
                            )
                        )
                    ),
                    setting=settings.to_proto()
                )
            )

        return self.build_vector_group(index, data, dict(zip(leafs, np.array([v.value for v in response.vectors]))))