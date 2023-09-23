import argparse
import openai
import pandas as pd
import re

class TableMatcher:
    def __init__(self, template_path, source_path, api_key):
        # Load the template and source tables into pandas dataframes
        self.template = pd.read_csv(template_path)
        self.source = pd.read_csv(source_path)
        # Set the OpenAI API key
        openai.api_key = api_key

    @staticmethod
    def extract_table_features(table_df):
        # Initialize dictionaries to hold column types, date formats, and numeric ranges
        column_types = {}
        date_formats = {}
        numeric_ranges = {}

        # Loop through columns and determine their data type and other features
        for col in table_df.columns:
            if table_df[col].dtype in ['int64', 'float64']:
                column_types[col] = 'numeric'
                numeric_ranges[col] = (table_df[col].min(), table_df[col].max())
            else:
                try:
                    datetime_col = pd.to_datetime(table_df[col])
                    column_types[col] = 'date'
                    date_formats[col] = datetime_col.dt.strftime('%d-%m-%Y').iloc[0]
                except:
                    column_types[col] = 'categorical'

        features = {
            'column_types': column_types,
            'date_formats': date_formats,
            'numeric_ranges': numeric_ranges,
        }

        return features

    @staticmethod
    def describe_column(name, features):
        # Generate a description for each column based on its features
        desc = f"Column '{name}' is of type {features['column_types'][name]}."
        if features['column_types'][name] == 'date':
            desc += f" Date format is {features['date_formats'][name]}."
        elif features['column_types'][name] == 'numeric':
            desc += f" Values range from {features['numeric_ranges'][name][0]} to {features['numeric_ranges'][name][1]}."
        return desc

    def match_columns(self, template_col, template_desc, source_desc):
        # Use OpenAI to find the best match between the template and source columns
        prompt = f"For the template column named '{template_col}' which is described as: {template_desc}. Which column from the source {source_desc} best matches it?"
        response = openai.Completion.create(model="text-davinci-002", prompt=prompt, max_tokens=100)

        return response.choices[0].text.strip()

    @staticmethod
    def extract_column_name(description, columns_list):
        # Extract the column name from the description using regex
        column_name_matches = re.findall(r"'(.*?)'", description)
        for column_name in column_name_matches:
            if column_name in columns_list:
                return column_name
        else:
            return None

    @staticmethod
    def convert_and_match_format(source_df, template_df, mappings):
        # Convert source columns to the format specified in the template
        for template_col, source_col in mappings.items():
            if template_df[template_col].dtype == 'object' and source_df[source_col].dtype == 'object':
                try:
                    template_format = pd.to_datetime(template_df[template_col].dropna().iloc[0]).strftime('%d-%m-%Y')
                    source_df[source_col] = pd.to_datetime(source_df[source_col]).dt.strftime(template_format)
                except Exception as e:
                    print(f"Error converting {source_col}: {e}")

        source_df = source_df[list(mappings.values())]
        source_df.columns = list(mappings.keys())

        return source_df

    def get_matched_table(self):
        # Extract features from the template and source tables
        table_A_features = self.extract_table_features(self.source)
        template_features = self.extract_table_features(self.template)

        # Generate descriptions for each column based on its features
        template_descriptions = {col: self.describe_column(col, template_features) for col in template_features['column_types']}
        source_descriptions = {col: self.describe_column(col, table_A_features) for col in table_A_features['column_types']}

        column_mappings = {}
        # Map the columns of the source table to the template table
        for t_col, t_desc in template_descriptions.items():
            best_match = self.match_columns(t_desc, '\n'.join(source_descriptions.values()), source_descriptions)
            column_mappings[t_col] = best_match

        for key, value in column_mappings.items():
            column_mappings[key] = self.extract_column_name(value, self.source.columns)

        # Convert the formats of source columns to match the template and return the converted table
        converted_source = self.convert_and_match_format(self.source, self.template, column_mappings)

        return converted_source
