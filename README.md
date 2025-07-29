# Microsoft-Rewards-Bot

Microsoft Rewards (Bing Rewards) Bot - Completes searches and quizzes, written in Python! :raised_hands:

## Overview

This program automatically completes search requests and quizzes for Microsoft Rewards. Search terms are generated using the daily top searches from Google Trends' API.

The bot runs Selenium in headless mode for seamless deployment on a VPS and optimized performance on local machines. It also leverages Selenium’s user agent options to earn points across all three platforms: PC (Edge Browser), Mobile, and more.

## Features
- Completes PC, Edge browser, and mobile searches for Microsoft Rewards.
- Automates polls, quizzes (multiple-choice, click-and-drag, reorder), punch cards, and Explore dailies.
- Generates search terms using Google Trends' API for optimal results.
- Runs in headless mode for efficient, background operation.
- Supports unlimited accounts via JSON configuration.
- Uses randomized search speeds to simulate natural usage.
- Logs errors and info by default; DEBUG mode tracks executed commands and search terms.

## Requirements
- Python          		[3.9](https://www.python.org/downloads/)
- Requests        		2.27.1
- Selenium        		4.0.0b4
- pyotp           		2.6.0
- python-telegram-bot	13.7
- Chrome Browser  		(Up-to-date)

## Use

1.  Clone and navigate to repo (recommended) or download the latest [release](https://github.com/tmxkn1/Microsoft-Rewards-Bot/releases).
2.  Modify `options/login_cred.json.example` with your account names and passwords,
    remove `.example` from filename.
3.  If your account has 2-factor authentication (2FA) enabled, please follow [README-2FA](READMEs/README-2FA.md).
4.  Enter into cmd/terminal/shell: `python -m pip install -r requirements.txt`
5.  Enter into cmd/terminal/shell: `python ms_rewards.py --headless`.

## To Do

- High priority:
  - Quiz AutoComplete

## License

100% free to use and open source.

#### Credit

@AnthonyZJiang for the base idea which I updated to modern Microsoft Rewards