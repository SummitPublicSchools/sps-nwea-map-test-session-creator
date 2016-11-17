![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# SPS NWEA MAP Test Session Creator
> Additional information or tagline

This is a fairly straight-forward tool built in Python on the simple
sps-automation library that uses Selenium is used in order to create NWEA MAP
testing sessions in Firefox through the NWEA admin website based on school and
grade.

## Installing / Getting started

To use this project, complete the following steps:
1. Download or clone the project to your computer.
2. Use pip to install the following dependencies:
  * psycopg2
  * bs4
  * selenium
3. Edit the `config-default.ini` file to include your own settings. Rename it to `config.ini`.
4. Edit the `schools.json` file to include the grades tested at the school and
the option codes in the HTML associated with each school. More on this below.
5. Run the script!

```shell
git clone https://github.com/SummitPublicSchools/sps-nwea-map-test-session-creator
cd sps-nwea-map-test-session-creator/
python create_map_testing_sessions.py
```

## Developing

Here's a brief intro about what a developer must do in order to start developing
the project further:

```shell
git clone https://github.com/SummitPublicSchools/sps-nwea-map-test-session-creator
cd sps-nwea-map-test-session-creator/
```

#### Ideas for Future Development
Here are some thoughts that I've had about future features (some of which are
painfully obvious, but just haven't been worth the development time):
* In the case of a failure mid-run, create a way for script to pick up where it
left off the next time it is run.
* Have it output a file of the test sessions that it created during a run
* Create a way to make test sessions for a list of students or a list of classes.

## Features

This is a pretty straight-forward script. The only real features are as follows:
* Set the schools and grades you want to automatically create MAP testing sessions for
* Select the tests that you want to create MAP testing sessions for

## Configuration

Configuration is carried out only in a config file and a JSON file. You should
not have to modify the actual python code in order to make this tool work. there
is, however, an important concept that needs to be touched on to set up these
config files.

### Selecting Options in Drop Down Menus Using Selenium
This is the most time-consuming part of set-up. Most drop down menus make their
selections on the back end by indicating the user's choice with some sort of
(usually numeric) option value. To have Selenium correctly select the options
you want, you need to make sure that you have input the correct option values into
the config.ini and schools.json files. To do this, take the following steps:
1. Log in to the NWEA admin interface using Chrome or Firefox
2. Find the dropdown for which you need option values. Right click it and select
'Inspect' or similar. This will open the developers console and highlight the
HTML for the dropdown Select element.
3. Click the arrow to expand the contents of the select. If you scroll down a
bit you will see the options, along with their values. Copy and past the appropriate
value into the config.ini or schools.json folder.

You will need to find option values for the following dropdown menus:
* In the 'Find Students' area at the top of 'Manage Test Sessions' Screen
  * School
* In the 'Assign Now' option for assigning students a certain test
  * Test Name

See the GIF below for an example of finding the option value for a school.


#### config.ini
The following provides more information about the settings in the different config.ini file sections.

##### General
* `dex_output_dir`: Currently unused.

##### NWEA
* `admin_host`: The URL for your NWEA admin instance.
* `api_host`: The API URL for NWEA. Not needed for this tool.
* `username`: The username for the NWEA admin account with the Proctor role that
will be used to create the testing sessions.
* `password`: The password for the above account.
* `math_test_option_value`
* `reading_test_option_value`
* `testing_term`: The current testing term. This is used for making the test session names.
* `testing_year`: The current testing year. This is used for making the test session names.
* `dex_path`: This is not used for this tool.

#### schools.json
This file essentially lays out a dictionary data structure that will be used to
make each of the testing sessions (by grade in each school). It is important
because the structure of this file dictates which and how many test sessions
will be created.

Let's take a look at a single example:
```json
"everest": {"option_value": 1040, "grades": [9, 10]}
```

* `everest` is the school name and will be used in creating the test session name
* `option_value` is the option value for the Schools dropdown menu option pertaining to that school (see above).
* `grades[]` is a comma-separated list of the grades that will be tested at a particular school

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Licensing

The code in this project is licensed under MIT license.
