from Selenium2Library import Selenium2Library
from selenium.webdriver.common.keys import Keys
from robot.api.deco import keyword
from xlrd import open_workbook
import time
import datetime
import xlrd
from Pojo.TracTicket import TracTicket
from selenium.webdriver.support.ui import Select
from GoogleDriveFile import ReadGoogleSheet

class WrapperMethod(Selenium2Library):
    @keyword('Open Seperate Browser')
    def open_seperate_browser(self,url):
        driver = self._current_browser();
        # open tab
        print("Inside 1")
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        print("Inside 2")
        time.sleep(2);
        for tab in driver.window_handles:
            driver.switch_to.window(tab)
            print("Window title ", driver.title)
            print("Window Current URL ", driver.current_url)
        driver.get(url)

    @keyword('Read this week ticket')
    def read_this_week_ticket(self,excel_id):
        #file = ReadGoogleSheet().get_spreadSheet()
        #book = open_workbook(file_contents=file.read())
        book = open_workbook("../Data/" + excel_id)
        sheet = book.sheet_by_name("Alert Ticket")
        TrackTickets =[]
        #Read the content of Alert Ticket
        for col_index in range(sheet.ncols):
            if(sheet.cell(1,col_index).value == 'QA Verified Date'):
                alert_ticket_QA_column = col_index
            elif(sheet.cell(1,col_index).value == 'Description'):
                alert_ticket_Description = col_index
            elif (sheet.cell(1, col_index).value == 'TICKET_ID'):
                alert_ticket_ticketID = col_index
            elif (sheet.cell(1, col_index).value == 'Priority'):
                alert_ticket_Priority = col_index
            elif (sheet.cell(1, col_index).value == 'Work Hours'):
                alert_ticket_WH = col_index
        print("WH",alert_ticket_WH)

        picklist =False;
        for row_index in xrange(2, sheet.nrows):
            picklist = False;
            for col_index in range(sheet.ncols):
                if col_index == alert_ticket_QA_column:
                    ticket_day = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row_index,col_index),
                                                  book.datemode))
                    today = datetime.datetime.today()
                    #first_day= today - datetime.timedelta(days=today.weekday())
                    #last_day = today + datetime.timedelta(days=-today.weekday()+5)
                    first_day= today - datetime.timedelta(days=today.weekday() + 7)
                    last_day = today + datetime.timedelta(days=-today.weekday()-2)
                    if(last_day.day < 8):
                        release = 1
                    elif(last_day.day < 15):
                        release = 2
                    elif (last_day.day < 22):
                        release = 3
                    else:
                        release = 4

                    if ticket_day  >= first_day and  ticket_day <= last_day:
                        print ("Exact date ",ticket_day.date())
                        picklist =True;
            if picklist:
               tractk = TracTicket(sheet.cell_value(row_index,alert_ticket_ticketID) + "-" + sheet.cell_value(row_index,alert_ticket_Description)
                                    , sheet.cell_value(row_index,alert_ticket_Priority), first_day.date(), last_day.date(), 6, release, 1, "vinoth.mahendira", sheet.cell_value(row_index,alert_ticket_WH), "Test Execution")
               TrackTickets.append(tractk)

        for item in TrackTickets:
            item.printDetails()

        return TrackTickets



    @keyword('Create Ticket')
    def create_ticket(self,tractk):
        driver = self._current_browser();
        select = Select(driver.find_element_by_id('field-type'))
        select.select_by_visible_text('Maintenance')
        driver.find_element_by_id('field-summary').send_keys(tractk.name)
        select = Select(driver.find_element_by_id('field-task_priority'))
        select.select_by_visible_text(tractk.priority)
        psd = driver.find_element_by_id('field-psd')
        driver.execute_script("arguments[0].value =arguments[1];",psd,tractk.plannedStart)
        ped = driver.find_element_by_id('field-ped')
        driver.execute_script("arguments[0].value =arguments[1];", ped, tractk.plannedEnd)
        driver.find_element_by_id('field-no_of_testc_pre').send_keys(tractk.noTestCase)
        driver.find_element_by_id('field-no_of_testc_passed').send_keys(tractk.noTestCase)
        driver.find_element_by_id('field-no_of_testc_exec').send_keys(tractk.noTestCase)
        select = Select(driver.find_element_by_id('field-release'))
        select.select_by_visible_text(tractk.release)
        select = Select(driver.find_element_by_id('field-product_version_feature'))
        select.select_by_visible_text(tractk.version)
        select = Select(driver.find_element_by_id('field-owner'))
        select.select_by_visible_text(tractk.owner)
        driver.find_element_by_xpath("//*[@value='Create ticket']").click()
        print("Title of the page ", driver.title)


