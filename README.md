# 软件工程完美编程

[TOC]
## 一、项目说明
```
|── data_processing  
│     └── embeddings_process.py  
│     └── getStru2Vec.py
│     └── process_single_corpus.py
│     └── python_structured.py
│     └── sqlang_structured.py
│     └── word_dict.py  
```
此仓库用于为原始代码添加注释，提高代码的可读性。
***

## 二、文件说明
### embeddings_process.py文件
#### 1.概述
处理和准备文本数据，以便它们可以被用于自然语言处理（NLP）任务，特别是那些涉及词向量和词汇索引的任务。
#### 2.具体功能
* `trans_bin`函数：将文本格式的词向量文件转换为二进制格式的文件。在这里使用的是Gensim库最终得Word2Vec模型工具来加载和处理词向量。
* `get_new_dict`函数：加载预训练的词向量模型和一个词汇列表，初始化包含特殊符号的词字典。为每个词汇创建或获取词向量，并将这些向量和对应的词汇保存到新的文件中。若有词汇未找到对应的词向量，则记录下来，并在结束时打印“完成”信息。
* `get_index`函数：根据输入的类型、文本和词典，生成一个包含索引的列表。首先检查文本时代码类型还是其他类型，然后根据给定的词典将文本中的每个词转换为相应的索引。若文本长度超过了特定的限制，或遇到特定标记，函数会进行相应处理。最终，函数返回生成的索引列表。
* `serialization`函数：从指定的文件中加载一个词典和一个语料库，遍历语料库中的每个数据项，针对每个数据项的不同文本部分使用`get_index`函数将文本转换为索引列表。然后根据需要对这些索引列表进行长度限制和填充处理，以确保它们符合特定的长度要求。最后将处理之后的数据组合在一起，并保存到另一个指定的文件中。
***

### getStru2Vec.py文件
#### 1.概述
设置了一个通用的数据处理流程，可以应用于不同的编程语言和数据集。通过使用多进程来加速数据处理，使得大量数据的处理成为可能。处理完的数据适用于进一步的机器学习或数据分析任务。
#### 2.具体功能
* `multipro_python_query`函数：解析或处理单行python查询。
* `multipro_python_code`函数：解析或处理单行python代码。
* `multipro_python_context`函数：处理一个包含多行文本的数据列表data_list。每一行文本都被检查是否是特定的标记，如果是这个特殊标记，函数会将这个标记作为一个单独的列表元素添加到结果列表中；如果文本不是这个特殊标记，它会调用`python_context_parse`函数处理这行文本，并将处理结果添加到结果列表中。负责对上下文信息进行解析或处理。
* `multipro_sqlang_query`函数：批量处理一系列的SQL查询语句。
* `multipro_sqlang_code`函数：批量处理一系列的SQL代码片段。
* `multipro_sqlang_context`函数：处理一个包含多行文本的数据列表data_list。它会检查每一行文本是否与特定的标记匹配，若是，则它会将这个标记作为一个单独的列表元素添加到结果列表result中；若不是，它会调用`sqlang_context_parse`函数来处理这行文本，并将结果添加到结果列表中。负责解析或处理SQL上下文信息。
* `parse`函数：创建一个进程池，将数据列表data_list分割为多个较小的列表，每个小列表包含split_num元素。使用多进程池并行地对这些小列表应用三个不同的处理函数，分别用于处理不同类型的数据。每个函数的结果被展开并合并成一个大列表，函数打印出每种数据类型处理后的条目数量，并在所有进程完成后关闭进程池。
* `main`函数：主函数，从指定路径读取原始数据集，处理这些数据，并将处理后的数据保存到新的文件中。
***

### process_single_corpus.py文件
#### 1.概述
针对编程问题数据集进行了一系列的处理步骤，包括数据加载、分割、保存和标记
#### 2.具体功能
* `load_pickle`函数：从指定的pickle文件中加载数据。
* `split_data`函数：将数据集根据查询ID分为两部分：一部分是每个查询ID对应的数据只出现一次的数据集，另一部分是某些查询ID对应多条数据的数据集。
* `data_staqc_processing`函数：处理STAQC数据集，并将其分为两个部分：一个是每个查询ID只对应一条数据的部分，另一个是一个查询ID对应多条数据的部分。
* `data_large_processing`函数：处理存储在pickle文件中的大型数据集。
* `single_unlabeled_to_labeled`函数：读取一个未标记的数据集，为每个数据项添加一个固定的标签，然后将添加标签后的数据按照一定的顺序保存到一个新的文件中。
***

### python_structured.py文件
#### 1.概述
用来进行自然语言处理和源代码分析的工具，结合了正则表达式、自然语言处理和抽象语法树解析，能够处理和解析Python代码和自然语言查询，提取有用的信息。
#### 2.具体功能
* `repair_program_io`函数：修复输入输出格式，尤其是处理来自不同编程环境的代码片段。
* `get_vars`函数：遍历整个AST，收集所有的变量名。
* `get_vars_heuristics`函数：采用启发式方法从给定的Python代码字符串中提取变量名。
* `PythonParser`函数：解析Python代码字符串，并返回代码的标记化表示。
* `revert_abbrev`函数：将英文缩写还原为完整形式。
* `get_wordpos`函数：将词性标记转换为WordNet中对应的词性常量。
* `process_nl_line`函数：对自然语言文本进行一系列预处理步骤。
* `process_sent_word`函数：对给定的文本执行一系列自然语言处理操作，包括分词、替换特定模式、词性标注和词形还原。
* `filter_all_invachar`函数：清除文本中的非常用字符，以避免在后续的文本解析过程中出现错误。
* `filter_part_invachar`函数：清除文本行中的部分非常用字符，防止在文本解析过程中出现误解。
* `python_code_parse`函数：解析python代码行并转换为一组标准化的标记。
* `python_query_parse`函数：用于解析python查询语句。
* `python_context_parse`函数：解析python代码或查询语句的上下文。
***

### sqlang_structured.py文件
#### 1.概述
将SQL语句和自然语言句子转换为标准化的、易于分析的格式。
#### 2.具体功能
* `tokenizeRegex`函数：将输入的字符串按照预定义的规则进行分词，用于进一步的文本处理或分析。
* `sanitizeSql`函数：接受一个SQL语句字符串作为输入，然后进行一系列的清理和规范化处理，以确保SQL语句符合特定的格式要求。
* `parseStrings`函数：处理SQL语句中的字符串Token。
* `renameIdentifiers`函数：遍历和重命名SQL语句中的标识符。
* `getTokens`函数：接受由sqlparse库解析SQL语句后得到的解析对象列表作为输入，然后遍历这些对象，将它们平铺以提取出所有的Token。
* `removeWhitespaces`函数：递归地移出由sqlparse库解析SQL语句后得到的TokenList中的所有空白Token。
* `identifySubQueries`函数：递归地识别并标记SQL语句中的子查询。
* `identifyLiterals`函数：遍历由sqlparse库解析后得到的TokenList中的每个Token，识别SQL语句中的各种字面量类型，并对这些Token进行相应的标记。
* `identifyFunctions`函数：在由sqlparse库解析后得到的TokenList中标识SQL函数。
* `identifyTables`函数：在由sqlparse库解析后得到的TokenList中标识SQL语句中的表名。
* `revert_abbrev`函数：将英文字符串中的缩略语展开为完整形式。
* `get_wordpos`函数：根据传入的词性标记来返回相应的WordNet词性。
* `process_nl_line`函数：对给定的英文句子进行预处理，包括展开缩略语、去除多余的空格和换行符、转换命名风格、去除括号内的内容等，以便句子能更好地用于文本处理或自然语言处理任务。
* `process_sent_word`函数：对给定的句子进行预处理和词性还原。
* `filter_all_invachar`函数：清理输入字符串中的非常用字符，确保文本解析不会因为包含特殊字符而出错。
* `ilter_part_invachar`函数：清除输入字符串中的部分非常用字符。
* `sqlang_code_parse`函数：对输入的SQL语句进行预处理和解析。
* `sqlang_query_parse`函数：对SQL查询语句进行预处理和词语处理。
* `sqlang_context_parse`函数：对SQL语句的上下文进行预处理和词语处理。
***

### word_dict.py文件
#### 1.概述
从特定的数据集中提取和处理词汇表，并将处理后的词汇表保存到文件中。
#### 2.具体功能
* `get_vocab`函数：从两个语料库中提取并返回所有唯一的词汇。
* `load_pickle`函数：从指定的pickle文件中加载数据。
* `vocab_processing`函数：处理两个文件中的词汇表，并将最终得到的词汇集保存到指定的文件路径。
***
