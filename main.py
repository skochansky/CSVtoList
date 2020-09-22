import re
import pandas




def check_previous_and_next_line(current_index, listed):
    bool_list = []
    prev_line = listed[current_index - 1]
    next_line = listed[current_index + 1]
    if prev_line.count('*') > 5:
        bool_list.append(True)

    if next_line.count(',') > 0:
        bool_list.append(True)

    if bool_list.count(True) == 2:
        return True
    else:
        return False


def create_table_element(current_index, listed):
    columns = listed[current_index - 2]
    data_name = listed[current_index]
    work_index = current_index
    data = []
    line = ','
    while True:
        work_index += 1
        line = listed[work_index]
        if line.count(',') == 0:
            break
        data.append(line)
    return {'columns': columns, 'table_name': data_name, 'data': data}


def create_tables(listed):
    tables = []
    pattern = [r"%(.*)", r"!(.*)"]
    for elem in listed:
        current_index = listed.index(elem)
        for p in pattern:
            if re.match(p, elem):
                if check_previous_and_next_line(current_index, listed):
                    data = create_table_element(current_index, listed)
                    tables.append(data)
    return tables


def prepare_to_dataframe(tables):
    new_tables = []
    for table in tables:
        columns = table['columns'].replace('*', '')
        columns = columns.split(',')
        data = list(map(lambda x: x.split(','), table['data']))
        new_tables.append({'name': table['table_name'], 'columns': columns, 'data': data})
    return new_tables


def create_dataframe(tables_prepared_to_dataframe):
    dataframes = []
    for table in tables_prepared_to_dataframe:
        df = pandas.DataFrame(data=table['data'], columns=table['columns'])
        d = {'name': table['name'], 'dataframe': df}
        dataframes.append(d)
    return dataframes


def extract_from_dataframe(dataframes):
    # For example extract COLOR from table COVERINGS
    # Write name of table
    table_name = 'COVERINGS'
    for df in dataframes:
        lista = []
        if table_name in df['name']:
            # Variable as series
            extracted_series_part = df['dataframe']['PART_NUMBER']
            extracted_series_xy = df['dataframe']['XY']
            extracted_series_color = df['dataframe']['COLOR']
            k = 0
            for s in extracted_series_color:
                if s != 'BLACK' and s is not None:
                    lista.append(extracted_series_xy[k])
                    lista.append(extracted_series_part[k])
                k=k+1
            return lista

def czytaj_csv(path):
    with open(r'' + path) as c:
        file = c.read()

    listedd = file.split('\n')
    listedd = list(map(lambda x: x.replace(' ', ''), listedd))
    #pattern = [r"%(.*)", r"!(.*)"]
    #current_index = ''

    tables = create_tables(listedd)
    tables_prepared_to_dataframe = prepare_to_dataframe(tables)
    dataframes = create_dataframe(tables_prepared_to_dataframe)
    output = extract_from_dataframe(dataframes)
    return output

if __name__ == '__main__':

    print(czytaj_csv('COMPOSITE-ALL.csv'))

"""my_data = []
for table in tables:
   if 'LIBTYPE' in table['columns']:
       for elem in table['data']:
           listed_elem = elem.split(',')
           try:
               if 'TAPE' in listed_elem[-2]:
                   my_data.append(listed_elem)
           except:
               pass
"""
