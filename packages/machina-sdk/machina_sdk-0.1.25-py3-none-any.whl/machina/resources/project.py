class Project:
    """"""


    def __init__(self, client):
        """"""

        self.api = client


    def get(self, id):
        """"""

        result = self.api.get(f"project/{id}")

        return result
