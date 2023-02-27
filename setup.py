#! /usr/bin/env python

import sys
import os

def setup_homepage_items(lines:list, args):
    for item in detail_page_names:
        item_string = r'''<div class="icons" onclick="window.open('./{}.html')">'''.format(item)
        lines.append(item_string + '\n')
        item_string = r'''<i class="fas fa-user-md"></i> <h3>{}</h3> <p>click for details</p>'''.format(item)
        lines.append(item_string + '\n')
        item_string = r'''</div>'''
        lines.append(item_string + '\n\n')

def setup_detailpage_name(lines:list, args):
    name_string = r'''<a href="#" class="logo"> {} </a>'''.format(args[0])
    lines.append(name_string + '\n')

def setup_detailpage_image(lines:list, args):
    if args:
        img = '{}'.format(args[0])
        img_string = r'''<img src="{}" alt="">'''.format(img)
        lines.append(img_string + '\n')
    # else:
    #     img = 'images/home-img.png'
    # img_string = r'''<img src="{}" alt="">'''.format(img)
    # lines.append(img_string + '\n')

def setup_detailpage_notes(lines:list, args):
    name = args[0]
    note_string = r'''<h3>{} Performance</h3>'''.format(name)
    lines.append(note_string + '\n')
    note_string = r'''<p>{} performance details </p>'''.format(name)
    lines.append(note_string + '\n')

def setup_detailpage_sheet(lines:list, args):
    sheet_file = args[0]
    sheet_lines = []
    with open(sheet_file, 'r') as filp:
        sheet_lines = filp.readlines()

    lines.append(r'''<table class="table">''' + '\n')
    titles = sheet_lines[0].strip('\n').split('|')
    title_sting = r'<tr>  '
    for t in titles:
        title_sting += r'<th>{}</th> '.format(t)
    title_sting += r'</tr>'

    lines.append(title_sting + '\n')

    for data_line in sheet_lines[1:]:
        data_string = r'<tr> '
        data = data_line.strip('\n').split('|')
        for d in data:
            data_string += r'<td>{}</td> '.format(d)
        data_string += r'</tr>'
        lines.append(data_string + '\n')
    lines.append(r'''</table>''' + '\n')

def setup_detailpage_cases(lines:list, args):
    case_dir = args[0]
    case_name = args[1]
    case_string = r'''<input type="submit0" value="{}" class="btn" onclick="window.open('./{}.html')">'''.format(case_dir, case_name)
    lines.append(case_string + '\n')

def setup_casepage_name(lines:list, args):
    case_name = args[0]
    case_string = r'''<a href="#" class="logo"> {} </a>'''.format(case_name)
    lines.append(case_string + '\n')

def setup_casepage_img(lines:list, args):
    img_name = args[0]
    img_string = r'''<div class="content"> <h2>{}</h2> </div>'''.format(img_name)
    lines.append(img_string + '\n')
    img_string = r'''<div class="case"> <img src="{}" alt="" /> </div>'''.format(img_name)
    lines.append(img_string + '\n')

def init_setup_table(templete_name, page_name, position, setup_function, *args):
    if templete_name not in setup_list:
        setup_dict[templete_name] = {}
        setup_list.append(templete_name)
    if page_name not in setup_dict[templete_name]:
        setup_dict[templete_name][page_name] = []

    desc = (position, setup_function, args)
    setup_dict[templete_name][page_name].append(desc)

def setup_page(type_name:str, page_name:str, descs:list):
    templete = os.path.join(script_dir, type_name + '.templete')
    with open(templete, 'r') as filp:
        read_lines = filp.readlines()

    new_lines = []

    for line in read_lines:
        new_lines.append(line)
        for desc in descs:   
            pos, func, args = desc
            if pos in line:
                func(new_lines, args)

    fpath = os.path.join(out_path, '{}.html'.format(page_name))
    with open(fpath, 'w') as filp:
        filp.writelines(new_lines)
    os.system('chmod 775 ' + fpath)

# run from here
# get detail page name
script_dir = os.path.dirname(__file__)
flist = os.listdir(script_dir)
dir_filter = ('out_pages', '.git')
detail_page_names = []
for f in flist:
    fpath = os.path.join(script_dir, f)
    if os.path.isdir(fpath) and f not in dir_filter:
        detail_page_names.append(f)

setup_list = []
setup_dict = {}

out_path = os.path.abspath(os.path.join(script_dir, 'out_pages'))
os.system('rm -f ' + out_path + '*.html')

# register setup pass
init_setup_table('homepage', 'homepage', '<!-- add here -->', setup_homepage_items)
for detail_page in detail_page_names:
    init_setup_table('detailpage', detail_page, '<!-- detail name -->', setup_detailpage_name, detail_page)
    init_setup_table('detailpage', detail_page, '<!-- detail notes -->', setup_detailpage_notes, detail_page)
    detail_dir = os.path.join(script_dir, detail_page)
    detail_files = os.listdir(detail_dir)

    default_img = True
    setup_sheet = True
    for df in detail_files:
        case_dir = os.path.join(detail_dir, df)
        # recusive foreach case dir
        if os.path.isdir(case_dir):
            case_added = []
            for root, subdir, casefiles in os.walk(case_dir):
                for cf in casefiles:
                    suffix = cf.split('.')[-1]
                    if suffix.upper() in ('PNG', 'SVG', 'JPG'):
                        # add one case page entry to detailpage
                        case_realpath = os.path.relpath(root, script_dir)
                        case_name = case_realpath.replace('/', '_')
                        if case_name not in case_added:
                            init_setup_table('detailpage', detail_page, '<!-- detail cases -->', setup_detailpage_cases, case_realpath, case_name)
                            init_setup_table('casepage', case_name, '<!-- case name -->', setup_casepage_name, case_realpath)
                            case_added.append(case_name)

                        # add one case page
                        img_path = os.path.abspath(os.path.join(root, cf))
                        init_setup_table('casepage', case_name, '<!-- case img -->', setup_casepage_img, img_path)

        # if has image or sheet, show in detail page
        if os.path.isfile(case_dir):
            suffix = df.split('.')[-1]
            if setup_sheet and suffix == 'sheet':
                setup_sheet = False
                init_setup_table('detailpage', detail_page, '<!-- detail sheet -->', setup_detailpage_sheet, case_dir)
            if default_img and suffix.upper() in ('PNG', 'SVG', 'JPG'):
                default_img = False
                init_setup_table('detailpage', detail_page, '<!-- detail image -->', setup_detailpage_image, os.path.abspath(case_dir))                

    # use default image for detail page
    if default_img:
        init_setup_table('detailpage', detail_page, '<!-- detail image -->', setup_detailpage_image)

# setup page
for templete in setup_list:
    for page in setup_dict[templete]:
        setup_page(templete, page, setup_dict[templete][page])
