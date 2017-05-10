# HackRunningGo-SC
PC can run without legs. 😎

## Description

This python script can help you to add Running Records for your personal information. And the running route is so reasonable because we change others running route and recode.

## Fork Description

Some universities will score students' PE class based on the record of this application.

Therefore,I add a simple feature,which will allow you to add history running records.

You can add history running records by a single day as well as a specific timezone.

Have fun!

## Declaration

This project is not for profit, so our organization choose **opensource** for it. 
We hope our school to make a better app, it includes **encrypted transmission information**, **use tokens for authentication**, **irreversible encryption account password** and **more secure network interface**. We sincerely hope that the school software technology is getting better and better, and it is not like this. 😓

**So if you are like a 💩, we will fuck it. Thx.**


## Screenshot

<img src="/screenshot/ss.png" width="200px" />

## Operating environment

You need to install `python 2.7`. 
And we recommend you to use `terminal` or `bash` in Linux, `item` in macOS and `powershell` in Windows.

## Flow

### 1. Clone these repo(need git installed) or download the zip.

#### a.Clone the repo.

You need to deploy environment. 

```bash
git clone https://github.com/HackSwjtu/HackRunningGo-SC.git 
cd HackRunningGo-SC
```

#### b.Download the zip.

<image src="screenshot/ss3.png" width="400px" />

After download the zip,you need decompression it,and cd this dictionary.

### 2. Input your login id and password

Write your profile `id` and `password` to `user.data`.

```bash
bash \[id] [password] >> user.data
cat user.data
```

#### e.g

![](/screenshot/ss2.png)

Or you can also find `user.data` file and open it with notepad.Then write your `id` and `password` to it(support multiple users,one line for one user.).


### 3. Update running route static data. (optional)

You can run following command code to update the static running route data. It will update these files: `route.data` and `tp.data`.

```bash
python updateRoutes.py
```


### 4. Let's run! Hacking!

Run `HaRunGo.py`, and be happy! 

```bash
python HaRunGo.py
```

## MIT License

Copyright (c) 2016 Hack Swjtu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.







