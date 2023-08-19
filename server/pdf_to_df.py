import re
import pandas as pd
import PyPDF2




START_PATTERN = r'\n----\|--------\|----\|-----------\|-----------\|-------\|--------\|--------\|\n'
END_PATTERN = r'Signal'
PAGE_END_PATTERN=r'Data File'

STANDARDS = {
    "CH4_2%": "Two percent methane", 
    "600ppmCO2_2.1?ppmCH4": "619? ppm Methane, 2.X ppm CH4",
    "20%CO2": "20% CO2, 80% Nitrogen"
    
    }


# data cleanup

def generate_sample_id_from_sample_name(sample_name):
    if sample_name.startswith('40ML'):
        pass
    if sample_name.startswith(tuple('BEN', 600)):
        return



# generate df from pdf

def pdf_transform(input_file=None):
    print(f"Input file: {input_file}")
    pdf_file = open(input_file, 'rb') 
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    start_stop, sample_names, date = get_start_stop_pts_by_page(pdf_reader)
    df = get_table_data_by_start_stop(start_stop=start_stop, sample_names=sample_names, pdf_reader=pdf_reader, date=date)
    return df


def get_date(page_text):
    regex = r'(.*?)Page 1 of'
    matches = re.findall(regex, page_text)
    slash_locations = re.finditer(r'/', matches[0])
    slash_indices = [x.start() for x in slash_locations]
    date = matches[0][slash_indices[0]-1:slash_indices[1]+5]
    print(f"date from file: {date}")
    return date
    


def get_sample_names(page_text):
    sample_names = []
    regex = r'Signal(.*?)\n'
    matches = re.findall(regex, page_text)
    for x in matches:
        sample_name_regex = r'DUNITZ\\(.*?)\.D'
        sample_name = re.search(sample_name_regex, x).group(1)
        sample_names.append(sample_name)

    return sample_names

def create_df_from_table(table, name, date):
    peaks = []
    for row in table.split('\n'):
        row = " ".join(row.split()).split(" ")
        if len(row) > 7:
            peak, time, type, area, height, width, start, end = row
            peaks.append({
                'Sample_Name': name,
                'Sample_Date': date,
                'Peak': int(peak),
                'Time': float(time),
                'Type': type, 
                'Area': float(area),
                'Height': float(height),
                'Width': float(width),
                'Start': float(start),
                'End': float(end)
            })
    df = pd.DataFrame(peaks)
    return df


def get_start_stop_pts_by_page(pdf_reader):
    page_count = len(pdf_reader.pages)
    start_stop = []
    sample_names = []
    for page in range(0, page_count):
        page_text = pdf_reader.pages[page].extract_text()
        sample_names.append(get_sample_names(page_text))
        start_generator = re.finditer(START_PATTERN, page_text)
        end_generator = re.finditer(END_PATTERN, page_text)
        data_table_start_indices = [e.start() for e in start_generator]
        data_table_end_indices = [e.start() for e in end_generator]
        if page==0:
            # remove the first instance of signal (only for the first page)
            date = get_date(page_text=page_text)
            data_table_end_indices.pop(0)
        start_stop.append({"start": data_table_start_indices, "end": data_table_end_indices})
    return start_stop, sample_names, date

def get_table_data_by_start_stop(start_stop, sample_names, pdf_reader, date):
    table_string = sample_name = None
    page_count = len(pdf_reader.pages)
    dfs = []
    for page_idx, page_data in enumerate(start_stop): # for each page
        page_text = pdf_reader.pages[page_idx].extract_text()
        page_end_generator = re.finditer(PAGE_END_PATTERN, page_text)
        page_end_indices = [e.start() for e in page_end_generator]
        if table_string is not None: # check for carryover string from past page 
            if len(page_data['end']) == 0: # check if table continues to another page
                try:
                    table_string = table_string + '\n' + page_text[page_data['start'][0]+74:page_end_indices[-1]-69]
                    if page_idx == page_count -1: # if its the last page 
                        dfs.append(create_df_from_table(table_string, sample_name, date))
                        table_string = sample_name = None
                    continue
                except:
                    print(f"BORKED on: {table_string} page_text: {page_text}")
            else:
                table_string = table_string + '\n' + page_text[page_data['start'][0] + 74:page_data['end'][0]]
                dfs.append(create_df_from_table(table_string, sample_name, date))
                table_string = sample_name = None

        try:
            for array_idx, start_idx in enumerate(page_data['start']):
                sample_name = sample_names[page_idx][array_idx]
                table_string = page_text[start_idx + 74: page_data['end'][array_idx]]
                dfs.append(create_df_from_table(table_string, sample_name, date))
                table_string = sample_name = None
        except IndexError:
            if page_idx == page_count -1: #last page
                if table_string is None:
                    table_string = page_text[start_idx + 74:page_end_indices[-1]-69]
                else:
                    table_string =table_string + '\n' + page_text[start_idx + 74:page_end_indices[-1]-69]
                dfs.append(create_df_from_table(table_string, sample_name, date))
            table_string = page_text[start_idx + 74:page_end_indices[-1]]
    result = pd.concat(dfs, ignore_index=True)
    return result


"""
TODO
X handle dates
X handle directories
X handle the end of page/last page
X merge data frames
- clean up Code
X logging
X pull into package
"""



if __name__ == '__main__':
    start_stop, sample_names = get_start_stop_pts_by_page(pdf_reader)
    df = get_table_data_by_start_stop(start_stop=start_stop, sample_names=sample_names, pdf_reader=pdf_reader)

