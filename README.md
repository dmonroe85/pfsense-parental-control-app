# PFSense Parental Controls

This is a collection of applicatons used to enable dynamic parental controls
with the PFsense open-source router.  I wanted a flexible parental control
system that was easy to use, cheap, and reliable.  Nothing I found met all of
those requirements, so I built my own.

The current state of this is a little cumbersome; parts of the system take
advantage of AWS free tier to give me a simple persistence layer, but in
reality it could be done without that.  Honestly, I just wanted to play with
the serverless framework.  In a future version of this, I will probably remove
that.

## TODO

* Specify run instructions and configuration in each module
* Swappable backends
* Local override persistence

