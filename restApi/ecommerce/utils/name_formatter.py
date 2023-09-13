def name_format(string):
    prepositions = ['de', 'do', 'da', 'dos', 'das']
    string = string.lower()
    string = map(
        lambda x: x if x in prepositions else x.capitalize(), 
        string.split()
    )
    formatted_string = ' '.join(list(string))
    return formatted_string