import os
import requests
from datetime import datetime as dt

from .consts import ENDPOINT, APP_KEY_ENV_VAR_NAME


class AppKeyError(Exception):
    pass


def trace_req_resp(app_key: str = None):
    """
    Wrap your Lambda entry point with this decorator, supplying your App key. Zigmond will then automatically
    trace requests and responses of your skill for you to analyze in the dashboard.

    :param app_key: Your Zigmond App Key as supplied by Verto Lab
    :return:
    """
    try:
        app_key_val = app_key if isinstance(app_key, str) else os.environ[APP_KEY_ENV_VAR_NAME]
    except KeyError:
        raise AppKeyError(f'You should either supply your app_key explicitly, or set the {APP_KEY_ENV_VAR_NAME} '
                          f'environment variable')

    def internal_trace(original_f):
        def trace_and_call_f(*args, **kwargs):
            should_report = False
            request, f_resp = None, None
            try:
                event, context = args[0], args[1]
                request = event.get('request')
                if request:
                    should_report = True
            except Exception as e:
                pass
            try:
                f_resp = original_f(*args, **kwargs)
                return f_resp
            finally:
                if should_report:
                    report = dict(request=request)
                    if f_resp:
                        report['response'] = f_resp
                        report['response_ts'] = dt.now().isoformat(timespec='seconds') + 'Z'
                    requests.post(ENDPOINT, json=report, headers={'X-Zigmond-App-Key': app_key_val})
        return trace_and_call_f

    if app_key is None or isinstance(app_key, str):
        return internal_trace
    else:
        return internal_trace(app_key)
