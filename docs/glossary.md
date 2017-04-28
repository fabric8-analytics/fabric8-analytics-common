# Glossary

* **Bayesian Core**
  * Core services to provide detailed information about individual components and aggregated information about stack defined by ecosystem manifest file.
* **Ecosystem**
  * Language specific packaging and distribution format (f.e. npm, PyPi, RubyGems, Maven...).
* **Manifest File**
  * A file (or potentially set of files) describing a component or application and its dependencies (f.e. package.json, gemspec, pom.xml...).
* **(Celery) Worker**
  * A service monitoring a Celery task queue that performs data ingestion and/or normalization on a given artifact (see [workers](https://github.com/fabric8-analytics/worker/tree/master/cucoslib/workers)).
* **(Celery) Task**
  * A request placed on the Celery task queue and picked up by an instance of a worker subscribed to this queue. It's identified by UUID.
* **Selinon (Dispatcher)**
  * An implementation above Celery that helps us model Celery task flows in simple YAML configuration foles (see [worker configurations](https://github.com/fabric8-analytics/worker/tree/master/cucoslib/dispatcher)).
* **Scan Results**
  * Data returned by a successfully finished task in a form of JSON. When collected it is stored under analysis document.
* **Analysis**
  * Collection of all scan results for a particular component. It is stored in database and returned to users of the system over API.
* **Analysis Run**
  * A run of the defined Celery workers over a given component (identified by an ecosystem/name/version triplet). The resulting analysis data is stored when finished.
