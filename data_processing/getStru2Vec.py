import pickle
import multiprocessing
from python_structured import *
from sqlang_structured import *

#使用列表推导式，对列表中的每一行数据调用python_query_parse函数进行处理，最终返回一个新的列表，包含所有经过此函数处理后的数据
def multipro_python_query(data_list):
    return [python_query_parse(line) for line in data_list]

#使用列表推导式，对列表中的每一行代码调用python_code_parse函数进行解析或处理，最终返回一个新列表，其中包含所有经过此函数处理后的代码行
def multipro_python_code(data_list):
    return [python_code_parse(line) for line in data_list]

def multipro_python_context(data_list):
    result = [] #初始化一个空列表，用于存储处理后的结果
    for line in data_list: #遍历传入的数据列表，每个元素代表一行文本
        if line == '-10000': #检查当前行是否是特殊标记'-10000'
            result.append(['-10000']) #如果是，将包含'-10000'的列表添加到结果列表中
        else:
            #若不是特殊标记，则调用python_context_parse函数处理当前行
            result.append(python_context_parse(line))
            #将处理后的结果添加到结果列表中
    return result

#对列表中的每一行SQL查询语句调用sqlang_query_parse函数进行处理，最终返回一个新的列表，其中包含了所有经过sqlang_query_parse函数处理后的SQL查询结果
def multipro_sqlang_query(data_list):
    return [sqlang_query_parse(line) for line in data_list]

#使用列表推导式，对列表中的每一行SQL代码调用sqlang_code_parse函数进行解析或处理，最终返回一个新的列表，其中包含了所有经过sqlang_code_parse函数处理后的SQL代码行
def multipro_sqlang_code(data_list):
    return [sqlang_code_parse(line) for line in data_list]

def multipro_sqlang_context(data_list):
    result = [] #初始化一个空列表，用于存储处理后的结果
    for line in data_list: #遍历传入的数据列表，每个元素代表一行文本
        if line == '-10000': #检查当前行是否是特殊标记'-10000'
            result.append(['-10000']) #如果是这个特殊标记，将它作为列表添加到结果列表中
        else:
            #如果当前行不是特殊标记，调用sqlang_context_parse函数对其进行处理
            result.append(sqlang_context_parse(line))
            #将处理后的结果添加到结果列表中
    return result

def parse(data_list, split_num, context_func, query_func, code_func):
    pool = multiprocessing.Pool() #创建一个多进程的池以并行运行任务
    #将数据列表分割成较小的列表，每个小列表包含split_num数量的元素
    split_list = [data_list[i:i + split_num] for i in range(0, len(data_list), split_num)]
    #使用多进程池调用context_func函数处理每个小列表，并收集结果
    results = pool.map(context_func, split_list)
    #展开处理结果，将多个小列表合并成一个大列表
    context_data = [item for sublist in results for item in sublist]
    print(f'context条数：{len(context_data)}')

    #使用多进程池调用query_func函数处理每个小列表，并收集结果
    results = pool.map(query_func, split_list)
    #展开处理结果，将多个小列表合并成一个大列表
    query_data = [item for sublist in results for item in sublist]
    print(f'query条数：{len(query_data)}')

    #使用多进程池调用code_func函数处理每个小列表，并收集结果
    results = pool.map(code_func, split_list)
    #展开处理结果，将多个小列表合并成一个大列表
    code_data = [item for sublist in results for item in sublist]
    print(f'code条数：{len(code_data)}')

    #关闭多进程池，等待所有进程完成
    pool.close()
    pool.join()

    return context_data, query_data, code_data

def main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func):
    #打开并读取源数据文件
    with open(source_path, 'rb') as f:
        corpus_lis = pickle.load(f) #从文件中加载数据

    #调用parse函数处理原始数据，返回上下文、查询和代码数据
    context_data, query_data, code_data = parse(corpus_lis, split_num, context_func, query_func, code_func)
    #从原始数据中提取每项数据的ID
    qids = [item[0] for item in corpus_lis]

    #组合数据ID、上下文、代码和查询信息为一个新的数据集
    total_data = [[qids[i], context_data[i], code_data[i], query_data[i]] for i in range(len(qids))]

    #打开目标文件，并将处理后的数据集保存到指定路径
    with open(save_path, 'wb') as f:
        pickle.dump(total_data, f)

if __name__ == '__main__':
    staqc_python_path = '.ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_save = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.pkl'

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_save = './ulabel_data/staqc/sql_staqc_unlabled_data.pkl'

    main(python_type, split_num, staqc_python_path, staqc_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main(sqlang_type, split_num, staqc_sql_path, staqc_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)

    large_python_path = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    large_python_save = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.pkl'

    large_sql_path = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    large_sql_save = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.pkl'

    main(python_type, split_num, large_python_path, large_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main(sqlang_type, split_num, large_sql_path, large_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)
