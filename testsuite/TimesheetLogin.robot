*** Settings ***
Documentation     A test suite with a single test for close timesheet tickets
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          ../Resource/aspire_trac.txt

*** Test Cases ***
Close Track tickets
    Open Browser To Trac Page
    Click Narvar Project
    Open My Tickets
    @{links}=   Print the href of the table
    Close All tickets   @{links}


Read the Ticket
    @{TrckTicket}=   Read this week ticket   Vinoth Progress.xlsx
    Open Browser To Trac Page
    Click Narvar Project
    Create All tickets   @{TrckTicket}

