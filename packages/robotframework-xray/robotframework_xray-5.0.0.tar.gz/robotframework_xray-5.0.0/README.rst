Robot Framework
===============

.. contents::
   :local:

Introduction
------------



Installation
------------

If you already have Python with `pip <https://pip.pypa.io>`_ installed,
you can simply run::

    pip install robotframework-xray

For more detailed installation instructions, including installing Python, see
`<INSTALL.rst>`__.

Example
-------

Below is a simple example test case for testing login to some system.

.. code:: robotframework

    *** Settings ***
    Documentation     A test suite with a single test for valid login.
    ...
    ...               This test has a workflow that is created using keywords in
    ...               the imported resource file.
    Library           Xray

    *** Test Cases ***
    Valid Login
        [Tags]    EXE-123
        Open Browser To Login Page
        Input Username    demo
        Input Password    mode
        Submit Credentials
        Welcome Page Should Be Open
        [Teardown]    Close Browser

Usage
-----

.. code:: robotframework

    *** Settings ***
    Library           Xray

It is necessary to set the following parameters in the system variables or in the .env file:

XRAY_DEBUG = false # true/false

PROJECT_KEY = XSE # Project Key

TEST_PLAN = XSE-58

XRAY_API = https://xray.cloud.getxray.app/api/v2

XRAY_CLIENT_ID = 52888E2E5516439A854E8CD0B3B012AB

XRAY_CLIENT_SECRET = f5830cd0e9253ff57a636f094566245265ffa9a05d1074f0eb4b19de17361b20

CUCUMBER_PATH = C:/Projetos/robotframework-xray

In Jira create an Xray Test and set the TEST-TYPE to Cucumber.