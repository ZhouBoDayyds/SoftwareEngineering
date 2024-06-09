import pickle
import numpy as np
from gensim.models import KeyedVectors


# 将文本格式的词向量文件转换为二进制格式的文件。在这里使用的是Gensim库最终得Word2Vec模型工具来加载和处理词向量
def trans_bin(path1, path2):
    wv_from_text = KeyedVectors.load_word2vec_format(path1, binary=False)
    # 如果每次都用上面的方法加载，速度非常慢，可以将词向量文件保存成bin文件，以后就加载bin文件，速度会变快
    wv_from_text.init_sims(replace=True)
    wv_from_text.save(path2)


# 构建新的词典和词向量矩阵
def get_new_dict(type_vec_path, type_word_path, final_vec_path, final_word_path):
    #加载预训练的词向量模型
    model = KeyedVectors.load(type_vec_path, mmap='r')

    #读取词汇列表文件，并将其转换为列表
    with open(type_word_path, 'r') as f:
        total_word = eval(f.read())

    #初始化词典，包含特殊符号
    #'PAD'用于填充，'SOS'表示开始，'EOS'表示结束，'UNK'表示未知词
    word_dict = ['PAD', 'SOS', 'EOS', 'UNK']  #分别分配ID：0,1,2,3

    #记录未能在模型中找到的词
    fail_word = []
    #随机数生成器，用于创建未知词的词向量
    rng = np.random.RandomState(None)
    #创建特殊词的词向量
    pad_embedding = np.zeros(shape=(1, 300)).squeeze()
    unk_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
    sos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
    eos_embedding = rng.uniform(-0.25, 0.25, size=(1, 300)).squeeze()
    #将特殊词的词向量添加到词向量列表中
    word_vectors = [pad_embedding, sos_embedding, eos_embedding, unk_embedding]

    #遍历词汇列表中的每个词，并获取其词向量
    for word in total_word:
        try:
            word_vectors.append(model.wv[word])  #从模型中获取词向量
            word_dict.append(word) #将词添加到词典中
        except:
            fail_word.append(word) #若词不在模型中，则记录

    #将词向量列表转换为数组形式
    word_vectors = np.array(word_vectors)
    #创建词典，键是词，值是对应的索引
    word_dict = dict(map(reversed, enumerate(word_dict)))

    #将词向量矩阵保存到文件
    with open(final_vec_path, 'wb') as file:
        pickle.dump(word_vectors, file)

    #将词典保存到文件
    with open(final_word_path, 'wb') as file:
        pickle.dump(word_dict, file)

    print("完成")


# 得到词在词典中的位置
def get_index(type, text, word_dict):
    location = []
    #若输入类型为'code'，处理代码相关的文本
    if type == 'code':
        location.append(1) #在列表开头添加1表示这是代码类型
        len_c = len(text)
        #若文本长度加1小于350
        if len_c + 1 < 350:
            #若文本长度为1且文本内容为'-1000'
            if len_c == 1 and text[0] == '-1000':
                location.append(2) #添加2到列表，特殊情况处理
            else:
                #遍历文本中的每个词
                for i in range(0, len_c):
                    #从词典中获取当前词的索引，如果不存在则使用'UNK'的索引
                    index = word_dict.get(text[i], word_dict['UNK'])
                    location.append(index) #将索引添加到列表中
                location.append(2) #在列表末尾添加2表示结束
        else:
            #若文本长度加1大于或等于35-
            for i in range(0, 348):
                #只处理前348个词，并获取它们的索引
                index = word_dict.get(text[i], word_dict['UNK'])
                location.append(index)
            location.append(2) #在列表末尾添加2表示结束
    else:
        #若输入类型不是'code'，处理非代码相关的文本
        if len(text) == 0:
            location.append(0) #如果文本为空，添加0到列表
        elif text[0] == '-10000':
            location.append(0) #若文本的第一个元素是'-10000'，添加0到列表
        else:
            #遍历文本中的每个词
            for i in range(0, len(text)):
                #从词典中获取当前词的索引，如果不存在则使用'UNK'的索引
                index = word_dict.get(text[i], word_dict['UNK'])
                location.append(index) #将索引添加到列表中

    return location


# 将训练、测试、验证语料序列化
# 查询：25 上下文：100 代码：350
def serialization(word_dict_path, type_path, final_type_path):
    #从文件加载词典
    with open(word_dict_path, 'rb') as f:
        word_dict = pickle.load(f)

    #从文件加载语料库
    with open(type_path, 'r') as f:
        corpus = eval(f.read())

    total_data = [] #用于存储处理后的数据

    #遍历语料库中的每个数据项
    for i in range(len(corpus)):
        qid = corpus[i][0] #获取查询ID

        #处理不同部分的文本，将它们转换为索引列表
        Si_word_list = get_index('text', corpus[i][1][0], word_dict) #句子Si
        Si1_word_list = get_index('text', corpus[i][1][1], word_dict) #句子Si+1
        tokenized_code = get_index('code', corpus[i][2][0], word_dict) #代码片段
        query_word_list = get_index('text', corpus[i][3], word_dict) #查询文本
        block_length = 4
        label = 0

        #对索引列表进行长度限制和填充处理
        Si_word_list = Si_word_list[:100] if len(Si_word_list) > 100 else Si_word_list + [0] * (100 - len(Si_word_list))
        Si1_word_list = Si1_word_list[:100] if len(Si1_word_list) > 100 else Si1_word_list + [0] * (100 - len(Si1_word_list))
        tokenized_code = tokenized_code[:350] + [0] * (350 - len(tokenized_code))
        query_word_list = query_word_list[:25] if len(query_word_list) > 25 else query_word_list + [0] * (25 - len(query_word_list))

        #组合处理后的数据
        one_data = [qid, [Si_word_list, Si1_word_list], [tokenized_code], query_word_list, block_length, label]
        total_data.append(one_data) #添加到总数据列表中

    #将处理后的数据保存到文件
    with open(final_type_path, 'wb') as file:
        pickle.dump(total_data, file)


if __name__ == '__main__':
    # 词向量文件路径
    ps_path_bin = '../hnn_process/embeddings/10_10/python_struc2vec.bin'
    sql_path_bin = '../hnn_process/embeddings/10_8_embeddings/sql_struc2vec.bin'

    # ==========================最初基于Staqc的词典和词向量==========================

    python_word_path = '../hnn_process/data/word_dict/python_word_vocab_dict.txt'
    python_word_vec_path = '../hnn_process/embeddings/python/python_word_vocab_final.pkl'
    python_word_dict_path = '../hnn_process/embeddings/python/python_word_dict_final.pkl'

    sql_word_path = '../hnn_process/data/word_dict/sql_word_vocab_dict.txt'
    sql_word_vec_path = '../hnn_process/embeddings/sql/sql_word_vocab_final.pkl'
    sql_word_dict_path = '../hnn_process/embeddings/sql/sql_word_dict_final.pkl'

    # get_new_dict(ps_path_bin, python_word_path, python_word_vec_path, python_word_dict_path)
    # get_new_dict(sql_path_bin, sql_word_path, sql_word_vec_path, sql_word_dict_path)

    # =======================================最后打标签的语料========================================

    # sql 待处理语料地址
    new_sql_staqc = '../hnn_process/ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large = '../hnn_process/ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql = '../hnn_process/ulabel_data/sql_word_dict.txt'

    # sql最后的词典和对应的词向量
    sql_final_word_vec_path = '../hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl'
    sqlfinal_word_dict_path = '../hnn_process/ulabel_data/large_corpus/sql_word_dict_final.pkl'

    # get_new_dict(sql_path_bin, final_word_dict_sql, sql_final_word_vec_path, sql_final_word_dict_path)
    # get_new_dict_append(sql_path_bin, sql_word_dict_path, sql_word_vec_path, large_word_dict_sql, sql_final_word_vec_path,sql_final_word_dict_path)

    staqc_sql_f = '../hnn_process/ulabel_data/staqc/seri_sql_staqc_unlabled_data.pkl'
    large_sql_f = '../hnn_process/ulabel_data/large_corpus/multiple/seri_ql_large_multiple_unlable.pkl'
    # Serialization(sql_final_word_dict_path, new_sql_staqc, staqc_sql_f)
    # Serialization(sql_final_word_dict_path, new_sql_large, large_sql_f)

    # python
    new_python_staqc = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.txt'
    new_python_large = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.txt'
    final_word_dict_python = '../hnn_process/ulabel_data/python_word_dict.txt'
    large_word_dict_python = '../hnn_process/ulabel_data/python_word_dict.txt'

    # python最后的词典和对应的词向量
    python_final_word_vec_path = '../hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl'
    python_final_word_dict_path = '../hnn_process/ulabel_data/large_corpus/python_word_dict_final.pkl'

    # get_new_dict(ps_path_bin, final_word_dict_python, python_final_word_vec_path, python_final_word_dict_path)
    # get_new_dict_append(ps_path_bin, python_word_dict_path, python_word_vec_path, large_word_dict_python, python_final_word_vec_path,python_final_word_dict_path)

    # 处理成打标签的形式
    staqc_python_f = '../hnn_process/ulabel_data/staqc/seri_python_staqc_unlabled_data.pkl'
    large_python_f = '../hnn_process/ulabel_data/large_corpus/multiple/seri_python_large_multiple_unlable.pkl'
    # Serialization(python_final_word_dict_path, new_python_staqc, staqc_python_f)
    serialization(python_final_word_dict_path, new_python_large, large_python_f)

    print('序列化完毕')
    # test2(test_python1,test_python2,python_final_word_dict_path,python_final_word_vec_path)
