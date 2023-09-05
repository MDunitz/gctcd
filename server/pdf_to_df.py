import re
import pandas as pd
import PyPDF2
from .constants import *



START_PATTERN = r'\n----\|--------\|----\|-----------\|-----------\|-------\|--------\|--------\|\n'
END_PATTERN = r'Signal'
PAGE_END_PATTERN=r'Data File'



def pdf_transform(input_file=None):
    print(f"Input file: {input_file}")
    pdf_file = open(input_file, 'rb') 
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    start_stop, sample_names, date, instrument = get_start_stop_pts_by_page(pdf_reader)
    file_info = {"date": date, "instrument": instrument, "input_file": input_file}
    df = get_table_data_by_start_stop(start_stop=start_stop, sample_names=sample_names, pdf_reader=pdf_reader, file_info=file_info)
    return df


def get_date(page_text):
    regex = r'(.*?)Page 1 of'
    matches = re.findall(regex, page_text)
    slash_locations = re.finditer(r'/', matches[0])
    slash_indices = [x.start() for x in slash_locations]
    date = matches[0][slash_indices[0]-1:slash_indices[1]+5]
    return date
    

def get_instrument(page_text):
    regex = r'Data File C:\\HPCHEM\\(.*?)\\'
    instrument_id = re.search(regex, page_text).group(1)
    if int(instrument_id) == 2:
        return GCFID
    elif int(instrument_id) == 4:
       return GCTCD
    else:
        print("Could NOT id the instrument from the pdf")
        return None
    


def get_sample_names(page_text, page):
    sample_names = []
    regex = r'Signal(.*?)\n'
    matches = re.findall(regex, page_text)
    try:
        for x in matches:
            sample_name_regex = r'DUNITZ\\(.*?)\.D'
            sample_name = re.search(sample_name_regex, x).group(1)
            sample_names.append(sample_name)
    except AttributeError: # if the sample name isnt embedded in the signal get it from elsewhere
        regex = r'Sample Name: (.*?)\n'
        sample_name = re.search(regex, page_text).group(1)
        sample_names.append(sample_name)
    if len(sample_names)==0:
        print(f"No sample name found for page: {page}")
    return sample_names

def create_df_from_table(table, name, file_info):
    peaks = []
    for row in table.split('\n'):
        row = " ".join(row.split()).split(" ")
        if len(row) > 7:
            peak, time, type, area, height, width, start, end = row
            peaks.append({
                'Sample_Name': name,
                'Sample_Date': file_info['date'],
                'Instrument': file_info['instrument'],
                'Peak': int(peak),
                'Time': float(time),
                'Type': type, 
                'Area': float(area),
                'Height': float(height),
                'Width': float(width),
                'Start': float(start),
                'End': float(end),
                "pdf_file_name": file_info['input_file'],
            })
    df = pd.DataFrame(peaks)
    return df


def get_start_stop_pts_by_page(pdf_reader):
    page_count = len(pdf_reader.pages)
    start_stop = []
    sample_names = []
    for page in range(0, page_count):
        page_text = pdf_reader.pages[page].extract_text()
        sample_names.append(get_sample_names(page_text, page))
        start_generator = re.finditer(START_PATTERN, page_text)
        end_generator = re.finditer(END_PATTERN, page_text)
        data_table_start_indices = [e.start() for e in start_generator]
        data_table_end_indices = [e.start() for e in end_generator]
        if page==0:
            # remove the first instance of signal (only for the first page)
            date = get_date(page_text=page_text)
            data_table_end_indices.pop(0)
            instrument = get_instrument(page_text)
        start_stop.append({"start": data_table_start_indices, "end": data_table_end_indices})
    return start_stop, sample_names, date, instrument

def get_table_data_by_start_stop(start_stop, sample_names, pdf_reader, file_info):
    table_string = sample_name = None
    page_count = len(pdf_reader.pages)
    dfs = []
    for page_idx, page_data in enumerate(start_stop): # for each page
        page_text = pdf_reader.pages[page_idx].extract_text()
        page_end_generator = re.finditer(PAGE_END_PATTERN, page_text)
        page_end_indices = [e.start() for e in page_end_generator]
        if table_string is not None: # check for carryover string from past page

            if len(page_data['end']) == 0: # check if table doesnt end on this page
                if len(page_data['start']) == 0: # basically there is nothing on this page 
                    dfs.append(create_df_from_table(table_string, sample_name, file_info))
                    table_string = sample_name = None
                else:
                    table_string = table_string + '\n' + page_text[page_data['start'][0]+74:page_end_indices[-1]-69]
                    if page_idx == page_count -1: # if its the last page 
                        dfs.append(create_df_from_table(table_string, sample_name, file_info))
                        table_string = sample_name = None
                    continue
            else:
                table_string = table_string + '\n' + page_text[page_data['start'][0] + 74:page_data['end'][0]]
                dfs.append(create_df_from_table(table_string, sample_name, file_info))
                # pop off first start/end indexes so the sample names match the table (and we dont grab the same table again in the for loop below)
                page_data['start'].pop(0)
                page_data['end'].pop(0)
                table_string = sample_name = None

        try:
            for array_idx, start_idx in enumerate(page_data['start']):
                sample_name = sample_names[page_idx][array_idx]
                table_string = page_text[start_idx + 74: page_data['end'][array_idx]]
                dfs.append(create_df_from_table(table_string, sample_name, file_info))
                table_string = sample_name = None
        except IndexError:
            if page_idx == page_count -1: #last page
                if table_string is None:
                    table_string = page_text[start_idx + 74:page_end_indices[-1]-69]
                else:
                    table_string =table_string + '\n' + page_text[start_idx + 74:page_end_indices[-1]-69]
                dfs.append(create_df_from_table(table_string, sample_name, file_info))
            table_string = page_text[start_idx + 74:page_end_indices[-1]]
        if len(sample_names[page_idx]) > len(page_data['start']): # sample named on page before the table starts
            try:
                sample_name = sample_names[page_idx][array_idx + 1]
            except IndexError:
                print(f"sample_names: {sample_names}, page_idx: {page_idx}, page_count: {page_count}, array_idx: {array_idx}, table_String: {table_string}, sample_name: {sample_name}, page_data: {page_data}, page_text: {page_text}")
            table_string = "" # hack to correctly associate sample name with sample data on next page
    
    result = pd.concat(dfs, ignore_index=True)
    return result