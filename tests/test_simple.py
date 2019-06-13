import zigmond


@zigmond.trace(app_key='MY_KEY')
def my_handler(event, context):
    pass


@zigmond.trace
def my_handler(event, context):
    pass


def test_success():
    assert True
