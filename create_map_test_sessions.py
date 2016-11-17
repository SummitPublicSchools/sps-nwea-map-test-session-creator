import spsautomation as sps
import json
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

def create_map_testing_sessions():
    print('Loading Data...\n')
    # load login host and credentials
    nwea_config = sps.config_section_map("NWEA")
    host = nwea_config['admin_host']
    username = nwea_config['username']
    password = nwea_config['password']

    # load schools.json
    with open('schools.json') as data_file:
        schools_info = json.load(data_file)

    # load the proper test codes that we want to assign
    test_codes = {
        'math': nwea_config['math_test_option_value'],
        'reading': nwea_config['reading_test_option_value']
    }

    # load the testing term and year
    testing_term = nwea_config['testing_term']
    testing_year = nwea_config['testing_year']

    # create firefox selenium driver with 10 seconds of wait time
    print('Creating driver and logging into NWEA MAP Website...\n')
    driver = sps.configure_selenium(10)

    sps.login_to_nwea_selenium(driver, host, username, password)

    print('Creating Test Sessions...\n')
    # create the test sessions by school and by grade
    for school_key, school_value in schools_info.items():

        for test_code_key, test_code_value in test_codes.items():

            for grade in school_value['grades']:
                testSessionName = school_key + "_" + str(grade) + "_" + test_code_key + "_" + testing_term + str(testing_year)
                print(testSessionName)

                # go to 'Manage Test Sessions'
                driver.get("https://sps-admin.mapnwea.org/admin/supervisor/ManageTestSessions.seam")

                # click the button to make a new test session
                elem = driver.find_element_by_id('msf:setupNewSessionBtn')
                elem.click()

                # put curose in the schools drop down
                schoolSelect = Select(driver.find_element_by_id('formStudentSearch1:schoolDropDown'))

                schoolSelect.select_by_value(str(school_value['option_value']))

                time.sleep(1)
                gradesSelect = Select(driver.find_element_by_id('formStudentSearch1:gradeDropDown'))

                # select the grade
                gradesSelect.select_by_visible_text(str(grade))

                # hit the search button
                searchButton = driver.find_element_by_id('formStudentSearch1:btnSearch')
                searchButton.click()

                # add all of the students to the list
                time.sleep(2)   # wait for the DOM to be updated with the Student Search Modal, then click on search
                addStudentsButton = driver.find_element_by_id('ssf:btnAddToStudentList')
                addStudentsButton.click()

                # select all of these students
                time.sleep(2)
                selectAllStudentsButton = driver.find_element_by_id('slf:slTbl:selectAllInStudentList')
                selectAllStudentsButton.click()

                # wait for students to be selected
                time.sleep(5)

                # click assign test
                assignTestButton = driver.find_element_by_id('slf:slTbl:btnAssignTest')
                assignTestButton.click()

                # wait for the dialogue to load and the dom to update
                time.sleep(3)

                # select the appropriate test
                testSelect = Select(driver.find_element_by_id('at:testSelectionDropDown'))
                testSelect.select_by_value(str(test_code_value))

                # click the save session button
                elem = driver.find_element_by_id('at:assignTestOKBtn')
                elem.send_keys(Keys.RETURN)

                time.sleep(3)

                # click the 'Save Session' dialogue
                saveSessionButton = driver.find_element_by_id('slf:btnSaveSessionM')
                saveSessionButton.click()

                # wait until the Save Session Modal Comes Up - saveTestSessionFromManagedModalForm:testSessionName1
                time.sleep(3)
                testSessionNameTextBox = driver.find_element_by_id('saveTestSessionFromManagedModalForm:testSessionName1')
                testSessionNameTextBox.send_keys(testSessionName)

                saveAndExitButton = driver.find_element_by_id('saveTestSessionFromManagedModalForm:saveTestSessionFromManagedModalSaveBtn')
                saveAndExitButton.send_keys(Keys.RETURN)

                time.sleep(5)
    driver.close()

    print('All test sessions created!')


if __name__ == '__main__':

    if not sps.prompt_user_to_check_config_file('config.ini and schools.json'):
        sys.exit()
    else:
        print("Running Script - Press ctrl + c to abort\n")
        sps.load_config()
        create_map_testing_sessions()
