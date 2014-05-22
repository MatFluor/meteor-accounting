meteor-accounting
=================

Simple accounting software written in python with PySide and sqlite3.

This accounting software aims to be:
* reliable
* stable
* portable

Meteor-accounting is intended for bookkeeping and basic accounting in a small business or for a private perosn who does accounting for a small business. It is (atm) *only* a simple accounting software, so no interaction with your bank or more advances stuff.

### FAQ
#### What do you mean by protable?
What **portable** means is that you don't need to go through some installation process, so just download the release for your OS and you're ready to go!

#### Where are the files (meaning the databases)?
The Databases are per default made where your executable resides, on the same level (I might change that later on).

#### Do I need Python or the other fancy stuff installed on my machine?
No, that's what portable means too - no dependencies on your side.

#### Is it reliable? If I loose the data I'm screwed!
meteor-accounting works with the SQLite3 Database engine in it's background - every transaction is written into the database when you do it - so no manuel _Save_ is necessary. **But this does not mean that a backup is useless!** A backup is a reliable way to make sure your data isn't lost in case of a crash or similar events.

#### A Backup sounds nice, do I need to always copy the file to my eg. USB stick by myself?
At the moment - yes. I'm working on a simple Backup mechanism, which always saves your database on a location of your choice. The location will then be visible as "backup path" in the program.

#### Nice thing - how much does it cost?
Since it's in development, it's completely free (but don't expect flawlessness). Once it's producton-ready, there might be a price on the compiled version - in one way or another. E.g. the software itself is free, but customization option will be paid. I'm not sure which model I will follow at the moment.



