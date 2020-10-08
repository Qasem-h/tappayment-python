from .base import Resource
from ..constants.url import URL

class Payment(Resource):
    def __init__(self, client):
        super(Payment, self).__init__(client)
        self.base_url = client.base_url

    def all(self, data={}, **kwargs):
        
        return super(Payment, self).all(data, **kwargs)
    
    def authorize(self, data={}, **kwargs):

        print(URL.AUTH_URL)
        return self.post_url(URL.AUTH_URL, data, **kwargs)
    
    def get_authorize_status(self, authorize_id, data={}, **kwargs):
        authorize_id = authorize_id
        url = "{}/{}".format(URL.AUTH_URL, authorize_id)
        return self.get_url(url, data, **kwargs)

    def authorize_void(self, data={}, **kwargs):
        authorize_id = data['authorize_id']
        url = "{}/{}/void".format(URL.AUTH_URL, authorize_id)
        return self.post_url(url, data, **kwargs)

    def authorize_capture(self, data={}, **kwargs):

        print(URL.CHARGE_URL)
        return self.post_url(URL.CHARGE_URL, data, **kwargs)

    def refund(self, data={}, **kwargs):

        return self.post_url(URL.REFUND_URL, data, **kwargs)


    def get_refund_status(self, charge_id, data={}, **kwargs):
        charge_id = charge_id
        url = "{}/{}".format(URL.REFUND_URL, charge_id)
        return self.get_url(url, data, **kwargs)


    def charge(self, data={}, **kwargs):

        print(URL.CHARGE_URL)
        return self.post_url(URL.CHARGE_URL, data, **kwargs)

    def get_charge_status(self, charge_id, data={}, **kwargs):
        charge_id = charge_id
        url = "{}/{}".format(URL.CHARGE_URL, charge_id)
        return self.get_url(url, data, **kwargs)
