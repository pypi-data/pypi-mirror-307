def test_init() -> None:
    import rlogging

    assert rlogging.__version__


def test_imports() -> None:
    import rlogging.extension  # noqa: F401
    import rlogging.integration  # noqa: F401
    import rlogging.logs  # noqa: F401
    import rlogging.prometheus  # noqa: F401
    import rlogging.sentry  # noqa: F401
    import rlogging.settings  # noqa: F401
    import rlogging.telemetry  # noqa: F401
    import rlogging.utils  # noqa: F401
