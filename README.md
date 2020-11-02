# cars_search_engine

## 项目简介: 

汽车新闻搜索引擎, 项目采用elasticsearch收录了柯林斯大词典20w+的词汇词组, 10w+汽车之家的汽车新闻, 实现了搜索引擎的效果. 如果是英文单词的输入, 会有推荐搜索和纠错建议. 项目内部编写了爬虫程序和爬取到的数据, 可扩展搜索内容.

## 注意事项: 

### 前期准备 ( 下载es, Java jdk, kibana, ik分词器)

+ 链接：https://pan.baidu.com/s/12tgQ_9ueNlpV1Qs54wvKEw 
  提取码：kpk5 

### es环境配置

+ 首先安装 Java jdk
  + JAVA_HOME
  + 配置 path
+ 然后管理员身份运行bin目录下的bat文件安装es
+ 同上原理安装kibana
  + kibana 一个为es提供数据分析的web接口. 可使用它对日志进行高效的搜索, 可视化, 分析等操作(类似于mysql的客户端)
+ 注意: kibana和es, ik分词版本保持一致

### 启动es和kibana

+ es目录下管理员身份执行elasticsearch.bat

+ kibana目录下管理员身份执行kibana.bat

### 启动项目

+ 先通过 data_save.py 往 es 存储数据 (读取的文件是我先前爬取好的数据, 如有需要也可以自己修改爬虫文件爬取想要的数据)
+ 启动搜索引擎Django项目即可

