from dataclasses import dataclass

@dataclass
class Staycation():
    hotel_name : str
    duration : int
    unit_cost : int
    image_url : str
    description : str