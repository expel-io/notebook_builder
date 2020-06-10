import functools
import os
import re

import ipywidgets as widgets
import numpy as np
import pandas as pd
import qgrid
from IPython.display import display
from IPython.display import Javascript
from IPython.display import Markdown
from ipywidgets import fixed
from ipywidgets import interact
from ipywidgets import interact_manual
from ipywidgets import interactive
from ipywidgets import Layout


def downselect(f):
    """This is a decorator run before each downselect to catch any errors and display the downselect methods
    output. This can be configured to log and/or report an error reporting tool like Sentry."""

    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        if os.getenv('TESTING') is not None:
            # Skipping decortor logic
            return f(self, *args, **kwargs)
        else:
            try:
                result = f(self, *args, **kwargs)
                if type(result) == pd.DataFrame:
                    if result.empty or len(result.index) < 1:
                        return display(Markdown('**No results returned**'))
                    else:
                        return display(qgrid.show_grid(result, show_toolbar=True))
                elif type(result) == None:
                    return display(Markdown('**No results returned**'))
                else:
                    return result
            except Exception as e:
                display(Markdown(f'An error has been reported: <span style="color:red">{e}</span>'))
                pass  # Error reporting can be configured here!
    return wrap


class Downselects:
    """This class is responsible for providing necessary values for downselect functions.

    Args:
        hunt_data_df (dataframe): original hunt data

    Attributes:
        df (dataframe): original hunt data

    """

    def __init__(self, hunt_data_df):
        self.df = hunt_data_df

    def get_df(self, df=None):
        """Returns the hunt_data dataframe otherwise a passed in dataframe."""

        if df is not None:
            return df
        else:
            return self.df.copy()

    @downselect
    def general_frequency_trend(self, groupby, uniqued, df=None):
        """Returns a dataframe of unique 'groupby' values and the frequency of the 'uniqued' column

        Args:
            groupby (list): Columns to group the dataframe records by
            uniqued (str): Column to get unique count of
            df (dataframe): passed in dataframe to run this downselect on

        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        return df.groupby(groupby).nunique()[[uniqued]].rename(columns={uniqued: 'count'})

    @downselect
    def column_frequency_count(self, column, df=None):
        """Returns a dataframe of unique instances of 'column' values and their frequencies

        Args:
            column (str): The column to unique on
            df (dataframe): passed in dataframe to run this downselect on

        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        tmpdf = df.groupby([column]).size().reset_index(name='count')
        return tmpdf.sort_values(by=['count'], ascending=False).reset_index(drop=True)

    @downselect
    def column_group(self, column_list, sort_by, df=None):
        """Returns a dataframe grouped by 'column_list' and sorted by 'sort_by'

        Args:
            column_list (list): The columns to group by
            sort_by (str): Column to sort by
            df (dataframe): passed in dataframe to run this downselect on

        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        tmpdf = df[column_list].drop_duplicates()
        return tmpdf.sort_values(by=[sort_by], ascending=False).reset_index(drop=True)

    @downselect
    def spread_counts_report(self, search_list, field_list, df=None):
        """Display a spread counts report an item in 'search_list'

        Args:
            search_list (list): columns to apply spread counts on
            field_list (list): columns to report within the resulting dataframe
            df (dataframe): passed in dataframe to run this downselect on

        Returns:
            Returns result as Markdown
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        tmpdf = df[field_list].copy()
        tmpdf[field_list] = tmpdf[field_list].astype(str).fillna(value='-')
        tmpdf.reset_index(drop=True)

        def spread_counts_helper(field, temp_frame):
            def x(cnt): return "is" if cnt == 1 else "are"
            def y(cnt): return " " if cnt == 1 else "s "
            def z(cnt): return " " if cnt == 1 else "es "
            try:
                if field == 'process_hash':
                    hash_exe_pat = temp_frame.copy()
                    hash_exe_pat = hash_exe_pat.drop_duplicates(
                        subset='process_hash', keep='first').set_index('process_hash', drop=False)
                    phash_list = temp_frame.process_hash.unique().tolist()

                    output = ""

                    output += '## Process Hash\n\n'
                    lph = len(phash_list)
                    output += f'There {x(lph)} {lph} unique process hash{z(lph)}associated with your search.\n\n'
                    h_head = '| Unique Process Hash{z{lph}}| Count in Hunt Data | Engine Hits | Engines Total | Detected By | Detected As |\n| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |\n'

                    for h in phash_list:
                        h_cnt = df.loc[df.process_hash == h, 'process_hash'].count()
                        hit = hash_exe_pat.loc[h, 'engines_hit']
                        etl = hash_exe_pat.loc[h, 'engines_total']
                        dby = hash_exe_pat.loc[h, 'detected_by']
                        das = hash_exe_pat.loc[h, 'detected_as']

                        h_md = f'| {h} | {h_cnt} | {str(hit)} | {str(etl)} | {str(dby)} | {str(das)} |\n'
                        h_head += h_md
                    output += h_head
                    return output

                else:
                    uniq_list = temp_frame[field].unique().tolist()
                    output = ""

                    output += f'## {field.replace("_", " ").capitalize()} List\n\n'
                    cnt = len(uniq_list)
                    output += f'There {x(cnt)} {cnt} unique {field.replace("_", " ")}{y(cnt)}associated with your search.\n\n'
                    heading = f'| Unique {field.replace("_", " ")}{y(cnt)}| Count in Hunt Data |\n| ----------- | ----------- |\n'
                    for i in uniq_list:
                        i_cnt = df.loc[df[field] == i, field].count()
                        i_md = f'| {i} | {i_cnt} |\n'
                        heading += i_md
                    output += heading
                    return output
            except Exception as e:
                return f'An error has been reported: <span style="color:red">{e}</span>'

        @interact
        def report_display(column=search_list, search=''):
            try:
                if search == '':
                    return display(Markdown('**Input Search Above.**'))
                else:
                    temp_frame = tmpdf[tmpdf[column].str.contains(search, flags=re.IGNORECASE, regex=True)]

                    for i in search_list:
                        display(Markdown(spread_counts_helper(i, temp_frame)))
                        display(Markdown(" "))

                    display(Markdown('## Rows From Hunt Data'))
                    display(temp_frame)
            except Exception as e:
                display(Markdown(f'An error has been reported: <span style="color:red">{e}</span>'))

    @downselect
    def java_exploit(self, column_list, df=None):
        """Returns any data where java is the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        return df[(df['parent_name'] == 'java.exe') | (df['parent_name'] == 'javaw.exe')][column_list]

    @downselect
    def office_exploit(self, column_list, df=None):
        """Returns any data where Microsoft Office products are the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        return df[(df['parent_name'] == 'winword.exe') | (df['parent_name'] == 'excel.exe')
                  | (df['parent_name'] == 'powerpnt.exe')][column_list]

    @downselect
    def adobe_exploit(self, column_list, df=None):
        """Returns any data where adobe is the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        return df[(df['parent_name'] == 'acrobat.exe') | (
            df['parent_name'] == 'acrord32.exe')][column_list]

    @downselect
    def web_shell_exploit(self, column_list, df=None):
        """Returns any data where web applications are the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Returns the dataframe object
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        return df[(df['parent_name'] == 'w3wp.exe') | (df['parent_name'] == 'tomcat.exe') | (
            df['parent_name'] == 'httpd.exe') | (df['parent_name'] == 'nginx.exe')][column_list]
