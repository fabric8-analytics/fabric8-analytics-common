# Contributing to Bayesian

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines (not rules) for contributing to Bayesian,
which is hosted in the [Bayesian Organization](https://github.com/baytemp/) on Github.
These are just guidelines, not rules, use your best judgment and feel free to
propose changes to this document in a pull request.

## Submitting Issues

* You can create an issue on any repo under [bayesian Github org](https://github.com/baytemp), include as many details as possible with your report
* Include the behavior you expected and maybe other places you've seen that behavior

## Submitting a Pull Request

*Note: Every PR requires at least one review from at least one of the Core Reviewers member.*

Core Reviewers are:

* Fridolin Pokorny <fridolin@redhat.com>
* Jiri Popelka <jpopelka@redhat.com>
* Michal Srb <msrb@redhat.com>
* Pavel Odvody <podvody@redhat.com>
* Slavek Kabrda <bkabrda@redhat.com>
* Tomas Hrcka <thrcka@redhat.com>

Before you submit your pull request consider the following guidelines:

* Fork the repository and clone your fork
* Make your changes in a new git branch:

     ```shell
     git checkout -b bug/my-fix-branch master
     ```

* Create your patch, **ideally including appropriate test cases**
* Include documentation that either describe a change to a behavior or the changed capability to an end user
* Commit your changes using **a descriptive commit message**. If you are fixing an issue please include something like 'this closes issue #xyz'
* Make sure your tests pass! We use Jenkins CI for our automated testing
* Push your branch to GitHub:

    ```shell
    git push origin bug/my-fix-branch
    ```

* When opening a pull request, select the `master` branch as a base.
* Mark your pull request with **[WIP]** (Work In Progress) to get feedback but prevent merging (e.g. [WIP] Update CONTRIBUTING.md)
* If we suggest changes then:
  * Make the required updates
  * Push changes to git (this will update your Pull Request):
    * You can add new commit
    * Or rebase your branch and force push to your Github repository:

    ```shell
    git rebase -i master
    git push -f origin bug/my-fix-branch
    ```

That's it! Thank you for your contribution!

### Merge Rules

* Include unit or integration tests for the capability you have implemented
* Include documentation for the capability you have implemented
* If you are fixing an issue, include the issue number you are fixing
* Python code should follow [PEP8](https://www.python.org/dev/peps/pep-0008/) conventions

## Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Reference issues and pull requests liberally

## Implementation details

### API

* Use hyphenation over underscore or camelCase (i.e. `/my-awesome-endpoint`)
* Any API change requires [RAML](http://raml.org/) documentation to be created or updated (otherwise the change will not be merged)
* Provide extensive examples for input and output
* Payload transferred over API should be in JSON format (exceptions are possible - for example while transferring files) and has to be documented with [JSON Schema](http://json-schema.org/) and [JSL](https://jsl.readthedocs.io/en/latest/tutorial.html), see existing schemas for [workers](https://github.com/baytemp/worker/tree/master/cucoslib/workers/schemas/) and [server](https://github.com/baytemp/server/tree/master/bayesian/schemas)

### Language

* Use Python 3 where possible with potential exceptions:
 * Ecosystem (Node.js, Ruby...) specific features which require parsing of the non-Python code
 * Specific use case where Python does not provide needed functionality, library, framework... - needs strong justification and approval from tech leads

### Deployment

* [OpenShift](https://www.openshift.com/) is our default and preferred way how to run Bayesian
* In case you are adding a new service make sure you provide a [Dockerfile](https://docs.docker.com/engine/reference/builder/) and [OpenShift configs](https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html)
