from Selenium2Library import Selenium2Library
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.api.deco import keyword
from xlrd import open_workbook
import time
import datetime
import xlrd
from Pojo.TracTicket import TracTicket
from selenium.webdriver.support.ui import Select
from GoogleDriveFile import ReadGoogleSheet
from selenium.webdriver.common.by import By
from decimal import *
from selenium import webdriver
import sys

class WrapperMethod(Selenium2Library):
    @keyword('Open Seperate Browser')
    def open_seperate_browser(self,url):
        driver = self._current_browser();
        # open tab
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
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
        TrackTickets = []
        sheet_names = {"Alert Ticket","Return Bug Ticket","TRACK","Other","Alert Bug"}
        #sheet_names = {  "Alert Bug"}
        for sheet in sheet_names:
            for item in self.create_track_tickets_list(sheet,book):
                TrackTickets.append(item)

        return TrackTickets



    @keyword('Create Ticket')
    def create_ticket(self,tractk):
        delay =10;
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
        if "Test Case Creation" in tractk.tasklist.keys():
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
        assert (tractk.name in driver.title)
        tractk.trac_id = driver.current_url.replace("https://prism.aspiresys.com/Narvar/ticket/", "")
        print("Trac id",tractk.trac_id)
        driver.find_element_by_id("estimatedhours-" + tractk.trac_id).click();
        WebDriverWait(driver,delay).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-labelledby='ui-dialog-title-estimated-hours-dialog-list'][contains(@style,'block')]")))
        for key in tractk.tasklist.keys():
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID,"#add-new")))
            driver.find_element_by_id("#add-new").click()
            WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,
                                                                                 "//div[@aria-labelledby='ui-dialog-title-estimated-hours-dialog-entry'][contains(@style,'block')]")))
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID,"timesheet_hours")))
            time = Decimal(tractk.tasklist[key])
            hour = int(time)
            minute = str(int((time-hour)*60)).zfill(2)
            driver.find_element_by_id("timesheet_hours").clear()
            driver.find_element_by_id("timesheet_hours").send_keys(str(hour))
            select = Select(driver.find_element_by_id('timesheet_minutes'))
            select.select_by_visible_text(minute)
            select = Select(driver.find_element_by_id('timesheet_reason'))
            select.select_by_visible_text(key)
            driver.find_element_by_id("timesheet_comments").send_keys(key)
            driver.find_element_by_id("save").click()
            WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//*[text()='"+ key.lower() +"']/following-sibling::*[text()='" + key + "']")))
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//a[.='close'][ancestor::div[contains(@style,'block')]]")))
        driver.find_element_by_xpath("//a[.='close'][ancestor::div[contains(@style,'block')]]").click()
        estimated_hour = driver.find_element_by_id("estimatedhours-" + tractk.trac_id).text
        print("Calculated Estimated Hour ", estimated_hour)
        assert (estimated_hour == (str(hour).zfill(2) + ":" + minute))

    @keyword('Go to saleforce')
    def new_click(self):
        driver = self._current_browser();
        driver.get("https://ssodisney--kanaqa.cs90.my.salesforce.com")
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                             "//em[@class='x-btn-split']")))
        element =  driver.find_element_by_xpath("//em[@class='x-btn-split']")
        print("x",element.location)
        print("x", element.location["x"])
        print("y", element.size)
        action = webdriver.ActionChains(driver)
        Xoffset = (element.size["width"] * 0.93);
        print Xoffset
        action.move_to_element_with_offset(element, 235, 0)
        action.click()
        action.perform()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                          "//ul/li[1]/input")))
        driver.find_element_by_xpath("//ul/li[1]/input").click()




    def create_track_tickets_list(self,sheet_name,book):
        sheet = book.sheet_by_name(sheet_name)
        TrackTickets = []
        # Read the content of Alert Ticket
        ticket_logged_date_col = 0
        print ("Open the sheet %s ", sheet_name)
        if sheet_name == "Other":
            for col_index in range(sheet.ncols):
                if (sheet.cell(1, col_index).value == 'Work Item'):
                    ticket_work_item_col = col_index
                elif (sheet.cell(1, col_index).value == 'Work'):
                    ticket_work_col = col_index
                elif (sheet.cell(1, col_index).value == 'Hour Spend'):
                    ticket_hour_spend_col = col_index
                elif (sheet.cell(1, col_index).value == "Date"):
                    ticket_logged_date_col = col_index
            picklist = False;
            for row_index in xrange(2, sheet.nrows):
                ticket_day = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row_index, ticket_logged_date_col),
                                                                     book.datemode))
                today = datetime.datetime.today()
                first_day = today - datetime.timedelta(days=today.weekday() + 7)
                last_day = today + datetime.timedelta(days=-today.weekday() - 2)
                if (last_day.day < 8):
                    release = 1
                elif (last_day.day < 15):
                    release = 2
                elif (last_day.day < 22):
                    release = 3
                else:
                    release = 4
                if ticket_day >= first_day and ticket_day <= last_day:
                    print ("Ticket date ", ticket_day.date())
                    picklist = True;
                workhour = str(sheet.cell_value(row_index, ticket_hour_spend_col))
                if picklist and workhour != "":
                    tracklist = {}
                    day_tracklist = {}
                    work = str(sheet.cell_value(row_index, ticket_work_col))
                    if len(workhour.split("\n")) != len(work.split("\n")):
                        print("Work %s & Hour spend not equal %s", work, workhour)
                        return TrackTickets
                    index = 0
                    worklist = work.split("\n")
                    for each_work in workhour.split("\n"):
                        tracklist[each_work] = worklist[index]
                        day_tracklist[each_work] = [ticket_day.date(),worklist[index]]
                        index += 1
                    tractk = TracTicket(
                        sheet.cell_value(row_index, ticket_work_item_col)
                        , "major", first_day.date(), last_day.date(), 0, release,
                        1, "vinoth.mahendira", tracklist,day_tracklist)
                    TrackTickets.append(tractk)
            for item in TrackTickets:
                item.printDetails()

            return TrackTickets

        for col_index in range(sheet.ncols):
            if (sheet.cell(1, col_index).value == 'QA Verified Date'):
                ticket_QA_column = col_index
            elif (sheet.cell(1, col_index).value == 'Description'):
                ticket_Description = col_index
            elif (sheet.cell(1, col_index).value == 'TICKET_ID'):
                ticket_ticketID = col_index
            elif (sheet.cell(1, col_index).value == 'Priority'):
                ticket_Priority = col_index
            elif (sheet.cell(1, col_index).value == 'Work'):
                ticket_Work = col_index
            elif (sheet.cell(1, col_index).value == 'Hour Spend'):
                ticket_hour_spend = col_index
            elif (sheet.cell(1, col_index).value == "Logged Date"):
                ticket_logged_date_col = col_index

        picklist = False;
        for row_index in xrange(2, sheet.nrows):
            picklist = False
            if sheet.cell_value(row_index, ticket_QA_column) == "" :
                continue
            try:
                ticket_day = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row_index, ticket_QA_column),
                                                                 book.datemode))
            except:
                print("Exception thrown on ticket %s : %s ",sheet.cell_value(row_index, ticket_ticketID),sys.exc_info()[0])
                continue

            today = datetime.datetime.today()
            # first_day= today - datetime.timedelta(days=today.weekday())
            # last_day = today + datetime.timedelta(days=-today.weekday()+5)
            first_day = today - datetime.timedelta(days=today.weekday() + 7)
            last_day = today + datetime.timedelta(days=-today.weekday() - 2)

            if ticket_day >= first_day and ticket_day <= last_day:
                picklist = True;
            if picklist == False and ticket_logged_date_col != 0:
                if sheet.cell_value(row_index, ticket_logged_date_col) == "":
                    continue
                try:
                    ticket_created_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row_index, ticket_logged_date_col),
                                                                 book.datemode))
                except:
                    print(
                    "Exception thrown on ticket %s : %s ", sheet.cell_value(row_index, ticket_ticketID), sys.exc_info()[0])
                    continue
                if ticket_created_date >= first_day and ticket_created_date <= last_day:
                    print ("Logged Date ", ticket_created_date.date())
                    picklist = True;
            workhour = str(sheet.cell_value(row_index, ticket_hour_spend))
            if picklist and workhour != "":
                if (last_day.day < 8):
                    release = 1
                elif (last_day.day < 15):
                    release = 2
                elif (last_day.day < 22):
                    release = 3
                else:
                    release = 4
                tracklist = {}
                day_tracklist ={}
                work = str(sheet.cell_value(row_index, ticket_Work))
                if len(workhour.split("\n")) !=  len(work.split("\n")):
                    print("Work %s & Hour spend not equal %s",work,workhour)
                    return TrackTickets
                index = 0
                worktime =workhour.split("\n")
                for each_work in work.split("\n"):
                    tracklist[each_work] = worktime[index]
                    if each_work == "Test Case Creation":
                        day_tracklist[each_work] = [ticket_created_date.date(), worktime[index]]
                    else:
                        day_tracklist[each_work] = [ticket_day.date(), worktime[index]]
                    index += 1
                tractk = TracTicket(sheet.cell_value(row_index, ticket_ticketID) + "-" + sheet.cell_value(row_index,ticket_Description)
                    , sheet.cell_value(row_index, ticket_Priority), first_day.date(), last_day.date(), 6, release,
                    1, "vinoth.mahendira", tracklist,day_tracklist)
                TrackTickets.append(tractk)
        for item in TrackTickets:
            item.printDetails()

        return TrackTickets

        @keyword('Click last week')
        def read_this_week_ticket(self, excel_id):
            # file = ReadGoogleSheet().get_spreadSheet()
            # book = open_workbook(file_contents=file.read())
            book = open_workbook("../Data/" + excel_id)
            TrackTickets = []
            sheet_names = {"Alert Ticket", "Return Bug Ticket", "TRACK", "Other", "Alert Bug"}
            # sheet_names = {  "Alert Bug"}
            for sheet in sheet_names:
                for item in self.create_track_tickets_list(sheet, book):
                    TrackTickets.append(item)

            return TrackTickets
