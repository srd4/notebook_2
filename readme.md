# Notebook App

This is basically a CRUD application for separating user statements into actionable (tasks) and the rest (ideas) to keep them organized in different container objects. The plan was to work on a simple and useful enough project that would increase my productivity while I went throw the dj4e lectures I learn Django, (and remembered Python) HTML, and CSS with.

It replaced a manual system that I was (not) using for separating ideas and tasks on several areas that I refer to as 'systems' which I use to organize myself and make progress on.

Inspired by todoist, GTD, and insight from many other software, people, media, and productivity methods.

## Models
- Container: Represents a container that holds items.
- Tag: Represents a tag that can be added to items.
- Item: Represents an individual item that can be added to a container and tagged.
- StatementVersion: Represents a version of the statement of an item.

# UI Demonstrations.

## Creating new item in a container.
![Alt Text 1](https://i.imgur.com/YcQKEOf.gif)

## Changing an item's tags.
![Alt Text 2](https://i.imgur.com/FBE8d3t.gif)

## Using the search bar.
![Alt Text 3](https://i.imgur.com/15o31eV.gif)

## Marking elements as done.
![Alt Text 4](https://i.imgur.com/gQ15fuV.gif)

## Features

The following is a list of features that Chat-gpt generated for me based on notebook app's database registry of completed tasks under my notebook 2.0 implementation and features containers (proofread by me):

- Create containers to hold actionable and non-actionable items.
- Use tags to categorize items
- Track when an item was last updated and how many times a container has been opened.
- Ability to collapse and expand containers
- Pre-filling forms with actionable or not when creating a new item.
- You can mark an item as done.
- A search bar for searching all items.
- A navigation menu.
- Displaying data about the number of active ideas in the containers view.
- Edit and delete buttons for containers within the container detail view.
- A toggle switch for marking items as done.
- Saving changes in done attribute of an item to the database without reloading the page.
- A time of completion attribute for items.
- User registration and login functionality.

## Built With
[![Language](https://img.shields.io/github/languages/count/srd4/notebook_2.svg)](https://github.com/srd4/notebook_2)
- Django
- Python
- Html
- CSS