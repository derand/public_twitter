#Public Twitter

##INSTALL
###Libraries
For working application need libraries: [requests-oauth](https://github.com/maraujop/requests-oauth), [Requests](http://docs.python-requests.org/en/latest/) download and put sources to this directory. For Requests library I change *requests/packages/urllib3/connectionpool.py* and hard set ssl library constants like this:

        ssl_req_scheme = {
            'CERT_NONE': 0,     # ssl.CERT_NONE,
            'CERT_OPTIONAL': 1, # ssl.CERT_OPTIONAL,
            'CERT_REQUIRED': 2  # ssl.CERT_REQUIRED
        }

###Set twitter application and user
Rename *constants.py.template* to *constants.py*. Create your application on [dev.twitter.com](https://dev.twitter.com/apps) and fill consumer_key and consumer_secret at constants.py. Next you need authorise your twitter account with new twitter application and fill "user token" and "user secret" on constants.py file.

###Set GAE application name
On *app.yaml* file set name of GAE application.

-----

Working example you can found at [derand.net](http://public_twitter.derand.net).
