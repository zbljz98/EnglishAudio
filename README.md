# EnglishAudio
A create English words audio file program
一个创建英语单词音频的小程序，音频源为剑桥官网

# 功能(Functions)
1. 从剑桥网站查询单词获取英式英语的读音链接
2. 可以选择是否保存单词单词的读音文件
3. 生成词汇音频文件时，可以设定是否重复、重复的次数、单词间隔时间
4. 可选择是否对单词进行排序，因为大部分词汇书都是这个顺序，排序后方便使用，但存在弊端
5. 重复的单词将只保留一个，且会给予提示
6. 可以选择是否自动分节（当单词超过20个后，每20个单词分为一个listen文件）
7. 音频文件生成成功后，会生成一个result文件，保存爬取的结果

# 如何使用
## windows
1. 从右侧release中下载EnglishAudio.exe文件，并下载项目中的ffmpeg压缩包
2. 下载项目中的ffmpeg文件，解压缩后添加到系统的环境变量中
3. 运行EnglishAudio.exe文件，如出现下图提示，请检查ffmpeg的环境变量时候正确
![image](https://user-images.githubusercontent.com/31961185/113503263-495c0380-9563-11eb-9699-e748eeadb388.png)
4. 若没出现提升，按照程序提示操作即可

# 已存在问题
1. 部分单词是存在的但是在剑桥网站上无法查询，所以不能获取链接
2. 所有复数的单词，均是单数的读音

# 待改进
1. 用户可以选择，音频文件是否保存在一个文件夹内而不是在当前目录下载生成
