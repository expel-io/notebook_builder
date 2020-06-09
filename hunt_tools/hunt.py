import pandas as pd
from IPython.display import display
from IPython.display import HTML
from IPython.display import Javascript
from IPython.display import Markdown


def run_all(ev):
    display(Javascript('IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+1, IPython.notebook.ncells())'))


class Hunt:
    """This class is responsible for processing raw hunt data for Jupyter threat hunting
    Args:
        df (dataframe): the hunt data
    Attributes:
        col_dict (dict): column name normalization
    """

    def __init__(self, file_path):
        self.file_path = file_path

        # Dictionary to normalize hunt_data column names
        # Different vendor technologies will return different field values for the same attribute
        self.col_dict = {
            'src_ip': ['Source IP', 'Source Ip', 'Source IP 1', 'src_ip', 'Source', 'sourceip'],
            'dest_ip': ['Destination IP', 'Destination Ip', 'Dest_Ip', 'Dest_IP', 'dest_ip'],
            'dest_port': ['Destination Port', 'Dest Port', 'dest_port'],
            'domain': ['Domain', 'domain'],
            'process_first_seen': ['Process First Seen', 'first_executed', 'first_seen'],
            'process_last_seen': ['Process Last Seen', 'last_executed', 'last_seen'],
            'connection_first_seen': ['Connection First Seen'],
            'connection_last_seen': ['Connection Last Seen'],
            'process_hash': ['Process Hash', 'Process_Hash', 'process_hash'],
            'process_name': ['Process Name', 'process_name'],
            'process_path': ['Process Path', 'process_path'],
            'process_args': ['Process Arguments', 'Process Args', 'Args', 'args', 'Command Line', 'process_args', 'cmdline'],
            'timestamp': ['Timestamp', 'Registration Date/Time', 'timestamp'],
            'host': ['Hostname', 'hostname', 'Host', 'Asset Name', 'host'],
            'sensor_id': ['Sensor Id', 'Agent ID', 'hostId', 'sensor_id'],
            'parent_name': ['Parent Name', 'parent', 'parent_name'],
            'parent_args': ['Parent Args', 'Parent Arguments', 'parent_args'],
            'user': ['User', 'Process User', 'user', 'Username', 'username', 'process_user', 'user_name'],
            'netconns': ['Netconns', 'netconns', 'Connection Count', 'Connections'],
            'event_id': ['Event Id', 'event_id', 'Event Id(s)', 'Unique Process Id'],
        }

    @property
    def hunt_df(self):
        """Property to get hunt_df from self.file_path.
        Args:
            self
        Returns:
            DataFrame from file_path
        """
        df = pd.read_json(self.file_path, orient='records', typ='frame')
        return df

    def get_hunt_df(self, df=None):
        """Getter function for hunt data
        Args:
            df (dataframe): passed in dataframe to run this function on
        Returns:
            The hunt data dataframe
        """

        if df is not None:
            return df
        else:
            return self.hunt_df.copy()

    def normalize_hunt_df(self, column_list, df=None):
        """Fetches hunt data dataframe and normalizes and appends column names
        Args:
            column_list (list): columns to append to dataframe
            df (dataframe): passed in dataframe to run this function on
        Returns:
            The hunt data dataframe
        """

        df = self.get_hunt_df(df=df)

        # generates a unique ID for each record for reporting and uniquing data
        df['record_id'] = range(1000, 1000 + len(df))
        df['record_id'] = df.record_id.astype(str)

        # This builds a list of current field names
        self.columns1 = list(df.columns.values)
        # and a copy we can apply changes to
        self.columns2 = self.columns1.copy()

        # This next for loop, matches column names and applies changes
        for index, i in enumerate(self.columns2):
            for nbs, recs in self.col_dict.items():
                if i in recs:
                    self.columns2[index] = nbs

        # Renaming requires a dictionary from our "current field names"
        # to our new set of changes
        self.new_col_dict = dict(zip(self.columns1, self.columns2))

        # here, we rename using the dictionary above
        df = df.rename(index=str, columns=self.new_col_dict)

        # use config column_list to make sure all columns are in the data
        # avoids key errors generated from hunting across many different technologies
        for c in column_list:
            if c not in df:
                df[c] = ''

        return df
