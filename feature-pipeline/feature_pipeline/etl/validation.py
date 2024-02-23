from great_expectations.core import ExpectationSuite, ExpectationConfiguration


def build_expectation_suite() -> ExpectationSuite:
    """
    Builder used to retrieve an instance of the validation expectation suite.
    """

    expectation_suite_weather_forecast = ExpectationSuite(
        expectation_suite_name="weather_forecast_suite"
    )

    # Columns.
    expectation_suite_weather_forecast.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list": [
                    "time",
                    "temperature_2m",
                    "rain"
                ]
            },
        )
    )
    expectation_suite_weather_forecast.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_column_count_to_equal", kwargs={"value": 3}
        )
    )

    # Time
    expectation_suite_weather_forecast.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "time"},
        )
    )

    # Rain
    expectation_suite_weather_forecast.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": "rain",
                "min_value": 0,
                "strict_min": False,
            },
        )
    ),
    expectation_suite_weather_forecast.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "rain"},
        )
    )

    return expectation_suite_weather_forecast