# performance case viewer

Performance case viewer is a tools that can creat html file according to file tree.
User can run setup.py to setup html files.

## core mechanism

The script setup.py can traverse the directories where it is located, use templete files to creat static html files corresponding to directories. This tools can support up to three-levels directories.

## how to add case

For example

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

in this example:

- An example is added, this will creat a detailpage, user can use mkdir to add a new page
- Tools support set a web image to a detailpage. under example dir, a image file example.png is added. png, jpg, svg are both supported
- Tools support add a sheet to a detailpage. under example dir, a example.sheet is added
- Tools support as many cases as possible under a detailpage. under each case dir, user can add as many image as possible.

when you update your case, you must run setup.py to update web pages.

## how to browse the web

you can open out_pages/homepage.html use your local browser.
