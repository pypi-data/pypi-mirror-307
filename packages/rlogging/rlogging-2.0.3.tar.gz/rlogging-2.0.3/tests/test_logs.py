from rlogging.logs import generate_logging_dict, logging_setup


def test_logging_setup():
    logging_setup()


def test_generate_logging_dict():
    assert isinstance(generate_logging_dict(), dict)
