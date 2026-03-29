from enum import Enum


class TransportCategory(str, Enum):
    # buses
    RAPID_BUS_KL = "rapid-bus-kl"
    RAPID_BUS_MRT_FEEDER = "rapid-bus-mrtfeeder"
    RAPID_BUS_KUANTAN = "rapid-bus-kuantan"
    RAPID_BUS_PENANG = "rapid-bus-penang"

    # trains
    RAPID_RAIL_KL = "rapid-rail-kl"
