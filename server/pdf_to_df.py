import re
import pandas as pd
import PyPDF2

file_path = '../../../Desktop/lab_work/sessions/GCTCD/20230816/40mL_1.x.pdf'
pdf_file = open(file_path, 'rb') 
pdf_reader = PyPDF2.PdfReader(pdf_file)


START_PATTERN = r'\n----\|--------\|----\|-----------\|-----------\|-------\|--------\|--------\|\n'
END_PATTERN = r'Signal'
PAGE_END_PATTERN=r'Data File'

def get_sample_names(page_text):
    sample_names = []
    regex = r'Signal(.*?)\n'
    matches = re.findall(regex, page_text)
    for x in matches:
        sample_name_regex = r'DUNITZ\\(.*?)\.D'
        sample_name = re.search(sample_name_regex, x).group(1)
        sample_names.append(sample_name)

    return sample_names

def create_df_from_table(table, name):
    peaks = []
    ### FIX ME
    sample_date = "8/16/2023"
    for row in table.split('\n'):
        row = " ".join(row.split()).split(" ")
        if len(row) > 7:
            peak, time, type, area, height, width, start, end = row
            peaks.append({
                'Sample_ID': name,
                'Sample_Date': sample_date,
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
            data_table_end_indices.pop(0)
        start_stop.append({"start": data_table_start_indices, "end": data_table_end_indices})
    return start_stop, sample_names

def get_table_data_by_start_stop(start_stop, sample_names, pdf_reader):
    table_string = None
    sample_name = None
    page_count = len(pdf_reader.pages)
    dfs = []
    for page_idx, page_data in enumerate(start_stop): # for each page
        page_text = pdf_reader.pages[page_idx].extract_text()
        page_end_generator = re.finditer(PAGE_END_PATTERN, page_text)
        page_end_indices = [e.start() for e in page_end_generator]
        if table_string is not None: # check for carryover string from past page 
            if len(page_data['end']) == 0: # check if its the last page (or if the table goes onto a 3rd+ page)
                table_string = table_string + '\n' + page_text[page_data['start'][0]+74:page_end_indices[-1]-69]
                if page_idx == page_count -1: # if its the last page 
                    dfs.append(create_df_from_table(table_string, sample_name))
                    table_string = None
                    sample_name = None
                continue
            else:
                table_string = table_string + '\n' + page_text[page_data['start'][0] + 74:page_data['end'][0]]
                dfs.append(create_df_from_table(table_string, sample_name))
                table_string = None
                sample_name = None
        try:
            for array_idx, start_idx in enumerate(page_data['start']):
                sample_name = sample_names[page_idx][array_idx]
                table_string = page_text[start_idx + 74: page_data['end'][array_idx]]
                dfs.append(create_df_from_table(table_string, sample_name))
                table_string = None
                sample_name=None
        except IndexError:
            if page_idx == page_count -1:
                print('this code actually got hit')
                table_string =table_string + '\n' + page_text[start_idx + 74:page_end_indices[-1]-69]
                dfs.append(create_df_from_table(table_string, sample_name))
            table_string = page_text[start_idx + 74:page_end_indices[-1]]
    result = pd.concat(dfs, ignore_index=True)
    print(result)
    return result


"""
TODO
- handle dates
X handle the end of page/last page
X merge data frames
- clean up Code
- pull into package
"""



if __name__ == '__main__':
    start_stop, sample_names = get_start_stop_pts_by_page(pdf_reader)
    df = get_table_data_by_start_stop(start_stop=start_stop, sample_names=sample_names, pdf_reader=pdf_reader)

