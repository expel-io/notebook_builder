import functools
import re

import ipywidgets as widgets
import numpy as np
import pandas as pd
import qgrid
from IPython.display import display
from IPython.display import HTML
from IPython.display import Javascript
from IPython.display import Markdown
from ipywidgets import fixed
from ipywidgets import interact
from ipywidgets import interact_manual
from ipywidgets import interactive
from ipywidgets import Layout


def downselect(f):
    """This is a decorator run before the function and will catch any errors and can be configured to log and/or
    report to an error reporting tool like Sentry."""

    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            display(Markdown(f'An error has been reported: <span style="color:red">{e}</span>'))
            pass
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
            Displays the dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        new_df = df.groupby(groupby).nunique()[[uniqued]].rename(columns={uniqued: 'count'})
        display(HTML("<br>"))
        display(qgrid.show_grid(new_df, show_toolbar=True))

    @downselect
    def column_frequency_count(self, column, df=None):
        """Returns a dataframe of unique instances of 'column' values and their frequencies

        Args:
            column (str): The column to unique on
            df (dataframe): passed in dataframe to run this downselect on

        Returns:
            Displays the dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        tmpdf = df.groupby([column]).size().reset_index(name='count')
        tmpdf = tmpdf.sort_values(by=['count'], ascending=False).reset_index(drop=True)
        display(qgrid.show_grid(tmpdf, show_toolbar=True))

    @downselect
    def column_group(self, column_list, sort_by, df=None):
        """Returns a dataframe grouped by 'column_list' and sorted by 'sort_by'

        Args:
            column_list (list): The columns to group by
            sort_by (str): Column to sort by
            df (dataframe): passed in dataframe to run this downselect on

        Returns:
            Displays the dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        tmpdf = df[column_list].drop_duplicates()
        tmpdf = tmpdf.sort_values(by=[sort_by], ascending=False).reset_index(drop=True)
        display(qgrid.show_grid(tmpdf, show_toolbar=True))

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

                    display(Markdown('## Process Hash'))
                    lph = len(phash_list)
                    display(Markdown(f'There {x(lph)} {lph} unique process hash{z(lph)}associated with your search.'))
                    h_head = '| Unique Process Hash{z{lph}}| Count in Hunt Data | Engine Hits | Engines Total | Detected By | Detected As |\n| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |\n'

                    for h in phash_list:
                        h_cnt = df.loc[df.process_hash == h, 'process_hash'].count()
                        hit = hash_exe_pat.loc[h, 'engines_hit']
                        etl = hash_exe_pat.loc[h, 'engines_total']
                        dby = hash_exe_pat.loc[h, 'detected_by']
                        das = hash_exe_pat.loc[h, 'detected_as']

                        h_md = f'| {h} | {h_cnt} | {str(hit)} | {str(etl)} | {str(dby)} | {str(das)} |\n'
                        h_head += h_md
                    display(Markdown(h_head))

                else:
                    uniq_list = temp_frame[field].unique().tolist()

                    display(Markdown(f'## {field.replace("_", " ").capitalize()} List'))
                    cnt = len(uniq_list)
                    display(
                        Markdown(f'There {x(cnt)} {cnt} unique {field.replace("_", " ")}{y(cnt)}associated with your search.'))
                    heading = f'| Unique {field.replace("_", " ")}{y(cnt)}| Count in Hunt Data |\n| ----------- | ----------- |\n'
                    for i in uniq_list:
                        i_cnt = df.loc[df[field] == i, field].count()
                        i_md = f'| {i} | {i_cnt} |\n'
                        heading += i_md
                    display(Markdown(heading))
            except Exception as e:
                display(Markdown(f'An error has been reported: <span style="color:red">{e}</span>'))

        @interact
        def report_display(column=search_list, search=''):
            try:
                if search == '':
                    return display(HTML('<h4>Input Search Above.</h4>'))
                else:
                    temp_frame = tmpdf[tmpdf[column].str.contains(search, flags=re.IGNORECASE, regex=True)]

                    for i in search_list:
                        spread_counts_helper(i, temp_frame)
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
            Displays a dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        java_df = df[(df['parent_name'] == 'java.exe') | (df['parent_name'] == 'javaw.exe')][column_list]
        if len(java_df.index) > 0:
            display(HTML("<h3>Exploit of Java</h3>"))
            display(HTML("<br>"))
            java_df_qgrid_widget = qgrid.show_grid(java_df, show_toolbar=True)
            display(java_df_qgrid_widget)
        else:
            display(HTML("<h3>Exploit of Java</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def office_exploit(self, column_list, df=None):
        """Returns any data where Microsoft Office products are the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        office_df = df[(df['parent_name'] == 'winword.exe') | (df['parent_name'] == 'excel.exe')
                       | (df['parent_name'] == 'powerpnt.exe')][column_list]
        if len(office_df.index) > 0:
            display(HTML("<h3>Exploit of Office Apps and Embedded Macros</h3>"))
            display(HTML("<br>"))
            office_df_qgrid_widget = qgrid.show_grid(office_df, show_toolbar=True)
            display(office_df_qgrid_widget)
        else:
            display(HTML("<h3>Exploit of Office Apps and Embedded Macros</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def office_scripting_exploit(self, column_list, df=None):
        """Returns any data where Microsoft Office products are the parent process with scripting child processes
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        office_df = df[(df['parent_name'] == 'winword.exe') | (df['parent_name'] == 'excel.exe')
                       | (df['parent_name'] == 'powerpnt.exe')][column_list].copy()
        office_script_df = office_df[office_df.process_name.str.contains(
            'wscript\.exe|cscript\.exe|vbc\.exe|mshta\.exe|cmd\.exe|powershell\.exe|perl\.exe|python|jsc\.exe', flags=re.IGNORECASE, regex=True)]
        if len(office_script_df.index) > 0:
            display(HTML("<h3>Scripting Interpreters from Exploit of Office Apps and Embedded Macros</h3>"))
            display(HTML("<br>"))
            display(office_script_df)
        else:
            display(HTML("<h3>Scripting Interpreters from Exploit of Office Apps and Embedded Macros</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def browser_scripting_exploit(self, column_list, df=None):
        """Returns any data where Microsoft Office products are the parent process with browser child processes
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        office_df = df[(df['parent_name'] == 'winword.exe') | (df['parent_name'] == 'excel.exe')
                       | (df['parent_name'] == 'powerpnt.exe')][column_list].copy()
        browser_script_df = office_df[office_df.process_name.str.contains(
            'iexplore\.exe|chrome\.exe|firefox\.exe', flags=re.IGNORECASE, regex=True)]
        if len(browser_script_df.index) > 0:
            display(HTML("<h3>Browser activity from Exploit of Office Apps and Embedded Macros</h3>"))
            display(HTML("<br>"))
            display(browser_script_df)
        else:
            display(HTML("<h3>Browser activity from Exploit of Office Apps and Embedded Macros</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def adobe_exploit(self, column_list, df=None):
        """Returns any data where adobe is the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        adobe_df = self.df[(self.df['parent_name'] == 'acrobat.exe') | (
            self.df['parent_name'] == 'acrord32.exe')][column_list]
        if len(adobe_df.index) > 0:
            display(HTML("<h3>Exploit of Adobe apps for Execution</h3>"))
            display(HTML("<br>"))
            adobe_df_qgrid_widget = qgrid.show_grid(adobe_df, show_toolbar=True)
            display(adobe_df_qgrid_widget)
        else:
            display(HTML("<h3>Exploit of Adobe apps for Execution</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def adobe_scripting_exploit(self, column_list, df=None):
        """Returns any data where adobe is the parent process with scripting child processes
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        adobe_df = df[(df['parent_name'] == 'acrobat.exe') | (df['parent_name'] == 'acrord32.exe')][column_list].copy()
        adobe_script_df = adobe_df[adobe_df.process_name.str.contains(
            'wscript\.exe|cscript\.exe|mshta\.exe|cmd\.exe|powershell\.exe|perl\.exe|python|jsc\.exe', flags=re.IGNORECASE, regex=True)]
        if len(adobe_script_df.index) > 0:
            display(HTML("<h3>Scripting Interpreter from Exploit of Adobe apps for Execution</h3>"))
            display(HTML("<br>"))
            display(adobe_script_df)
        else:
            display(HTML("<h3>Scripting Interpreter from Exploit of Adobe apps for Execution</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def web_shell_exploit(self, column_list, df=None):
        """Returns any data where web applications are the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        websh_df = df[(df['parent_name'] == 'w3wp.exe') | (df['parent_name'] == 'tomcat.exe') | (
            df['parent_name'] == 'httpd.exe') | (self.df['parent_name'] == 'nginx.exe')][column_list]
        if len(websh_df.index) > 0:
            display(HTML("<h3>Webshell Spawning Sub-Process</h3>"))
            display(HTML("<br>"))
            websh_df_qgrid_widget = qgrid.show_grid(websh_df, show_toolbar=True)
            display(websh_df_qgrid_widget)
        else:
            display(HTML("<h3>Webshell Spawning Sub-Process</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))

    @downselect
    def sql_exploit(self, column_list, df=None):
        """Returns any data with SQL applications as the parent process
        Args:
            column_list (list): columns to display in dataframe
            df (dataframe): passed in dataframe to run this downselect on
        Returns:
            Displays a dataframe as QGrid
        """

        df = self.get_df(df=df)
        if df.empty:
            return None

        sqlinj_df = df[(df['parent_name'] == 'sqlservr.exe') | (df['parent_name'] == 'mysqld.exe') | (
            df['parent_name'] == 'postgres.exe') | (self.df['parent_name'] == 'mongod.exe')][column_list]
        if len(sqlinj_df.index) > 0:
            display(HTML("<h3>SQL Injection</h3>"))
            display(HTML("<br>"))
            sqlinj_df_qgrid_widget = qgrid.show_grid(sqlinj_df, show_toolbar=True)
            display(sqlinj_df_qgrid_widget)
        else:
            display(HTML("<h3>SQL Injection</h3>"))
            display(HTML("<br>"))
            display(HTML("<p><b>Returned no results.</b></p>"))
            display(HTML("<br>"))
            return None
