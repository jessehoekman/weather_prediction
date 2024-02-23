from great_expectations.core import ExpectationConfiguration, ExpectationSuite


def build_expectation_suite() -> ExpectationSuite:
    """Builder used to retrieve an instance of the validation expectation suite."""
    expectation_suite_weather_prediction = ExpectationSuite(
        expectation_suite_name="weather_prediction_suite",
    )

    # Columns.
    expectation_suite_weather_prediction.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list": [
                    "city",
                    "time",
                    "temperature",
                    "rainfall",
                ],
            },
        ),
    )
    expectation_suite_weather_prediction.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_column_count_to_equal",
            kwargs={"value": 4},
        ),
    )

    # Time
    expectation_suite_weather_prediction.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "time"},
        ),
    )

    # Rain
    (
        expectation_suite_weather_prediction.add_expectation(
            ExpectationConfiguration(
                expectation_type="expect_column_min_to_be_between",
                kwargs={
                    "column": "rainfall",
                    "min_value": 0,
                    "strict_min": False,
                },
            ),
        ),
    )
    expectation_suite_weather_prediction.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "rainfall"},
        ),
    )

    return expectation_suite_weather_prediction
