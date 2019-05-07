# Route Manager

## Overview

This Django-based webapp is a re-implementation of a workflow manager I used at a previous employer. Their design and implementation was horrible. While in my HCI class, we were given an open ended project and this immediately came to mind.

## Function

To understand what I built you must understand what the previous system's purpose was. At my previous job the deliverable were routes. A route is a section of road, somewhere in the US, that was driving using LIDAR cameras. After a route was collected it would have to go through the four stages of processing before it could be delivered (WF1 - WF3 and QC). The workflow manager they used was simple desktop application that was full of bugs that made it very difficult to use. Also the UI, was far from intuitive. Sometimes the word _Submit_ would mean different things or it would simply not update the changes on the database. If the person who created the routes made any mistakes, they had to write complex UPDATE statements directly on the database to make changes. These are just a few of the problems that I wanted to fix in my implementation.

## Goals

The goals for the project, as listed on the documentation, were as follows:

>Prototype an interface, with a focus on design/usability (not on functionality)
>Can either remake an existing interface or imagine a new one.
>Focus on five pieces of functionality you want to prototype.

In my original project proposal to my professor I posed these five pieces of functionality:

* A simple UI for adding routes one-by-one
* A way to upload a CSV for bulk uploads of routes
* A way for Project Managers to update routes simply without using messy SQL
* An intuitive UI for the processors and QC
* A way for processors to add notes to routes

In my current implementation, I have completed all of these except the CSV upload (which is a WIP), but I have added a lot of extra functionality in terms of Users. For my system to be complete to my stantards I will need to add the following pieces of functionality:

* A way to upload a CSV for bulk uploads of routes
* A User homepage for viewing currently active routes
* Ability to mark routes that have errors


