import typing
from .scenario import TestScenario


class Network1(TestScenario):
    not_ssl = False
    get_insecure = False
    web_view_client = False
    vulnerable_x509_certificate = False
    detail = []

    def __init__(self,
                 not_ssl: typing.Optional[bool] = None,
                 get_insecure: typing.Optional[bool] = None,
                 web_view_client: typing.Optional[bool] = None,
                 vulnerable_x509_certificate: typing.Optional[bool] = None,
                 detail: typing.Optional[typing.List[str]] = None):
        if not_ssl is not None:
            self.not_ssl = not_ssl
        if get_insecure is not None:
            self.get_insecure = get_insecure
        if web_view_client is not None:
            self.web_view_client = web_view_client
        if vulnerable_x509_certificate is not None:
            self.vulnerable_x509_certificate = vulnerable_x509_certificate
        if detail is not None:
            self.detail = detail

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new_not_ssl = self.not_ssl or other.not_ssl
        new_get_insecure = self.get_insecure or other.get_insecure
        new_web_view_client = self.web_view_client or other.web_view_client
        new_vulnerable_x509_certificate = self.vulnerable_x509_certificate or other.vulnerable_x509_certificate
        new_detail = [detail for detail in self.detail]
        for detail in other.detail:
            if detail not in new_detail:
                new_detail.append(detail)
        return self.__class__(new_not_ssl,
                              new_get_insecure,
                              new_web_view_client,
                              new_vulnerable_x509_certificate,
                              new_detail)
