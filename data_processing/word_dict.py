import pickle


def get_vocab(corpus1, corpus2):
    #初始化一个空集合，用于存储所有唯一的词汇
    word_vocab = set()
    #遍历两个语料库
    for corpus in [corpus1, corpus2]:
        #遍历语料库中的每个元素
        for i in range(len(corpus)):
            #更新词汇表集合以包含当前元素的指定结构中的所有词汇
            word_vocab.update(corpus[i][1][0])
            word_vocab.update(corpus[i][1][1])
            word_vocab.update(corpus[i][2][0])
            word_vocab.update(corpus[i][3])
    print(len(word_vocab))
    return word_vocab


def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


def vocab_processing(filepath1, filepath2, save_path):
    #从第一个文件读取词汇集并转换为集合
    with open(filepath1, 'r') as f:
        total_data1 = set(eval(f.read()))
    #从第二个文件读取词汇集
    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())
    #提取第二个文件的词汇集
    word_set = get_vocab(total_data2, total_data2)
    #计算两个词汇集的交集，并排除这部分词汇
    excluded_words = total_data1.intersection(word_set)
    word_set = word_set - excluded_words

    print(len(total_data1))
    print(len(word_set))

    with open(save_path, 'w') as f:
        f.write(str(word_set))


if __name__ == "__main__":
    python_hnn = './data/python_hnn_data_teacher.txt'
    python_staqc = './data/staqc/python_staqc_data.txt'
    python_word_dict = './data/word_dict/python_word_vocab_dict.txt'

    sql_hnn = './data/sql_hnn_data_teacher.txt'
    sql_staqc = './data/staqc/sql_staqc_data.txt'
    sql_word_dict = './data/word_dict/sql_word_vocab_dict.txt'

    new_sql_staqc = './ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql = './ulabel_data/sql_word_dict.txt'

    final_vocab_processing(sql_word_dict, new_sql_large, large_word_dict_sql)
