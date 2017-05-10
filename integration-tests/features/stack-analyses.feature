Feature: Stack Analyses API V1

  Scenario Outline: <text>
    Given System is running
    When I post a valid "<input file>" to api/v1/stack-analyses/
    And I get a valid request ID
    Then I get stack analyses response via api/v1/stack-analyses/
    And Response matches "<output file>"

    Examples: Test cases
      | text                                                                              | input file | output file  |
      | Request analysis for pom.xml with known and unknown packages                      | pom1.xml   | result1.json |
      | Request analysis for pom.xml which matches ref stack                              | pom2.xml   | result2.json |
      | Request analysis for pom.xml which is subset of ref stack                         | pom3.xml   | result3.json |
      | Request analysis for pom.xml which is subset of ref stack with version miss match | pom4.xml   | result4.json |
      | Request analysis for pom.xml with components not available in maven ref stack     | pom5.xml   | result5.json |