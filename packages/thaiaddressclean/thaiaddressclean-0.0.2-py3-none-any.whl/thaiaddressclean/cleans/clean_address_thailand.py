import pandas as pd
import re
import csv
import importlib.resources

# thai_addr_file_path =  f'../refs/thai_addr.csv'
# thai_address_reference = pd.read_csv(thai_addr_file_path)



def validate_value(data_input, thai_address_reference, column_ref, column_result):
    match = thai_address_reference.loc[thai_address_reference[column_ref] == data_input, column_result]
    return match.iloc[0] if not match.empty else ''


def validate_province(prov_key, thai_address_reference):
    province_validated = validate_value(prov_key, thai_address_reference, 'ProvinceThai', 'ProvinceThai')
    if not province_validated:
        province_validated = validate_value(prov_key, thai_address_reference, 'ProvinceEng', 'ProvinceThai')
    return province_validated


def validate_district(dist_key, thai_address_reference):
    for col in ['DistrictThai', 'DistrictThaiShort', 'DistrictEng', 'DistrictEngShort']:
        district_validated = validate_value(dist_key, thai_address_reference, col, 'DistrictThai')
        if district_validated:
            return district_validated
    return ''


def validate_subdistrict(subdist_key, thai_address_reference):
    for col in ['TambonThai', 'TambonThaiShort', 'TambonEng', 'TambonEngShort']:
        subdistrict_validated = validate_value(subdist_key, thai_address_reference, col, 'TambonThai')
        if subdistrict_validated:
            return subdistrict_validated
    return ''


def validate_subdistrict_by_district_prov(subdist_key, thai_address_reference, province=None, district=None):
    filtered_reference = thai_address_reference
    if province:
        filtered_reference = filtered_reference[filtered_reference['ProvinceThai'] == province]
    if district:
        filtered_reference = filtered_reference[filtered_reference['DistrictThai'] == district]
    for col in ['TambonThai', 'TambonThaiShort', 'TambonEng', 'TambonEngShort']:
        match = filtered_reference[filtered_reference[col] == subdist_key]
        # if not match.empty:
        #     return match.iloc[0]['TambonThai']
        if len(match) > 1:
            exact_match = match[match[col] == subdist_key]
            if not exact_match.empty:
                return exact_match.iloc[0]['TambonThai'] 
            else:
                return match.iloc[0]['TambonThai'] 

        elif not match.empty:
            return match.iloc[0]['TambonThai']
    return ''


def extract_subdistrict_district(text):
    subdistrict_match = re.findall(r'\bต\.\S*', text)
    district_match = re.findall(r'\bอ\.\S*', text)
    subdistrict = subdistrict_match[0][2:] if subdistrict_match else None
    district = district_match[0][2:] if district_match else None 
    return subdistrict, district

def clean_split_with_subdistrict_district(split_list, subdistrict, district):
    cleaned_split = []
    for item in split_list:
        normalized_item = re.sub(r'^(อ|ต)', '', item)
        if item.startswith('อ') and district and normalized_item == district:
            cleaned_split.append(district)  
        elif item.startswith('ต') and subdistrict and normalized_item == subdistrict:
            cleaned_split.append(subdistrict)  
        else:
            cleaned_split.append(item)  
    return cleaned_split

def preprocess_province_in_split_list(split_list):
    return ["กรุงเทพมหานคร" if item in ["กรุงเทพฯ", "กรุงเทพ","กทม","กทม."] else item for item in split_list]





def cleanse_and_autofill_address(input_address, thai_address_reference):
    exclude_patterns = [r'\bRoad\b', r'\bStreet\b', r'\bSoi\b', r'\bBuilding\b', r'\bFloor\b']
    cleaned_address = re.sub(r'[.]', '', input_address) 
    cleaned_address_parts = cleaned_address.split(",")  
    split_address = []
    split_address_noclean = []
    for part in cleaned_address_parts:
        split_address_noclean.extend(part.strip().split())
    split_address_noclean = split_address_noclean[::-1]
    split_address_noclean = preprocess_province_in_split_list(split_address_noclean)
    subdistrict_spl, district_spl = extract_subdistrict_district(input_address)
    split_address = clean_split_with_subdistrict_district(split_address_noclean, subdistrict_spl, district_spl)
    # print(f'======== Split : {split_address}')
    if split_address[0].isdigit() and len(split_address[0]) == 5:

        return cleanse_and_autofill_address_by_position(split_address, thai_address_reference)
    else:
        result = {
        'valid':False,
        'postal_code': None,
        'province': None,
        'district': None,
        'subdistrict': None,
        'full_address': input_address
        }
        for row in split_address:
            if row.isdigit() and len(row) == 5: 
                result['postal_code'] = row
                match = thai_address_reference[thai_address_reference['PostCodeMain'] == int(row)]
                if not match.empty:
                    result['province'] = match.iloc[0]['ProvinceThai']
                    result['district'] = match.iloc[0]['DistrictThai']
                break
        # print(f'1 : {result}')            
        if not result['province']:
            for row in split_address:
                prov_key = re.sub(r'(จ\.|จังหวัด)', '', row) if re.match('(จ\.[^\s]+|จังหวัด[^\s]+)', row) else row
                province_validated = validate_province(prov_key, thai_address_reference)
                if province_validated:
                    result['province'] = province_validated
                    break
        # print(f'2 : {result}')    
        if not result['district']:
            for row in split_address:
                if row == "เมือง" and result['province']:
                    dist_key = "เมือง" + result['province']
                else:
                    dist_key = re.sub(r'(อ\.|อำเภอ|เขต)', '', row) if re.match('(อ\.[^\s]+|อำเภอ[^\s]+|เขต[^\s]+)', row) else row
                district_validated = validate_district(dist_key, thai_address_reference)
                if district_validated:
                    result['district'] = district_validated
                    break
        # print(f'3 : {result}')  
        for row in split_address[2:]:
            if any(re.search(pattern, row, re.IGNORECASE) for pattern in exclude_patterns):
                continue
            subdist_key = re.sub(r'(ต\.|ตำบล|แขวง)', '', row) if re.match('(ต\.[^\s]+|ตำบล[^\s]+|แขวง[^\s]+)', row) else row
            # subdistrict_validated = validate_subdistrict(subdist_key, thai_address_reference)
            subdistrict_validated = validate_subdistrict_by_district_prov(subdist_key, thai_address_reference, province=result.get('province'), district=result.get('district'))
            if subdistrict_validated:
                result['subdistrict'] = subdistrict_validated
                break
        # print(f'4 : {result}')   
        #------- Zipcode validate
        if all([result['province'], result['district'], result['subdistrict']]):
            match = thai_address_reference[
                (thai_address_reference['ProvinceThai'] == result['province']) &
                (thai_address_reference['DistrictThai'] == result['district']) 
            ]
            if not match.empty:
                result['postal_code'] = match.iloc[0]['PostCodeMain']

        
        #------- Auto fill -------
        # district
        if not result['district'] and result['province'] and result['subdistrict']:
            match = thai_address_reference[
                (thai_address_reference['ProvinceThai'] == result['province']) &
                (thai_address_reference['TambonThai'] == result['subdistrict'])
            ]
            if not match.empty:
                result['district'] = match.iloc[0]['DistrictThai']

        # province
        if not result['province'] and result['district'] and result['subdistrict']:
            match = thai_address_reference[
                (thai_address_reference['DistrictThai'] == result['district']) &
                (thai_address_reference['TambonThai'] == result['subdistrict'])
            ]
            if not match.empty:
                result['province'] = match.iloc[0]['ProvinceThai']

        # province and district by sub
        if not result['province'] and not result['district'] and result['subdistrict']:
            match = thai_address_reference[
                (thai_address_reference['TambonThai'] == result['subdistrict'])
            ]
            if not match.empty:
                result['province'] = match.iloc[0]['ProvinceThai']
                result['district'] = match.iloc[0]['DistrictThai']

        # postcode
        if not result['postal_code'] and all([result['province'], result['district']]):
            match = thai_address_reference[
                (thai_address_reference['ProvinceThai'] == result['province']) &
                (thai_address_reference['DistrictThai'] == result['district'])
            ]
            if not match.empty:
                result['postal_code'] = match.iloc[0]['PostCodeMain']

        # province and postcode by district
        if not result['postal_code'] and not result['province'] and result['district']:
            match = thai_address_reference[
                (thai_address_reference['DistrictThai'] == result['district'])
            ]
            if not match.empty:
                result['postal_code'] = match.iloc[0]['PostCodeMain']
                result['province'] = match.iloc[0]['ProvinceThai']

        #---- final validate with master data
        # print(f'Final : {result}')
        if result['province'] and result['district'] and result['subdistrict']:
            valid_match = thai_address_reference[
                (thai_address_reference['ProvinceThai'] == result['province']) &
                (thai_address_reference['DistrictThai'] == result['district']) &
                (thai_address_reference['TambonThai'] == result['subdistrict'])
            ]
            if valid_match.empty:
                print("Invalid : not match data in master")
                result['subdistrict'] = None
            else:
                result['valid'] = True



        return result


def cleanse_and_autofill_address_by_position(split_address, thai_address_reference):
    result = {
        'valid':False,
        'postal_code': None,
        'province': None,
        'district': None,
        'subdistrict': None,
        'full_address': ' '.join(split_address[::-1])
    }
    #  1: Postcode
    if split_address[0].isdigit() and len(split_address[0]) == 5:
        result['postal_code'] = split_address[0]
        match = thai_address_reference[thai_address_reference['PostCodeMain'] == int(split_address[0])]
        if not match.empty:
            result['province'] = match.iloc[0]['ProvinceThai']
            result['district'] = match.iloc[0]['DistrictThai']
    #  2: Province
    if len(split_address) > 1:
        result['province'] = validate_province(split_address[1], thai_address_reference)
    #  3: District
    if len(split_address) > 2:
        if split_address[2] == "เมือง" and result['province']:
            split_address[2] = "เมือง" + result['province']
        result['district'] = validate_district(split_address[2], thai_address_reference)
    #  4: Subdistrict
    if len(split_address) > 3:
        # result['subdistrict'] = validate_subdistrict(split_address[3], thai_address_reference)
        result['subdistrict']  = validate_subdistrict_by_district_prov(split_address[3], thai_address_reference, province=result.get('province'), district=result.get('district'))
    #------- Auto fill -------
    # district
    if not result['district'] and result['province'] and result['subdistrict']:
        match = thai_address_reference[
            (thai_address_reference['ProvinceThai'] == result['province']) &
            (thai_address_reference['TambonThai'] == result['subdistrict'])
        ]
        if not match.empty:
            result['district'] = match.iloc[0]['DistrictThai']
    # province
    if not result['province'] and result['district'] and result['subdistrict']:
        match = thai_address_reference[
            (thai_address_reference['DistrictThai'] == result['district']) &
            (thai_address_reference['TambonThai'] == result['subdistrict'])
        ]
        if not match.empty:
            result['province'] = match.iloc[0]['ProvinceThai']
    # province and district by sub
    if not result['province'] and not result['district'] and result['subdistrict']:
        match = thai_address_reference[
            (thai_address_reference['TambonThai'] == result['subdistrict'])
        ]
        if not match.empty:
            result['province'] = match.iloc[0]['ProvinceThai']
            result['district'] = match.iloc[0]['DistrictThai']
    # postal_code
    if not result['postal_code'] and all([result['province'], result['district']]):
        match = thai_address_reference[
            (thai_address_reference['ProvinceThai'] == result['province']) &
            (thai_address_reference['DistrictThai'] == result['district']) 
        ]
        if not match.empty:
            result['postal_code'] = match.iloc[0]['PostCodeMain']
    # province and postcode by district
        if not result['postal_code'] and not result['province'] and result['district']:
            match = thai_address_reference[
                (thai_address_reference['DistrictThai'] == result['district'])
            ]
            if not match.empty:
                result['postal_code'] = match.iloc[0]['PostCodeMain']
                result['province'] = match.iloc[0]['ProvinceThai']

    # print(f'Final : {result}')
    if result['province'] and result['district'] and result['subdistrict']:
        valid_match = thai_address_reference[
            (thai_address_reference['ProvinceThai'] == result['province']) &
            (thai_address_reference['DistrictThai'] == result['district']) &
            (thai_address_reference['TambonThai'] == result['subdistrict'])
        ]
        if valid_match.empty:
            print("Invalid : not match data in master")
            result['subdistrict'] = None
        else:
            result['valid'] = True
    return result


def load_csv_data():
    # ใช้ pandas ในการอ่านไฟล์ CSV เป็น DataFrame โดยตรง
    with importlib.resources.path("thaiaddressclean.refs", "thai_addr.csv") as csv_path:
        data = pd.read_csv(csv_path)
    return data
thai_address_reference = load_csv_data()
def clean_thai_address(input_address):
    return cleanse_and_autofill_address(input_address, thai_address_reference)




# print(f'============For test===================')
# input_address = ""
# filled_address = cleanse_and_autofill_address(input_address, thai_address_reference)
# print(f'Result : {filled_address}')
# print(f'===============================')



# example_addr_file_path =  f'../refs/example_addr.csv'
# example_address_reference = pd.read_csv(example_addr_file_path)

# def test_cleanse_and_autofill_address(example_address_reference, thai_address_reference):
#     results = [] 
#     for index, row in example_address_reference.iterrows():
#         input_address = row['address_full'] 
#         result = cleanse_and_autofill_address(input_address, thai_address_reference)
#         results.append(result)
#     results_df = pd.DataFrame(results)
#     return results_df

# test_results = test_cleanse_and_autofill_address(example_address_reference, thai_address_reference)
# print(test_results)
#--------- Export to csv
# test_results.to_csv('../output/cleaned_addresses.csv', index=False, encoding="utf-8")
#--------- Save to local postgres
# engine = create_engine('postgresql+psycopg2://postgres:ja8yt24@localhost:5433/clean')
# test_results = test_results.astype({col: 'object' if dtype == 'O' else 'float' if dtype == 'float64' else 'int' for col, dtype in test_results.dtypes.items()})
# test_results = test_results.applymap(lambda x: int(x) if isinstance(x, (np.integer, np.int64)) else x)
# test_results.to_sql('cleaned_addresses4', con=engine, if_exists='replace', index=False)