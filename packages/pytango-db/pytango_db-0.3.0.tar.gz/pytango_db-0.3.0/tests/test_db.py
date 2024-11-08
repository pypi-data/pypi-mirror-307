import tango


def test_get_info(pytango_databaseds):
    db = tango.Database()
    info = db.get_info()
    assert info.startswith("TANGO Database")
