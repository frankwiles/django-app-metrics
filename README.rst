
Django App Metrics
==================

django-app-metrics allows you to capture and report on various events in your
applications.  You simply define various named metrics and record when they
happen.  These might be certain events that may be immediatey useful, for
example 'New User Signups', 'Downloads', etc.

Or they might not prove useful until some point in the future.  But if you
begin recording them now you'll have great data later on if you do need it.

For example 'Total Items Sold' isn't an exciting number when you're just
launching when you only care about revenue, but being able to do a contest
for the 1 millionth sold item in the future you'll be glad you were tracking
it.

You then group these individual metrics into a MetricSet, where you define
how often you want an email report being sent, and to which User(s) it should
be sent.


TODO
----

    - Improve text and HTML templates to display trending data well
    - Create redis backend for collection and aggregation

