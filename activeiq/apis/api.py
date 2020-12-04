class PublicApi(object):

  def __init__(self, client, basepath=None):
    self._client = client

  def request(self, path=None, *args, **kwargs):
    path = path or []
    return self._client.request(path, *args, **kwargs)