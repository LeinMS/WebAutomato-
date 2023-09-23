# Table Matcher

**TableMatcher** is a utility that assists in matching and converting columns of one table (the source table) to conform to the format and structure of another reference table (the template). By utilizing the OpenAI API, it automates the process of identifying which columns in the source table match those in the template, and it subsequently performs any necessary data conversions to ensure consistency.

## Prerequisites

- Python 3.x
- Libraries: openai, pandas, re, and argparse
- OpenAI API key

## How to Use

Ensure that you have all the required libraries installed. You can install them using:

```
pip install openai pandas argparse
```

To use the script, you need to provide paths to the source and template tables, the path where the matched table will be saved, 
and your OpenAI API key. Use the following command format:


```
python script_name.py --source path_to_source.csv --template path_to_template.csv --target path_to_save_matched.csv --api_key YOUR_OPENAI_API_KEY
```


# Features
Feature Extraction: The script first extracts features of the columns, including the data type (numeric, date, or categorical), range for numeric data, and date format for date columns.
Column Description: For every column, a description is generated to help with the matching process.
Column Matching: Using OpenAI, it matches the source columns with the template columns.
Data Conversion: If the source and template column data types or formats differ, the source data is converted to match the template.

# Caution
Using the OpenAI API might result in costs depending on your usage level. 
Ensure that you are aware of the rate limits and associated charges before running the script extensively.

# Known Limitations
Date columns in the source table are expected to be convertible to the format 'dd-mm-yyyy'. 
If they follow a different format, the conversion process might fail or produce unexpected results.

# Conclusion
TableMatcher streamlines the process of matching and converting table columns, making it easier to integrate data from different sources. 
Ensure you always review the matched table for accuracy and completeness after using the tool.
