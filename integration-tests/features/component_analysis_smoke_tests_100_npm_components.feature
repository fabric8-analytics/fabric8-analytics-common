 Feature: Smoke tests for the component analysis REST API


  Scenario Outline: Check the component analysis REST API endpoint for 100 most popular NPM components
    Given System is running
    Given Three scale preview service is running
    When I wait 2 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key

     When I start component analyses <ecosystem>/<package>/<version> with user_key
     Then I should get 200 status code
      And I should receive a valid JSON response

     When I look at the component analysis duration
     Then I should see that the component analysis duration is less than 10 second

     When I look at recent component analysis
     Then I should receive JSON response containing the result key
      And I should find at least one analyzed package in the component analysis
      And I should find the package <package> from <ecosystem> ecosystem in the component analysis
      And I should find the component <package> version <version> from <ecosystem> ecosystem in the component analysis
      And I should find new recommended version in case the CVE is detected for an analyzed component
      And I should find CVE report in case the CVE is detected for an analyzed component

     Examples: EPV
     | ecosystem  | package             | version              |
     | npm        | lodash              | 4.17.15              | #1
     | npm        | request             | 2.88.0               | #2
     | npm        | chalk               | 2.4.2                | #3
     | npm        | commander           | 2.20.0               | #4
     | npm        | express             | 4.17.1               | #5
     | npm        | async               | 3.1.0                | #6
     | npm        | react               | 16.8.6               | #7
     | npm        | debug               | 4.1.1                | #8
     | npm        | underscore          | 1.9.1                | #9
     | npm        | bluebird            | 3.5.5                | #10
     | npm        | moment              | 2.24.0               | #11
     | npm        | fs-extra            | 8.1.0                | #12
     | npm        | react-dom           | 16.8.6               | #13
     | npm        | mkdirp              | 0.5.1                | #14
     | npm        | prop-types          | 15.7.2               | #15
     | npm        | colors              | 1.3.3                | #16
     | npm        | glob                | 7.1.4                | #17
     | npm        | body-parser         | 1.19.0               | #18
     | npm        | yargs               | 13.3.0               | #19
     | npm        | minimist            | 1.2.0                | #20
     | npm        | yeoman-generator    | 4.0.1                | #21
     | npm        | through2            | 3.0.1                | #22
     | npm        | jquery              | 3.4.1                | #23
     | npm        | babel-runtime       | 6.26.0               | #24
     | npm        | vue                 | 2.6.10               | #25
     | npm        | axios               | 0.19.0               | #26
     | npm        | webpack             | 4.39.1               | #27
     | npm        | inquirer            | 6.5.0                | #28
     | npm        | babel-core          | 6.26.3               | #29
     | npm        | rxjs                | 6.5.2                | #30
     | npm        | q                   | 1.5.1                | #31
     | npm        | uuid                | 3.3.2                | #32
     | npm        | cheerio             | 1.0.0-rc.3           | #33
     | npm        | classnames          | 2.2.6                | #34
     | npm        | gulp-util           | 3.0.8                | #35
     | npm        | tslib               | 1.10.0               | #36
     | npm        | semver              | 6.3.0                | #37
     | npm        | babel-loader        | 8.0.6                | #38
     | npm        | rimraf              | 2.6.3                | #39
     | npm        | shelljs             | 0.8.3                | #40
     | npm        | object-assign       | 4.1.1                | #41
     | npm        | gulp                | 4.0.2                | #42
     | npm        | core-js             | 3.1.4                | #43
     | npm        | zone.js             | 0.10.1               | #44
     | npm        | winston             | 3.2.1                | #45
     | npm        | yosay               | 2.0.2                | #46
     | npm        | js-yaml             | 3.13.1               | #47
     | npm        | coffee-script       | 1.12.7               | #48
     | npm        | css-loader          | 3.2.0                | #49
     | npm        | babel-preset-es2015 | 6.24.1               | #50
     | npm        | eslint              | 6.1.0                | #51
     | npm        | socket.io           | 2.2.0                | #52
     | npm        | ember-cli-babel     | 7.8.0                | #53
     | npm        | redux               | 4.0.4                | #54
     | npm        | handlebars          | 4.1.2                | #55
     | npm        | style-loader        | 1.0.0                | #56
     | npm        | mocha               | 6.2.0                | #57
     | npm        | babel-polyfill      | 6.26.0               | #58
     | npm        | superagent          | 5.1.0                | #59
     | npm        | ejs                 | 2.6.2                | #60
     | npm        | dotenv              | 8.0.0                | #61
     | npm        | optimist            | 0.6.1                | #62
     | npm        | mongodb             | 3.3.0-beta2          | #63
     | npm        | xml2js              | 0.4.19               | #64
     | npm        | co                  | 4.6.0                | #65
     | npm        | aws-sdk             | 2.504.0              | #66
     | npm        | file-loader         | 4.1.0                | #67
     | npm        | ws                  | 7.1.1                | #68
     | npm        | babel-eslint        | 10.0.2               | #69
     | npm        | chai                | 4.2.0                | #70
     | npm        | redis               | 2.8.0                | #71
     | npm        | mongoose            | 5.6.8                | #72
     | npm        | typescript          | 3.5.3                | #73
     | npm        | request-promise     | 4.2.4                | #74
     | npm        | path                | 0.12.7               | #75
     | npm        | react-redux         | 7.1.0                | #76
     | npm        | morgan              | 1.9.1                | #77
     | npm        | promise             | 8.0.3                | #78
     | npm        | ora                 | 3.4.0                | #79
     | npm        | ramda               | 0.26.1               | #80
     | npm        | node-fetch          | 2.6.0                | #81
     | npm        | autoprefixer        | 9.6.1                | #82
     | npm        | bootstrap           | 4.3.1                | #83
     | npm        | url-loader          | 2.1.0                | #84
     | npm        | webpack-dev-server  | 3.7.2                | #85
     | npm        | node-sass           | 4.12.0               | #86
     | npm        | cookie-parser       | 1.4.4                | #87
     | npm        | eslint-plugin-react | 7.14.3               | #88
     | npm        | extend              | 3.0.2                | #89
     | npm        | eslint-plugin-import | 2.18.2              | #90
     | npm        | babel-preset-react  | 6.24.1               | #91
     | npm        | mime                | 2.4.4                | #92
     | npm        | node-uuid           | 1.4.8                | #93
     | npm        | html-webpack-plugin | 3.2.0                | #94
     | npm        | chokidar            | 3.0.2                | #95
     | npm        | marked              | 0.7.0                | #96
     | npm        | postcss             | 7.0.17               | #97
     | npm        | extract-text-webpack-plugin | 3.0.2        | #98
     | npm        | less                | 3.9.0                | #99
     | npm        | meow                | 5.0.0                | #100
