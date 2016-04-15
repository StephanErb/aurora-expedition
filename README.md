# Aurora Expedition
This is a hands-on tutorial for Apache Aurora &amp; Apache Mesos. It was assembled for a [Meetup of DevOps Karlsruhe](http://www.meetup.com/DevOps-Karlsruhe-Meetup/events/229457000/).


Our goal:

* Install a single-node Aurora & Mesos cluster in a virtual machine
* Deploy a Python Flask service onto the cluster
* Monitor the service using Prometheus



## Cluster Setup

We want to use the [official Aurora vagrant setup](https://github.com/apache/aurora/blob/master/docs/getting-started/vagrant.md).  The provided single-node setup is not production grade, but should be more than sufficient for our small hands-on.

    git clone https://github.com/apache/aurora.git
    cd aurora
    git checkout rel/0.13.0   # latest release as of 15.04.2016
    vagrant up                # depending on your network speed this can take several minutes


If this goes as planned, the following [components](https://github.com/apache/aurora/blob/rel/0.13.0/docs/getting-started/overview.md#components) should be reachable locally:

* Aurora Scheduler: http://aurora.local:8081
* Mesos Master: http://aurora.local:5050

If this does not work as expected, see the [Troubleshooting guide](https://github.com/apache/aurora/blob/rel/0.13.0/docs/getting-started/vagrant.md#troubleshooting).


## Flask Example

We will have a short look at the simple Flask app that we want to use in the remainder of this tutorial:

    vagrant ssh

    git clone https://github.com/StephanErb/aurora-expedition
    cd aurora-expedition

    # install python prerequisites
    sudo apt-get install python-virtualenv

    # install app & it requirements
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pip install -e .

    # start the Flask app using Gunicorn as an HTTP server
    gunicorn toyserver.main:app --bind :8000


We can now check form outside of our Vagrant box that the server is running es expected:


    $ curl http://aurora.local:8000
    Hello World!


We are now ready to deploy that via Aurora


## Deplying the Flask Example using Apache Aurora


    aurora job create devcluster/www-data/devel/toyserver toyserver.aurora

## References

* Apache Aurora: https://aurora.apache.org/
* Apache Mesos: https://mesos.apache.org/
* Flask: http://flask.pocoo.org/
* Gunicorn: http://gunicorn.org/
