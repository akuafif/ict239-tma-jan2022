from dataclasses import dataclass

# using dataclass to define objects with only data and very minimal functionalities
@dataclass
class Staycation():
    hotel_name : str
    duration : int
    unit_cost : int
    image_url : str
    description : str