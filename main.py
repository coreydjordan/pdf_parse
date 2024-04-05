import PyPDF2
import re
import pandas as pd
import os

def pdf_pull():
    pdfFileObj = open(r"C:\Users\C974776\OneDrive - Constellation\Desktop\python tools\Carla\Files\SMBCNE0624_3N_SE DUE 3-18-24_TX_newSMBRenewals_20240327.pdf", 'rb')
    account_numbers = []
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    for i in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[i]
        extracted_text = pageObj.extract_text()
        n_list = extracted_text.split()

    #--------   get account numbers from first page -----------

        if len(n_list) > 0 and "#" in n_list:
            acct_index = n_list.index("#")
            next_el = n_list[acct_index + 1]
            if next_el.isdigit():
                account_numbers.append(next_el)

    # #--------   get account numbers from second page -----------

        if len(n_list) > 1 and n_list[0] == "UDC":
            for item in n_list:
                if item.isdigit() and len(item) >= 10:
                    # print(item)
                    account_numbers.append(item)
                if "-" in item and len(item) > 15:
                    account_numbers.append(item[10:])
                if len(item) > 20 and item.isdigit() == True:
                    account_numbers.append(item[5:])
                    account_numbers.remove(item)


    # #--------   get account numbers with letters and characters -----------

        for a in n_list:
            pe_num = re.compile(r"[A-Za-z]+[0-9]+", re.IGNORECASE)
            if len(a) >= 15 and len(a) < 23 and pe_num.match(a) and a not in account_numbers:
                account_numbers.append(a)


    #------ ensure there are no duplicates or empty strings -------
    # account_numbers = list(set((account_numbers)))
    # for number in account_numbers:
    #     if len(number) > 24:
    #         account_numbers.append(number[4:])
    #         account_numbers.remove(number)
    # for n in account_numbers:
    #     if len(n) < 1:
    #         account_numbers.remove(n)


    #------- extract data from excel -------

    df = pd.read_excel(r"C:\Users\C974776\OneDrive - Constellation\Desktop\python tools\Carla\Files\SMBCNE0624_3N_SE DUE 3-18-24.xlsx")

    # # #------ delete columns that aren't the ldc account number -------

    df.drop(df.columns.difference(["LDC Account"]), axis=1, inplace=True)

    # #------turn column into list -------

    df_list = df["LDC Account"].tolist()
    for acct in account_numbers:
        if acct in account_numbers and acct in df_list:
            print(acct)
    # difference = list(set(account_numbers) - set(df_list))
    # print(difference)

    # in_excel_not_pdfs = []
    # in_pdfs_not_excel = []

    # # #------- find differences -------

    # for li in df_list:
    #     if li not in account_numbers:
    #         in_excel_not_pdfs.append(li)
    # for an in account_numbers:
    #     if an not in df_list:
    #         in_pdfs_not_excel.append(an)


    # if len(in_excel_not_pdfs) == 0 and len(in_pdfs_not_excel) == 0:
    #     print("There are no differences")
    # else:
    #     print("These are in excel, but not in pdfs: ", in_excel_not_pdfs, len(in_excel_not_pdfs))
    #     print("These are in pdfs, but not excel: ", in_pdfs_not_excel, len(in_pdfs_not_excel))

pdf_pull()
