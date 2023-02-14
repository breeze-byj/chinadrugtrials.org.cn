**_CDE&CFDI采集_**
=======
                                   __________  _________     ________________  ____
                                  / ____/ __ \/ ____( _ )   / ____/ ____/ __ \/  _/
                                 / /   / / / / __/ / __ \/|/ /   / /_  / / / // /  
                                / /___/ /_/ / /___/ /_/  </ /___/ __/ / /_/ // /   
                                \____/_____/_____/\____/\/\____/_/   /_____/___/
### 文件说明
    SourCode -> 项目名称

    --|data_input -> 格式化文件及数据保存路径

        ----|CDE/cde_export -> 数据保存路径

        ----|CDE/site_std -> site格式化文件存放路径

        ----|CDE/sponsor_std -> sponsor格式化文件存放路径

    --|pipeline -> spider脚本及格式化脚本路径

        ----|beian_data_collection.py

        ----|cde_data_collection.py -> 提取cde网站的脚本

        ----|cfdi_data_collection.py -> 提取cfdi网站的脚本

        ----|dqs_data_collection.py

        ----|phase_std.py -> phase格式化脚本

        ----|site_std.py

        ----|sponsor_std.py -> sponsor格式化脚本

        ----|scheme_no_std.py -> scheme_no格式化脚本

    --|utils -> 封装方法及replace配置文件存放路径

        ----|constants.py -> 各种文件的相对路径

        ----|encapsulation.py -> 封装的方法

        ----|insert_tit.py -> 文件表头写入方法及循环文件夹去重方法的封装

        ----|replace.ini -> replace数据的配置文件

    cde_main.py -> 脚本启动文件

### replace.ini
    所有replace操作都会在此文件中存放
    数据存放方式为:
        [组]
            项 = [['被处理数据','处理后结果'],['','']...]
    使用方式:
        处理结果str = conf_eval_data('组', '项', 需要格式化的文本)

### 操作说明
    1. 启动:直接启动cde_main.py文件即可同时采集cde/cfdi全量数据
    2. 数据处理:采集完成后自动写入title,去重,格式化并打包
    3. 文件存储:采集完成后的文件全部存入cde_export目录,生成的压缩文件.zip在项目根目录显示
    4. 可以根据需求,在项目运行前是否对上一批的数据.csv进行自动删除,若不进行自动删除则在项目启动前建议手动删除
    注: title写入,格式化等后置处理,如果需要重新处理,需要将源文件中的stand_**数据删除防止数据格式化不完善

### 脚本翻页:
    cde_data_collection.py: 若脚本在项目中途因异常情况需手动暂停或自动终止时,只需要修改for page in tqdm(range(0, page_count))起始参数即可,
    如:在10页程序终止,修改参数为当前终止时的页数-1 即:for page in tqdm(range(9, page_count))
    程序执行完毕后请将参数重新改为0
```python
for page in tqdm(range(0, page_count)):
    '''
        # 遍历获取到的总页数
        # range(
                0 : 若程序中途手动停止,再次运行时需手动修改为停止的页数-1实现续爬,不需要考虑重复问题
                page_count : 总页数,自动获取
                ) 
    '''
```

### 选择提取的数据:
    CDE/CFDI某部分数据不需要提取时注释
```python
def thread_start():
    start_time = time.time()
    # 将cde/cfdi存入线程组
    threads_list = []
    threads_list.append(Thread(target=run_cde))
    threads_list.append(Thread(target=run_cfdi))
    # 遍历线程组并执行
    for thread in threads_list:
        thread.start()
    print(f'程序结束,耗时:{time.time() - start_time}')
```

### 文件删除:
    根据需求,程序执行前是否对上一批次的csv文件进行删除(只会对 cde_export/* 下的.csv文件进行删除)
```python
delete_all_csv()
```

### 采集耗时:
    采集时间约为70min,采集时的网络环境,文本的解析速度及服务器配置等均会影响脚本的采集速度,所以此时长仅作为参考

### 注意事项:
    采集时请务必关闭VPN,CFDI数据采集时如果vpn没有关闭则会请求报错

### 
.
.
.
.
.