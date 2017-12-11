Feature: Check the content written into the graph database

  @requires_access_to_graph_db @detailed_tests
  Scenario Outline: Check that all frequently used packages for the npm ecosystem are stored in the graph DB
    Given System is running
    When I ask Gremlin to find all versions of the package <package> in the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find at least <number> packages in the Gremlin response

     Examples: packages
         |package  | number |
         |sequence | 2 |
         |array-differ | 2 |
         |array-flatten | 2 |
         |array-map | 2 |
         |array-parallel | 2 |
         |array-reduce | 2 |
         |array-slice | 2 |
         |array-union | 2 |
         |array-uniq | 2 |
         |array-unique | 2 |
         |lodash | 2 |
         |lodash.assign | 2 |
         |lodash.assignin | 2 |
         |lodash._baseuniq | 2 |
         |lodash.bind | 2 |
         |lodash.camelcase | 1 |
         |lodash.clonedeep | 2 |
         |lodash.create | 2 |
         |lodash._createset | 2 |
         |lodash.debounce | 2 |
         |lodash.defaults | 2 |
         |lodash.filter | 2 |
         |lodash.findindex | 2 |
         |lodash.flatten | 2 |
         |lodash.foreach | 2 |
         |lodash.isplainobject | 2 |
         |lodash.mapvalues | 2 |
         |lodash.memoize | 1 |
         |lodash.mergewith | 2 |
         |lodash.once | 2 |
         |lodash.pick | 2 |
         |lodash._reescape | 2 |
         |lodash._reevaluate | 2 |
         |lodash._reinterpolate | 2 |
         |lodash.reject | 2 |
         |lodash._root | 2 |
         |lodash.some | 2 |
         |lodash.tail | 1 |
         |lodash.template | 2 |
         |lodash.union | 2 |
         |lodash.without | 2 |
         |npm | 2 |
         |underscore | 2 |

