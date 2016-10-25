# HackRunningGo-SC
PC can run without legs. 😎

## Description

This python script can help you to add Running Records for your personal personal information. And the running route is so reasonable because we change others running route and recode.

## Screenshot

![](/screenshot/ss.png)

## Operating environment

You need to install `python 2.7`. 
And we recommend you to use `terminal` or `bash` in Linux, `item` in macOS and `powershell` in Windows.

## Flow

### 1. Clone these repo.

You need to deploy environment. 

```bash
git clone https://github.com/HackSwjtu/HackRunningGo-SC.git 
cd HackRunningGo-SC
```

### 2. Update running route static data. (optional)

You can run following command code to update the static running route data. It will update these files: `route.data` and `tp.data`.

```bash
python updateRoutes.py
```

### 3. Input your login id and password

Write your profile `id` and `password` to `user.data`.

```bash
bash \n[id] [password] >> user.data
cat user.data
```

#### e.g

![](/screenshot/ss2.png)

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







