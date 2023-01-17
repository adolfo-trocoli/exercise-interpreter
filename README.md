# exercise interpreter
> Small python script designed to quickly search through my exercise log file.

## Table of Contents
* [General Info](#general-information)
* [Functioning and usage](#functioning-and-usage)
* [Web deployment](#web-deployment)
* [File format](#file-format)
* [Setup](#setup)
* [Room for Improvement](#room-for-improvement)
* [Technologies Used](#technologies-used)
* [Project Status](#project-status)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)


## General Information
Python script designed to interpret personal logs of exercise and extract data from them using regular expressions. It was designed and developed from scratch for this purpose.

## Functioning and usage
The script needs to be called with an input file as an argument. It will then read and search for the different options specified.

\- Available options:

	-h, --help: shows help message
	-s, --search: search for the exercise in file and shows every occurrence
	-m, --month: shows the percentage of days trained in a certain month, month should be specified with format m/y
	-d, --day: show the whole day exercise, day should be specified with format d/m/y
	--pr: shows all personal records for a certain exercise
	-t, --total: shows total reps of a given exercise, requires -s to know what exercise to show

## Web deployment
This same script is also deployed in a [web-server](https://dev6981.d2qnjwwk6ymm5j.amplifyapp.com/). This was done to try some of the AWS services and get some experience on how to configure them. I will indicate the steps followed to deploy it at a high level. The files used to do this are under ./exercise_interpreter_web directory.
- First, I have modified slightly the script to be able to work as AWS Lambda, accepting the parameters as an event/context pair as needed for this kind of function.
- Then I created an API Gateway so it can accept POST method from web server and associated it with the lambda function.
- Lastly, I have set up a little script inside the html file so it detects the checked settings and sends the request to the API. This html file has been uploaded and deployed using AWS Amplify.

## File format
To be read by the program, the file needs to be written in a specific format. There is a sample file called "sample_file.txt" to demonstrate it.

	d/m/y [More text]
	<exercise> <series>x<reps> [ + <other_reps> ]

A short example would be the following:

	31/7/22 (Domingo)
	fondos 3x12
	flexiones 3x12
	elevaciones piernas paralelas 2x8 + 6

## Setup
The script is fully-working and ready to be downloaded.

## Room for Improvement
A lot of things could be improved but this was designed to be used by me so I just sketched a working version fast.

#### Technologies Used
- Python 3

#### Project Status
Project is complete. Any additions, comments, and requests are welcomed in the Issues page, which will be reviewed periodically.

#### Acknowledgements
This program was created for personal use and needs a very specific format in the exercise log that I use. The needed format is specified in the [file format](#file-format) section.

#### Contact
Created by [@adolfo-trocoli](github.com/adolfo-trocoli)
LinkedIn [profile](https://www.linkedin.com/in/adolfo-trocol%C3%AD-naranjo-a07250224)
