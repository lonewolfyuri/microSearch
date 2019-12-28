from collections import defaultdict, OrderedDict




if __name__ == "__main__":
    index = defaultdict(OrderedDict)
    for ndx in range(4):
        temp_index = dict()
        with open("temp_index_" + str(ndx) + ".txt") as iFile:
            temp_index = eval(iFile.read()[11:].replace("<class 'collections.OrderedDict'>, ", ""))
        for term, o_dict in temp_index.items():
            for document_id, values in o_dict.items():
                index[term][document_id] = values
    print(str(index))
