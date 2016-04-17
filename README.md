# Aurora Expedition
This is a hands-on tutorial for Apache Aurora &amp; Apache Mesos. It was assembled for a [Meetup of DevOps Karlsruhe](http://www.meetup.com/DevOps-Karlsruhe-Meetup/events/229457000/).

Our goal:

* Install a single-node Aurora & Mesos cluster in a virtual machine.
* Deploy a Python Flask service onto the cluster.
* Play with the app using various APIs.


## Cluster Setup

We want to use the [official Aurora vagrant setup](https://github.com/apache/aurora/blob/master/docs/getting-started/vagrant.md).  The provided single-node setup is not production grade, but should be more than sufficient for our small hands-on.

    git clone https://github.com/apache/aurora.git
    cd aurora
    vagrant up  # depending on your network speed this can take several minutes


If this goes as planned, the following [components](https://github.com/apache/aurora/blob/rel/0.13.0/docs/getting-started/overview.md#components) should be reachable locally on `aurora.local` (`192.168.33.7`):

* Aurora Scheduler: http://aurora.local:8081
* Mesos Master: http://aurora.local:5050

If this does not work as expected, see the [Troubleshooting guide](https://github.com/apache/aurora/blob/rel/0.13.0/docs/getting-started/vagrant.md#troubleshooting).


## Flask Example

We will have a short look at the simple Flask app that we want to use in the remainder of this tutorial:

    vagrant ssh

    git clone https://github.com/StephanErb/aurora-expedition
    cd aurora-expedition

    # install python prerequisites
    sudo apt-get install python-virtualenv -y

    # install the example app
    virtualenv venv
    source venv/bin/activate
    pip install -e .

    # start the Flask app using Gunicorn as an HTTP server
    gunicorn toyserver.main:app --bind :8000


We can now check form outside of our Vagrant box that the server is running as expected:

    $ curl http://aurora.local:8000
    <html><head><title></title></head>
      <body>
        <pre>
         ______________
        < Hello World! >
         --------------
                \   ^__^
                 \  (oo)\_______
                    (__)\       )\/
                        ||----w |
                        ||     ||
        </pre>
      </body>
    </html>


Yeah! Now we are ready to deploy that via Aurora.


## Deployment using Apache Aurora

For the deployment, we will use the Aurora configuration bundled in the toyserver repository:

    vagrant ssh
    cd ~/aurora-expedition/deployment

    # inspect what we are going to deploy
    aurora job inspect devcluster/www-data/devel/toyserver toyserver.aurora

    # launch the job on the cluster
    aurora job create devcluster/www-data/devel/toyserver toyserver.aurora


We can view the job via the scheduler UI at http://aurora.local:8081/scheduler/www-data/devel/toyserver or by using the commandline client:

    $ aurora job status devcluster/www-data/devel/toyserver
    Active tasks (1):
        Task role: www-data, env: devel, name: toyserver, instance: 0, status: RUNNING on 192.168.33.7
          cpus: 1.0, ram: 32 MB, disk: 32 MB
          ports: {'http': 31584}
          failure count: 0 (max 1)
          events:
           2016-04-17 15:36:18 PENDING: None
           2016-04-17 15:36:18 ASSIGNED: None
           2016-04-17 15:36:21 STARTING: Initializing sandbox.
           2016-04-17 15:36:21 RUNNING: None


Our job has a single instance. We can send a HTTP request to this particular instance `0` using the built-in HTTP redirecting mechanism of Aurora (for production, we would use a proper load balancer instead):

    $ curl -L http://aurora.local:8081/mname/www-data/devel/toyserver/0
    <html><head><title></title></head>
      <body>
        <pre>
         ______________
        < Hello World! >
         --------------
                \   ^__^
                 \  (oo)\_______
                    (__)\       )\/
                        ||----w |
                        ||     ||
        </pre>
      </body>
    </html>



## Aurora Job updates

First of all, we want to add two additional instances to our job. We do this by telling Aurora to copy the configuration of instance `0`:

    $ aurora job add devcluster/www-data/devel/toyserver/0 2
    INFO] Adding 2 instances to devcluster/www-data/devel/toyserver using the task config of instance 0

Once the additional instances are running, we prepare an update of our job by changing the job configuration `toyserver.aurora`:

* change `instances = 1` to `intances = 3` in order to reflect our previous instance addition
* change the checksum of the installed code to `checksum = 75060f6455e80e44abdf597a6349a56f7f4d34e4`

We can now perform a rolling job update of all instances:

    # inspect the changes between deployed and local configuration
    aurora job diff devcluster/www-data/devel/toyserver toyserver.aurora

    # start rolling job update
    aurora update start devcluster/www-data/devel/toyserver toyserver.aurora

The status of the update can be checked via the Aurora update UI, or by looking at the HTML output of the individual instances:

* http://aurora.local:8081/mname/www-data/devel/toyserver/0
* http://aurora.local:8081/mname/www-data/devel/toyserver/1
* http://aurora.local:8081/mname/www-data/devel/toyserver/2

May the unicorns be with you!


## Mesos Inspection

Aurora is a Mesos framework. We can therefore extract various metrics about our running task instances from Mesos:

* Master state: `curl http://aurora.local:5050/master/state-summary | python -m json.tool` will return a summary of the entire Mesos cluster as seen by the master.
* Task metrics: `curl http://aurora.local:5051/monitor/statistics | python -m json.tool` will return the CPU and memory usage for each task on this particular slave.
* Failover Fun: `sudo stop mesos-slave` will disable the Mesos slave while all tasks continue to run. After a default timeout of 75 seconds, the Mesos master will consider all task instances to be `LOST` because it has lost connectivity with the slave. Aurora will try to reschedule them. Unfortunately, this won't work as we only have a single slave. Once we restart the slave using `sudo start mesos-slave`, the whole cluster state will reconcile.


## References

* Apache Aurora: https://aurora.apache.org/
* Apache Mesos: https://mesos.apache.org/
* Flask: http://flask.pocoo.org/
* Gunicorn: http://gunicorn.org/
