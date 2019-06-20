# Zigmond Python SDK

## Installation

In your `requirements.txt` file add the following line:
>git+https://github.com/vertolab/zigmond-python.git#zigmond

Then `pip install -r requirements.txt`

## Usage

Assuming your Lambda Handler as defined in the AWS Lambda console is `my_module.my_func`, simply wrap it with Zigmond
and you should be good to go:
```python
import zigmond


@zigmond.trace(app_key='YOUR_APP_KEY')
def my_func(event, context):
    # handle the event
    return {}
 ```
 
To better protect your App Key, consider using Lambda's support of environment variables to store your key. Zigmond
will look for an App Key in the environment variable `ZIGMOND_APP_KEY` if no key is supplied explicitly:
```python
import zigmond
 
 
@zigmond.trace()
def my_func(event, context):
   pass
   # ...
``` 
