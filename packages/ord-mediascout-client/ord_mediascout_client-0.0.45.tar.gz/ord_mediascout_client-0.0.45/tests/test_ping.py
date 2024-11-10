def test_ping(client):
    assert client.ping()


def test_ping_auth(client):
    assert client.ping_auth()
