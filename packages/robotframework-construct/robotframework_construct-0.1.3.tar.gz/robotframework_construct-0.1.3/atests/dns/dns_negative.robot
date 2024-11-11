*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using dns as an example for both UDP and TCP.
Variables          dns_construct.py
Library            robotframework_construct
*** Test Cases ***
basic negative tests
    Run keyword and expect error   ValueError: Argument 'protocol' got value 'raw' that cannot be converted to Protocol: Protocol does not have member 'raw'. Available: 'TCP' and 'UDP'   Open raw connection to server `1.1.1.1´ on port `53´
