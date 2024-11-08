class Organization:
    """"""


    def __init__(self, client):
        """"""

        self.api = client


    def get(self, id):
        """"""

        result = self.api.get(f"organization/{id}")

        return result
