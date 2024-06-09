import pickle
from collections import Counter


def load_pickle(filename):
    #以二进制方式打开文件
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='iso-8859-1')
    return data


def split_data(total_data, qids):
    #使用Counter统计qids中每个元素出现的次数
    result = Counter(qids)
    #初始化一个空列表，用于存储包含唯一查询ID的数据
    total_data_single = []
    #初始化一个空列表，用于存储包含多个相同查询ID的数据
    total_data_multiple = []
    #遍历total_data中的每个数据
    for data in total_data:
        #如果当前数据的查询ID在qids中唯一出现，将当前数据添加到total_data_single列表中
        if result[data[0][0]] == 1:
            total_data_single.append(data)
        #否则，将当前数据添加到total_data_multiple列表中
        else:
            total_data_multiple.append(data)
    return total_data_single, total_data_multiple


def data_staqc_processing(filepath, save_single_path, save_multiple_path):
    #打开原始数据文件，并读取其内容
    with open(filepath, 'r') as f:
        #将文件中的字符串内容转换成相应的数据结构
        total_data = eval(f.read())
    #从总数据中提取所有查询ID
    qids = [data[0][0] for data in total_data]
    #调用split_data函数分离处包含唯一查询ID的数据和包含多个相同查询ID的数据
    total_data_single, total_data_multiple = split_data(total_data, qids)

    #将包含唯一查询ID的数据保存到指定的文件中
    with open(save_single_path, "w") as f:
        f.write(str(total_data_single))
    #将包含多个相同查询ID的数据保存到另一个指定的文件中
    with open(save_multiple_path, "w") as f:
        f.write(str(total_data_multiple))


def data_large_processing(filepath, save_single_path, save_multiple_path):
    #使用load_pickle函数加载指定路径的pickle文件
    total_data = load_pickle(filepath)
    #从总数据中提取所有查询ID
    qids = [data[0][0] for data in total_data]
    #调用split_data函数分离处包含唯一查询ID的数据和包含多个相同查询ID的数据
    total_data_single, total_data_multiple = split_data(total_data, qids)

    #将包含唯一查询ID的数据序列化并保存到指定的pickle文件中
    with open(save_single_path, 'wb') as f:
        pickle.dump(total_data_single, f)
        #将包含多个相同查询ID的数据序列化并保存到另一个指定的pickle文件中
    with open(save_multiple_path, 'wb') as f:
        pickle.dump(total_data_multiple, f)


def single_unlabeled_to_labeled(input_path, output_path):
    #使用load_pickle函数加载输入路径的pickle文件
    total_data = load_pickle(input_path)
    #为每个数据项添加标签1，构成一个新的列表，每个元素都是一个包含原始数据第一项和标签1的列表
    labels = [[data[0], 1] for data in total_data]
    #根据每个元素的第一项和第二项，对列表进行排序
    total_data_sort = sorted(labels, key=lambda x: (x[0], x[1]))
    #将排序后的数据转换为字符串，并写入到指定的输出文件中
    with open(output_path, "w") as f:
        f.write(str(total_data_sort))


if __name__ == "__main__":
    staqc_python_path = './ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_single_save = './ulabel_data/staqc/single/python_staqc_single.txt'
    staqc_python_multiple_save = './ulabel_data/staqc/multiple/python_staqc_multiple.txt'
    data_staqc_processing(staqc_python_path, staqc_python_single_save, staqc_python_multiple_save)

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_single_save = './ulabel_data/staqc/single/sql_staqc_single.txt'
    staqc_sql_multiple_save = './ulabel_data/staqc/multiple/sql_staqc_multiple.txt'
    data_staqc_processing(staqc_sql_path, staqc_sql_single_save, staqc_sql_multiple_save)

    large_python_path = './ulabel_data/python_codedb_qid2index_blocks_unlabeled.pickle'
    large_python_single_save = './ulabel_data/large_corpus/single/python_large_single.pickle'
    large_python_multiple_save = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    data_large_processing(large_python_path, large_python_single_save, large_python_multiple_save)

    large_sql_path = './ulabel_data/sql_codedb_qid2index_blocks_unlabeled.pickle'
    large_sql_single_save = './ulabel_data/large_corpus/single/sql_large_single.pickle'
    large_sql_multiple_save = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    data_large_processing(large_sql_path, large_sql_single_save, large_sql_multiple_save)

    large_sql_single_label_save = './ulabel_data/large_corpus/single/sql_large_single_label.txt'
    large_python_single_label_save = './ulabel_data/large_corpus/single/python_large_single_label.txt'
    single_unlabeled_to_labeled(large_sql_single_save, large_sql_single_label_save)
    single_unlabeled_to_labeled(large_python_single_save, large_python_single_label_save)
