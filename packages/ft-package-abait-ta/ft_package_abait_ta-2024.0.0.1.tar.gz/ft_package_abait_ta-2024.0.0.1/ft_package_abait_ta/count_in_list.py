def count_in_list(input_list: list, search_for: any) -> int:
    """
    This Function is used to count
    how many Occurence of search_for are in input_list
also the function raise an exception once the input_list is None
    * Function only accept list ==> type(input_list) == <class 'list'>
    search_for can be 'any'
    """
    try:
        if input_list is None:
            raise TypeError("'NoneType' object is not a list")
        return input_list.count(search_for)
    except Exception as e:
        print(f'raised  : {e}')
