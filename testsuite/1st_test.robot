*** Settings ***
Documentation           This is a simple test with Robot Framework
Library                 Selenium2Library


*** Variables ***
${SERVER}               http://google.com
${BROWSER}              Firefox
${DELAY}                0


*** Keywords ***
Open Browser To Login Page
    Open Browser        ${SERVER}   ${BROWSER}
    Maximize Browser Window


*** Test Cases ***
Valid Login
    Open Browser To Login Page
    [Teardown]    Close Browser