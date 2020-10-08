from .base import Resource
from ..constants.url import URL

class Refund(Resource):
    def __init__(self, client):
        super(Refund, self).__init__(client)
        self.base_url = client.base_url

    def all(self, data={}, **kwargs):
        
        return super(Refund, self).all(data, **kwargs)

    def refund(self, data={}, **kwargs):
        
        return self.post_url(URL.REFUND_URL, data, **kwargs)

    def get_refund_status(self, charge_id, data={}, **kwargs):
        charge_id = charge_id
        url = "{}/{}".format(URL.REFUND_URL, charge_id)
        return self.get_url(url, data, **kwargs)
