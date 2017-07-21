# Glossary

* **fabric8-analytics core**
  * Core services to provide detailed information about individual components and aggregated information about stack defined by ecosystem manifest file.
* **Ecosystem**
  * Language specific packaging and distribution format (f.e. npm, PyPi, RubyGems, Maven...).
* **Manifest File**
  * A file (or potentially set of files) describing a component or application and its dependencies (f.e. package.json, gemspec, pom.xml...).
* **(Celery) Worker**
  * A service monitoring a Celery task queue that performs data ingestion and/or normalization on a given artifact (see [workers](https://github.com/fabric8-analytics/fabric8-analytics-worker/tree/master/f8a_worker/workers)).
* **(Celery) Task**
  * A request placed on the Celery task queue and picked up by an instance of a worker subscribed to this queue. It's identified by UUID.
* **Selinon (Dispatcher)**
  * An implementation above Celery that helps us model Celery task flows in simple YAML configuration files (see [worker configurations](https://github.com/fabric8-analytics/fabric8-analytics-worker/tree/master/f8a_worker/dispatcher)).
* **Scan Results**
  * Data returned by a successfully finished task in a form of JSON. When collected it is stored under analysis document.
* **Analysis**
  * Collection of all scan results for a particular component. It is stored in RDS/PostgreSQL during analysis run, distributed to S3 and Graph database and after that returned to users of the system over API from the graph database.
* **Analysis Run**
  * A run of the defined Celery workers over a given component (identified by an ecosystem/name/version triplet). The resulting analysis data is stored when finished.
