from .resources import Resource


class Coin(Resource):
    GOLD = "gold"
    SILVER = "silver"

    str_lookup = {"G": GOLD, "S": SILVER}
    all_resources = [SILVER, GOLD]
