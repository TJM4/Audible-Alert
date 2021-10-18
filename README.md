# Audible Alert

## Introduction

This is a small Python scripts which will alert you via a Discord webhook whenever
any author you have selected posts a new audiobook to Audible. I made this script
as there is no way to do this natively on Audible and I found myself needing to
manually check a list of authors names to see if they had released any more books
in my favourite series.

## Setup

Firstly, clone the repo

``git clone https://github.com/TJM4/Audible-Alert``

Next, install the requirements

``pip install -r requirements.txt``

You can now create a config file. The wizard provides an easy way to do this. To get started run

``python generate_config.py``

You're now ready to run the script!

``python main.py``