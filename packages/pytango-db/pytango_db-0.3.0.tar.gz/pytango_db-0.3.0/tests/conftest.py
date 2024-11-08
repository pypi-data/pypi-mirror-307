import contextlib
import os
import subprocess
import sys
import time

import pytest
import tango


@pytest.fixture(scope="session")
def tango_databaseds():
    """
    This fixture expects there to be a "default" Tango database available at
    TANGO_HOST. Note that some modifications to the db will be done, basically
    adding a server with some devices. It is removed afterwards.
    """

    db = tango.Database()

    device = "test/dummy/1"
    dev_info = tango.DbDevInfo()
    dev_info.name = device
    dev_info._class = "Dummy"
    server = "Dummy/1"
    dev_info.server = server
    db.add_server(dev_info.server, dev_info, with_dserver=True)

    # Start our dummy device
    # Note: may not be needed, we don't communicate with any other device than the
    # database device itself. But we may want some realistic metadata in the DB.
    # Maybe remove later.
    path = os.path.abspath(os.path.dirname(__file__))
    dummy = subprocess.Popen(
        [sys.executable, f"{path}/dummy.py", "1"], stderr=subprocess.PIPE
    )
    waited = 0
    dt = 0.3
    while True:
        time.sleep(dt)
        waited += dt
        if dummy.poll() is not None:
            stderr = dummy.stderr.read().decode()
            print(stderr)
            raise RuntimeError(f"Dummy device stopped: {dummy.returncode}")
        try:
            proxy = tango.DeviceProxy(device, green_mode=tango.GreenMode.Synchronous)
            proxy.ping()
            if proxy.read_attribute("State").value == tango.DevState.RUNNING:
                break
        except tango.DevFailed as exc:
            if waited > 10:
                raise RuntimeError("Tired of waiting for device proxy...") from exc
        except AssertionError:
            pass

    yield

    # TODO ensure this happens also after failing tests?
    db.delete_server(server)

    # Clean up
    with contextlib.suppress(Exception):
        dummy.kill()


@pytest.fixture(scope="session")
def pytango_databaseds():
    """
    Sets up the pytango based database device for running tests.
    Starts with a 'vanilla' Tango DB and adds a dummy tango device.
    Some acrobatics to ensure that we're using a separate TANGO_HOST.
    """
    # TODO get a free port
    PYTANGO_HOST = "127.0.0.1:11000"
    try:
        databaseds = subprocess.Popen(
            [sys.executable, "-m", "databaseds.database", "2", "-v4"],
            stderr=subprocess.PIPE,
            env={
                "PYTANGO_DATABASE_NAME": ":memory:",  # Don't write db to disk
                "TANGO_HOST": PYTANGO_HOST,
            },
        )

        waited = 0
        dt = 0.3
        while True:
            time.sleep(dt)
            waited += dt
            if databaseds.poll() is not None:
                stderr = databaseds.stderr.read().decode()
                print("------------------STDERR------------------")
                print(stderr)
                print("------------------------------------------")
                raise RuntimeError(f"Database stopped: {databaseds.returncode}")
            try:
                host, port = PYTANGO_HOST.split(":")
                db = tango.Database(host, int(port))
                db.get_info()
                break
            except tango.DevFailed as exc:
                if waited > 10:
                    raise RuntimeError("Tired of waiting for database...") from exc
            except AssertionError:
                pass

        device = "test/dummy/1"
        dev_info = tango.DbDevInfo()
        dev_info.name = device
        dev_info._class = "Dummy"
        server = "Dummy/1"
        dev_info.server = server
        db.add_server(dev_info.server, dev_info, with_dserver=True)

        # Start our dummy device
        path = os.path.abspath(os.path.dirname(__file__))
        dummy = subprocess.Popen(
            [sys.executable, f"{path}/dummy.py", "1"],
            stderr=subprocess.PIPE,
            env={
                "TANGO_HOST": PYTANGO_HOST,
            },
        )
        waited = 0
        dt = 0.3
        while True:
            time.sleep(dt)
            waited += dt
            if dummy.poll() is not None:
                stderr = dummy.stderr.read().decode()
                print("------------------STDERR------------------")
                print(stderr)
                print("------------------------------------------")
                raise RuntimeError(f"Dummy device stopped: {dummy.returncode}")
            try:
                proxy = tango.DeviceProxy(
                    f"tango://{PYTANGO_HOST}/{device}",
                    green_mode=tango.GreenMode.Synchronous,
                )
                proxy.ping()
                if proxy.read_attribute("State").value == tango.DevState.RUNNING:
                    break
            except tango.DevFailed as exc:
                if waited > 10:
                    raise RuntimeError("Tired of waiting for device proxy...") from exc
            except AssertionError:
                pass

        yield PYTANGO_HOST

    finally:
        # Clean up
        try:
            dummy.kill()
            db.delete_server(server)
        except Exception:
            pass
        with contextlib.suppress(Exception):
            databaseds.kill()
