Feature: Smoke tests for the component analysis REST API


  Scenario Outline: Check the component analysis REST API endpoint for 100 most popular PyPi components
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token

     When I read <ecosystem>/<package>/<version> component analysis with authorization token
     Then I should get 200 status code
      And I should receive a valid JSON response

     When I look at the component analysis duration
     Then I should see that the component analysis duration is less than 10 second

     When I look at recent component analysis
     Then I should receive JSON response containing the result key
      And I should find at least one analyzed package in the component analysis
      And I should find the package <package> from <ecosystem> ecosystem in the component analysis
      And I should find the component <package> version <version> from <ecosystem> ecosystem in the component analysis
      And I should find new recommended version in case the CVE is detected for an analyzed component
      And I should find CVE report in case the CVE is detected for an analyzed component

     Examples: EPV
     | ecosystem  | package             | version              |
     | pypi       | pip                 | 19.2.1               | #1
     | pypi       | urllib3             | 1.25.3               | #2
     | pypi       | botocore            | 1.12.202             | #3
     | pypi       | six                 | 1.12.0               | #4
     | pypi       | python-dateutil     | 2.8.0                | #5
     | pypi       | s3transfer          | 0.2.1                | #6
     | pypi       | pyyaml              | 5.1.2                | #7
     | pypi       | docutils            | 0.15.2               | #8
     | pypi       | pyasn1              | 0.4.6                | #9
     | pypi       | requests            | 2.22.0               | #10
     | pypi       | setuptools          | 41.0.1               | #11
     | pypi       | jmespath            | 0.9.4                | #12
     | pypi       | certifi             | 2019.6.16            | #13
     | pypi       | awscli              | 1.16.212             | #14
     | pypi       | rsa                 | 4.0                  | #15
     | pypi       | futures             | 3.3.0                | #16
     | pypi       | idna                | 2.8                  | #17
     | pypi       | colorama            | 0.4.1                | #18
     | pypi       | wheel               | 0.33.4               | #19
     | pypi       | chardet             | 3.0.4                | #20
     | pypi       | simplejson          | 3.16.0               | #21
     | pypi       | boto3               | 1.9.202              | #22
     | pypi       | pytz                | 2019.2               | #23
     | pypi       | numpy               | 1.17.0               | #24
     | pypi       | cffi                | 1.12.3               | #25
     | pypi       | markupsafe          | 1.1.1                | #26
     | pypi       | cryptography        | 2.7                  | #27
     | pypi       | awscli-cwlogs       | 1.4.5                | #28
     | pypi       | jinja2              | 2.10.1               | #29
     | pypi       | pycparser           | 2.19                 | #30
     | pypi       | pbr                 | 5.4.2                | #31
     | pypi       | enum34              | 1.1.6                | #32
     | pypi       | protobuf            | 3.9.1                | #33
     | pypi       | asn1crypto          | 0.24.0               | #34
     | pypi       | ipaddress           | 1.0.22               | #35
     | pypi       | click               | 7.0                  | #36
     | pypi       | pytest              | 5.0.1                | #37
     | pypi       | attrs               | 19.1.0               | #38
     | pypi       | future              | 0.17.1               | #39
     | pypi       | decorator           | 4.4.0                | #40
     | pypi       | pyparsing           | 2.4.2                | #41
     | pypi       | pandas              | 0.25.0               | #42
     | pypi       | pytest-runner       | 5.1                  | #43
     | pypi       | pyasn1-modules      | 0.2.6                | #44
     | pypi       | werkzeug            | 0.15.5               | #45
     | pypi       | psutil              | 5.6.3                | #46
     | pypi       | virtualenv          | 16.7.2               | #47
     | pypi       | flask               | 1.1.1                | #48
     | pypi       | boto                | 2.49.0               | #49
     | pypi       | py                  | 1.8.0                | #50
     | pypi       | itsdangerous        | 1.1.0                | #51
     | pypi       | google-api-core     | 1.14.2               | #52
     | pypi       | coverage            | 4.5.4                | #53
     | pypi       | argparse            | 1.4.0                | #54
     | pypi       | setuptools-scm      | 3.3.3                | #55
     | pypi       | pluggy              | 0.12.0               | #56
     | pypi       | mock                | 3.0.5                | #57
     | pypi       | scipy               | 1.3.0                | #58
     | pypi       | grpcio              | 1.22.0               | #59
     | pypi       | pyopenssl           | 19.0.0               | #60
     | pypi       | google-cloud-core   | 1.0.3                | #61
     | pypi       | pygments            | 2.4.2                | #62
     | pypi       | jsonschema          | 3.0.2                | #63
     | pypi       | psycopg2            | 2.8.3                | #64
     | pypi       | scikit-learn        | 0.21.3               | #65
     | pypi       | more-itertools      | 7.2.0                | #66
     | pypi       | cachetools          | 3.1.1                | #67
     | pypi       | pillow              | 6.1.0                | #68
     | pypi       | lxml                | 4.4.0                | #69
     | pypi       | docopt              | 0.6.2                | #70
     | pypi       | google-auth         | 1.6.3                | #71
     | pypi       | funcsigs            | 1.0.2                | #72
     | pypi       | websocket-client    | 0.56.0               | #73
     | pypi       | httplib2            | 0.13.1               | #74
     | pypi       | oauth2client        | 4.1.3                | #75
     | pypi       | google-api-python-client | 1.7.10               | #76
     | pypi       | mccabe              | 0.6.1                | #77
     | pypi       | paramiko            | 2.6.0                | #78
     | pypi       | tornado             | 6.0.3                | #79
     | pypi       | ptyprocess          | 0.6.0                | #80
     | pypi       | pyjwt               | 1.7.1                | #81
     | pypi       | pexpect             | 4.7.0                | #82
     | pypi       | sqlalchemy          | 1.3.6                | #83
     | pypi       | matplotlib          | 3.1.1                | #84
     | pypi       | uritemplate         | 3.0.0                | #85
     | pypi       | wrapt               | 1.11.2               | #86
     | pypi       | bcrypt              | 3.1.7                | #87
     | pypi       | pycodestyle         | 2.5.0                | #88
     | pypi       | markdown            | 3.1.1                | #89
     | pypi       | google-resumable-media | 0.3.2                | #90
     | pypi       | oauthlib            | 3.1.0                | #91
     | pypi       | elasticsearch       | 7.0.2                | #92
     | pypi       | docker              | 4.0.2                | #93
     | pypi       | ipython             | 7.7.0                | #94
     | pypi       | docker-pycreds      | 0.4.0                | #95
     | pypi       | prompt-toolkit      | 2.0.9                | #96
     | pypi       | atomicwrites        | 1.3.0                | #97
     | pypi       | multidict           | 4.5.2                | #98
     | pypi       | pymysql             | 0.9.3                | #99
     | pypi       | redis               | 3.3.6                | #100
