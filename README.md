# performance case viewer

**Performance case viewer** is a static web page generation tool for test result display. It can generate beautiful static web pages according to the file directory structure where the tool is located.

It has the following characteristics:

- The generated web page is static and can be opened directly with a browser
- The generation operation is very simple, only need to execute a unique script, and do not need to enter any parameters
- Support sheet display
- Support add as many number of directories as you can according to the rules

## core mechanism

The core mechanism of the tool is to retrieve all the folders where the tool is located through a script, and dynamically generate all web pages by referencing the html template. The hierarchical relationship of the web page corresponding to the hierarchical relationship of the directory. The tools directory is a three-level directory structure. The folder under the directory where the script is located is called the test class, which is the first-level directory structure. The folder under each test class is called a test item, which is the second-level directory structure. Several test pictures can be placed under the folder of each test item, which is the third-level directory structure.

## how to add case

The following file list is a test class that has been added

```txt
├── example
│   ├── case1
│   │   ├── cat.jpg
│   │   ├── lu.jpg
│   ├── case2
│   │   ├── mon.jpg
│   ├── example.png
│   └── example.sheet
├── out_pages
└── setup.py
```

You can add your test class or test item according to the operation similar to the following shell command. The following command line operation adds a cpu test class. under cpu test class, added case1,case2,case3 three test items, under test item case1, added a picture named 123.png

```shell
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ ls
README.md  casepage.templete  detailpage.templete  example  homepage.templete  out_pages  setup.py
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ ./setup.py
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ ls
README.md  casepage.templete  detailpage.templete  example  homepage.templete  out_pages  setup.py
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ mkdir cpu
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ cd cpu/
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer/cpu$ mkdir case1 case2 case3
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer/cpu$ cd case1/
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer/cpu/case1$ cp xxxx 123.png
```

### add a picture for test class

As the following operation, a picture named example.png is placed in the example test class directory.
This picture will be automatically referenced as the theme picture of the test class. Only **png,jpg,svg** are supported.

```shell
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ cd example/
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer/example$ cp xxxx example.png
case1  case2  example.png  example.sheet
```

### add a sheet for test class

```shell
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer$ cd example/
haochen@DESKTOP-7GLE6OA:~/workspace/case-viewer/example$ touch example.sheet
case1  case2  example.png  example.sheet
```

The text format of the sheet is as follows, each row in .sheet file corresponds to a row of the sheet, and each cell is separated by '|'. The file's suffix must be **.sheet**

```text
case name | case status | case detail
case1 | ok | this is a pass example
case2 | fail | this is a fail example
```

## how to browse the web

All generated static web pages will be stored in the **out_pages** directory, the generated web pages can be opened through a browser. **homepage.html** is the unified entrance of all web pages.

```shell
firefox out_pages/homepage.html
```
