import requests
import json

BoM_Url = "https://interviewbom.herokuapp.com/bom/"
Part_Url = "https://interviewbom.herokuapp.com/part/{id}/"


class BoMRequests:
    def get_bom(self):
        """
        Retrieve BoM string from REST API.
        :return: BoM json
        """
        try:
            ret = requests.get(BoM_Url)
            if ret.status_code == 200:
                return ret.json()
        except Exception:
            pass
        return None

    def get_part(self, part_id):
        """
        Get the part number from the REST API given the part id.
        :param part_id: part id
        :return: part number
        """
        try:
            ret = requests.get(Part_Url.format(id=part_id))
            if ret.status_code == 200:
                part_json = ret.json()
                return part_json['part_number']
        except Exception:
            pass
        return None


class MockRequests:
    def __init__(self, bom_str, part_number_dict):
        self.bom_json = json.loads(bom_str)
        self.part_number_dict = part_number_dict

    def get_bom(self):
        """
        Return the BoM json object.
        :return: BoM json
        """
        return self.bom_json

    def get_part(self, part_id):
        """
        Get the part number from the dictionary given the part id.
        :param part_id: part id
        :return: part number
        """
        return self.part_number_dict[part_id]
