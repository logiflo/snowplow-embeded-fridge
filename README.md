Embed Snowplow Micro to Fridge App
=======

# Index

- [Embed Snowplow Micro to Fridge App](#embed-snowplow-micro-to-fridge-app)
- [Index](#index)
- [About Embed Snowplow Micro to Fridge App](#about-embed-snowplow-micro-to-fridge-app)
- [How is the tracking embedded?](#how-is-the-tracking-embedded)
- [What's tracked?](#whats-tracked)
- [How to build](#how-to-build)
- [How to run](#how-to-run)
- [How to see the tracking data](#how-to-see-the-tracking-data)
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Future features](#future-features)
- [Bugs?](#bugs)
- [Honorable mentions](#honorable-mentions)

# About Embed Snowplow Micro to Fridge App

Fridge app is an open source application using django, which allows you to keep track of the groceries you have in the fridge as well as the ones that have run out. More info about this app can be found [here](https://github.com/logiflo/fridge-django).

In addition, Snowplow Micro is used to track the user and the way they engage with the application.

The project is structured as follow:

- fridge_web: Django fridge webapp.
  - fridge: Project’s connection with Django.
  - my_fridge: Fridge views.
  - users: User views.
  - Dockerfile: The docker file descriptor of the webapp.
  - manage.py: Django manager script.
  - requirements.txt: The Python modules used in the project.
- micro: Snowplow configuration folder.
- docker-compose.yml: The docker compose file descriptor of the services.

Version: 2.0.0 - Released: 29th May 2021

# How is the tracking embedded?

As the application is in Django, the Snowplow Python tracker is selected and installed locally, following the documentation provided by Snowplow.

After installation, the module is imported and the tracker is initialized inside the views.py file.

# What's tracked?

Thanks to Snowplow Micro and its pre-defined events and associated methods for tracking, I have tracked every page view of the fridge view using `track_page_view()`. In addition, the log out is also tracked using the pre-defined `track_link_click()`.

# How to build

Once the repo is cloned, it is required to create a file named `.env` at `fridge_web/fridge`. That file must contain the **SECRET_KEY** and **DATABASE_URL**; an example can be shown below:

```
SECRET_KEY=j6)1zc)bx230q^!9!@9wmfz6x!+d695iphyx%y-$tf5uf-f7b!
DATABASE_URL=sqlite:///db.sqlite3
```

# How to run

The application can be build and run using docker. For it we need to run
the next commands (following the previous section example):

```bash
docker compose up
```

This will launch two services:

- my_fridge: The Django service that host the fridge webapp.
- micro: The snowplow micro service that listens for tracking data from fridge application.

# How to see the tracking data

The tracking data can be seen at the folowing urls:
- `<webapp_url>/micro/all`:
Get a summary with the number of good and bad events currently in the cache.
- `<webapp_url>/micro/good`:
Query the good events (events that have been successfully validated).
- `<webapp_url>/micro/bad`: Query the bad events (events that failed validation).
- `<webapp_url>/micro/reset`: Delete all events from the cache.

More detailed information can be found [here](https://github.com/snowplow-incubator/snowplow-micro).
# Requirements

- Python 3.6 or above.


# Dependencies

See `requirements.txt` file at `fridge_web/`.

# Future features

- Track every click of the application, not just the logout click.
- Track when a grocery is added or removed.

# Bugs?

Please add them to the [Issue Tracker][issues] with as much info as possible, especially source code demonstrating the issue.

# Honorable mentions

- [Snowplow](https://snowplowanalytics.com/) for its open source version of [Snowplow Micro](https://github.com/snowplow-incubator/snowplow-micro), which is a small version of a full Snowplow data collection pipeline, used for testing purposes. It has only the collection and validation steps, holding events in memory rather than a data store.

[issues]: https://github.com/logiflo/snowplow-embeded-fridge/issues