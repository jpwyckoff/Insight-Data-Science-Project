def return_company_name(company_column, ranking_index):
    first_rec = df['company'][ranking_index[0]]
    second_rec = df['company'][ranking_index[1]]
    third_rec = df['company'][ranking_index[2]]
    fourth_rec = df['company'][ranking_index[3]]
    return first_rec, second_rec, third_rec, fourth_rec
