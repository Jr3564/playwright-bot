#!/usr/bin/env python3
from playwright.sync_api import Playwright, sync_playwright

import os
from os.path import join, dirname
from dotenv import load_dotenv
import csv
import sys


def run(playwright: Playwright, profile_links, credentials, timeout=5000):
    browser = playwright.chromium.launch(headless=False, timeout=timeout)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.linkedin.com/")



    page.locator("input[name=\"session_key\"]").click()
    page.locator("input[name=\"session_key\"]").fill(credentials.get('email'))

    page.locator("text=Senha Exibir >> [placeholder=\"\\ \"]").click()
    page.locator("text=Senha Exibir >> [placeholder=\"\\ \"]").fill(credentials.get('password'))

    with page.expect_navigation():
        page.locator("text=Entrar").nth(1).click()

    for profile in profile_links:
        newPage = context.new_page()
        newPage.goto(profile)
        newPage.close()

    context.close()
    browser.close()


def read_profiles_file(filename) -> list[str]:
    with open(filename) as file:
        file_data = csv.reader(file)
        header, *profiles = file_data

        if not len(profiles[0]):
            print('Profiles not found!')
            sys.exit()

        email_index = header.index('email')
        profile_links = [profile[email_index] for profile in profiles]

        return profile_links


def getCredentials() -> dict:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

    if not EMAIL or not PASSWORD:
        print('Credentials not found!')
        sys.exit()

    return {
        "email": EMAIL,
        "password": PASSWORD
    }


def getFilePath():
    file_path = sys.argv[-1]

    if not file_path:
        print('File path not found!')
        sys.exit()

    return file_path


with sync_playwright() as playwright:
    file_path = getFilePath()
    profiles = read_profiles_file(file_path)
    credentials = getCredentials()

    run(playwright, profiles, credentials)
