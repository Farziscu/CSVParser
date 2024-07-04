"""Parse CSV file for weight info"""

import parse
import views

"""step1: prepare csv file"""
parse.manage_file()

parse.weekly_group()
parse.monthly_group()

"""step2: elaborate data"""

"""step3: display data"""
views.main_views()
