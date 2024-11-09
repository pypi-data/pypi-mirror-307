from pdm_tools import tools


def user_query(sql:str):
    return tools.query(sql)


def list_fields():
    sql = """
    (SELECT DISTINCT [GOV_FIELD_NAME]
    FROM [PDMVW].[WB_PROD_DAY]
    UNION
    SELECT DISTINCT [GOV_FIELD_NAME]
    FROM [PDMVW].[WB_INJ_DAY])
    ORDER BY [GOV_FIELD_NAME]
    """
    return tools.query(sql)


def list_injectors(field_name:str):
    sql = f"""
    SELECT [WB_UWBI], MIN([PROD_DAY]) AS FIRST_INJ, MAX([PROD_DAY]) AS LAST_INJ
    FROM [PDMVW].[WB_INJ_DAY]
    WHERE [GOV_FIELD_NAME] = '{field_name.strip().upper()}'
    GROUP BY [WB_UWBI]
    """
    return tools.query(sql)


def list_producers(field_name:str):
    sql = f"""
    SELECT [WB_UWBI], MIN([PROD_DAY]) AS FIRST_PROD, MAX([PROD_DAY]) AS LAST_PROD
    FROM [PDMVW].[WB_PROD_DAY]
    WHERE [GOV_FIELD_NAME] = '{field_name.strip().upper()}'
    GROUP BY [WB_UWBI]
    """
    return tools.query(sql)


def get_injection(field_name:str, wb_uwbi:str=None, from_date:str=None, until_date:str=None, columns=None):
    if columns is None:
        columns = '*'
    elif type(columns) is str:
        pass
    else:
        columns = ', '.join(columns)
    from_date = "" if from_date is None else f" AND [PROD_DAY] >= '{from_date}'"
    until_date = "" if until_date is None else f" AND [PROD_DAY] <= '{until_date}'"
    wb_uwbi = [wb_uwbi] if type(wb_uwbi) is str else wb_uwbi
    wb_uwbi = "" if wb_uwbi is None else f""" AND ([WB_UWBI] = '{"' OR [WB_UWBI] = '".join(wb_uwbi)}')"""
    sql = f"""
    SELECT {columns} 
    FROM [PDMVW].[WB_INJ_DAY]
    WHERE [GOV_FIELD_NAME] = '{field_name.strip().upper()}'{from_date}{until_date}{wb_uwbi}
    """
    return tools.query(sql)


def get_production(field_name:str, wb_uwbi:str=None, from_date:str=None, until_date:str=None, columns=None):
    if columns is None:
        columns = '*'
    elif type(columns) is str:
        pass
    else:
        columns = ', '.join(columns)
    from_date = "" if from_date is None else f" AND [PROD_DAY] >= '{from_date}'"
    until_date = "" if until_date is None else f" AND [PROD_DAY] <= '{until_date}'"
    wb_uwbi = [wb_uwbi] if type(wb_uwbi) is str else wb_uwbi
    wb_uwbi = "" if wb_uwbi is None else f""" AND ([WB_UWBI] = '{"' OR [WB_UWBI] = '".join(wb_uwbi)}')"""
    sql = f"""
    SELECT {columns} 
    FROM [PDMVW].[WB_PROD_DAY]
    WHERE [GOV_FIELD_NAME] = '{field_name.strip().upper()}'{from_date}{until_date}{wb_uwbi}
    """
    return tools.query(sql)
