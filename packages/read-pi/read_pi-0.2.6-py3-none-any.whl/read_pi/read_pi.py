# !pip install tagreader
import tagreader
import pandas as pd
import numpy as np
import pickle
from os.path import exists
from os import remove


def save_to_cache(object, cache_file='./cache/cache_file.pkl'):
    write_mode = 'ab+' if exists(cache_file) else 'wb'
    try:
        with open(cache_file, write_mode) as f:
            pickle.dump(object, f)
    except:
        print("WARNING: failed to save cache file.")


def read_from_cache(key, cache_file='./cache/cache_file.pkl'):
    if not exists(cache_file):
        return None
    data = {}
    with open(cache_file, 'rb') as f:
        try:
            while key not in data:
                data = pickle.load(f)
        except EOFError:
            return None
        except TypeError:
            return None
    return data[key]


def clean_cache(cache_file='./cache/cache_file.pkl'):
    try:
        remove(cache_file)
        print(f"cache file deleted.")
    except:
        print(f"failed to delete cache file '{cache_file}'.")


def connect_to_PI(datasource='ONO-IMS', imstype='piwebapi'):
    # connect to PI vision
    c = tagreader.IMSClient(datasource, imstype)
    c.connect()
    return c


def search_tag(tag_pattern=None, description=None, pi_connection=None, datasource='ONO-IMS', imstype='piwebapi'):
    if tag_pattern is None and description is None:
        raise ValueError("can't both, tag_pattern and description, be None.")
    if pi_connection is None:
        pi_connection = connect_to_PI(datasource=datasource, imstype=imstype)
    return pi_connection.search(tag_pattern)


def get_data_from_PI(tags, start, end, interval, agg='AVG', pi_connection=None, verbose=False, rename=True, use_cache=False,
                     datasource='ONO-IMS', imstype='piwebapi'):
    if type(tags) is dict:
        tag_rename = {tag: alias for alias, tag in tags.items() if type(tag) is str}
        tag_rename.update({tag_: alias for alias, tag in tags.items() for tag_ in tag if type(tag) is list})
        tags = [tag
                for subitem in (tag_or_list 
                                if type(tag_or_list) is list
                                else [tag_or_list] for tag_or_list in tags.values())
                for tag in subitem]
    else:
        tag_rename = None
        
    # convert start and end string to datetime
    if type(start) is str:
        start = pd.to_datetime(start)
    if type(end) is str:
        end = pd.to_datetime(end)

    # look for requested data in cache file
    if use_cache:
        if verbose:
            print("   looking for this data in cache...")
        data = read_from_cache((str(tags), start, end, 'None' if agg == "RAW" else interval, agg))
        from_cache_ = True
    else:
        data = None

    if data is None:
        from_cache_ = False
        if verbose:
            print("   fetching data from PI...")
        if pi_connection is None:
            pi_connection = connect_to_PI(datasource=datasource, imstype=imstype)

        # download the data from PI Vision
        if (end - start).total_seconds() / interval > 150000:
            attempts = []
            attempt = start
            while attempt < end:
                next_attempt = attempt + np.timedelta64(interval * 100000, 's')
                attempts.append((attempt, next_attempt))
                attempt = next_attempt
            if verbose:
                print(f'  time window is too long, reading data in {len(attempts)} parts.')
            data = pd.concat(
                [pi_connection.read(tags,
                                    attempt[0],
                                    attempt[1], 
                                    interval,
                                    read_type=agg)
                for attempt in attempts],
                axis=0
                )

        else:
            data = pi_connection.read(tags,
                                    start,
                                    end, 
                                    interval,
                                    read_type=agg)
    
    if tag_rename is not None and 'tag_columns' not in data.attrs:
        data.attrs['requested_tags'] = tag_rename

        data.attrs['tag_columns'] = list(data.columns)
        if rename:
            data.rename(columns=tag_rename, inplace=True)

    data = data.fillna(value=np.nan).astype(float)
    
    # save requested data into cache file
    if use_cache and not from_cache_:
        save_to_cache({(str(tags), start, end, 'None' if agg == "RAW" else interval, agg): data})

    return data


def get_raw_data_from_PI(tags, start, end, interval=None, agg='RAW', pi_connection=None, verbose=False, rename=True, use_cache=False,
                     datasource='ONO-IMS', imstype='piwebapi', pre_time='365day', fillna_method='ffill'):
    """
    Gets the RAW data for each one of the tags and merge them into a single dataframe.
    
    This function is designed to download the data from discontinuos tags, like valves data,
    then some additional time before the `start` will be downloadeded aimed to ensure there 
    will be data within the requested timeframe. 
    This additiona time can be set using the parameter `pre_time`.
    The null values in the merged DataFrame will be filled using the `fillna_method`, 
    set to forward filling as default to complete the sporadict data from the valves tags.
    """
    # convert start and end string to datetime
    if type(start) is str:
        start = pd.to_datetime(start)
    if type(end) is str:
        end = pd.to_datetime(end)
    if type(pre_time) is str:
        pre_time = pd.to_timedelta(pre_time)

    if type(tags) is str:
        tags = [tags]
        columns_names = tags
    elif type(tags) is dict:
        columns_names = [alias for alias in tags.values()]
        tags = [{tag: alias} for tag, alias in tags.items()]
    else:
        columns_names = list(tags)
    
    data = [get_data_from_PI(tag, start - pre_time, end, interval=60*60*24 if interval is None else interval, agg=agg, pi_connection=pi_connection, 
                             verbose=verbose, rename=rename, use_cache=use_cache,
                             datasource=datasource, imstype=imstype) for tag in tags]

    if len(data) == 0:
        data = pd.DataFrame(columns=columns_names)
    elif len(data) == 1:
        data = data[0].sort_index()
        if len(data.index) > 0:
            tz = data.index[0].tz
            data = data.loc[start.tz_localize(tz): end.tz_localize(tz)]
    elif len(data) > 1:
        data = data[0].join(data[1:], how='outer').sort_index()
        if fillna_method == 'ffill':
            data.ffill(inplace=True)
        elif fillna_method == 'bfill':
            data.bfill(inplace=True)
        if len(data.index) > 0:
            tz = data.index[0].tz
            data = data.loc[start.tz_localize(tz): end.tz_localize(tz)]
    
    return data
