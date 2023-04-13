#! /usr/bin/env python

import sys
import os
import pandas as pd
import math

def setup_homepage_items(lines:list, args):
    item = args[0]
    item_string = r'''<div class="icons" onclick="window.open('./{}.html', target='_self')">'''.format(item)
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
        lines.append(r'''<div class="image">''' + '\n')
        img = '{}'.format(args[0])
        img_string = r'''<img src="{}" alt="">'''.format(img)
        lines.append(img_string + '\n')
        lines.append(r'''</div>''' + '\n')
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

    lines.append(r'''<h1 class="heading"> {} </h1>'''.format(sheet_file))
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

def setup_detailpage_csv(lines:list, args):
    sheet_file = args[0]
    sheet_lines = []
    with open(sheet_file, 'r') as filp:
        sheet_lines = filp.readlines()

    header = sheet_lines[0].split(',')[0]
    lines.append(r'''<h1 class="heading"> {} </h1>'''.format(header))
    lines.append(r'''<table class="table">''' + '\n')
    titles = sheet_lines[1].strip('\n').split(',')
    title_sting = r'<tr>  '
    for t in titles:
        if t == '':
            t = '---'
        title_sting += r'<th>{}</th> '.format(t)
    title_sting += r'</tr>'

    lines.append(title_sting + '\n')

    for data_line in sheet_lines[2:]:
        data_string = r'<tr> '
        data = data_line.strip('\n').split(',')
        for d in data:
            if d == '':
                d = '---'
            data_string += r'<td>{}</td> '.format(d)
        data_string += r'</tr>'
        lines.append(data_string + '\n')
    lines.append(r'''</table>''' + '\n')

def setup_detailpage_excel(lines:list, args):
    excel_path = args[0]

    df = pd.read_excel(excel_path, sheet_name=0)
    title = list(df.columns)
    lines.append(r'''<h1 class="heading"> {} </h1>'''.format(title[0]) + '\n')
    lines.append(r'''<table class="table">''' + '\n')

    excel_values = list(df.values)
    fields = excel_values[0]
    fields_sting = r'<tr>  '
    for field in fields:
        fields_sting += r'<th>{}</th> '.format(field)
    fields_sting += r'</tr>'
    lines.append(fields_sting + '\n')

    data_lines = excel_values[1:]
    for data in data_lines:
        data_string = r'<tr> '
        for ceil in data:
            if type(ceil) is float and math.isnan(ceil):
                ceil = '---'
            data_string += r'<td align="left">{}</td> '.format(ceil)
        data_string += r'</tr>'
        lines.append(data_string + '\n')
    lines.append(r'''</table>''' + '\n')

def setup_detailpage_cases(lines:list, args):
    child_name = args[0]
    child_path = args[1]
    case_string = r'''<input type="submit0" value="{}" class="btn" onclick="window.open('{}.html', target='_self')">'''.format(child_name, child_path)
    lines.append(case_string + '\n')

def setup_casepage_name(lines:list, args):
    child_name = args[0]
    case_string = r'''<a href="#" class="logo"> {} </a>'''.format(child_name)
    lines.append(case_string + '\n')

def setup_casepage_img(lines:list, args):
    img_path = args[0]
    img_name = args[1]
    img_string = r'''<div class="content"> <h2>{}</h2> </div>'''.format(img_name)
    lines.append(img_string + '\n')
    img_string = r'''<div class="case"> <img src="{}" alt="" /> </div>'''.format(img_path)
    lines.append(img_string + '\n')

def setup_css(lines:list, args):
    css_string = r'''<link rel="stylesheet" href="{}">'''.format(args[0])
    lines.append(css_string + '\n')

setup_list = []
setup_dict = {}

def init_setup_table(templete_name, page_name, position, setup_function, *args):
    if templete_name not in setup_list:
        setup_dict[templete_name] = {}
        setup_list.append(templete_name)
    if page_name not in setup_dict[templete_name]:
        setup_dict[templete_name][page_name] = []

    desc = (page_name, position, setup_function, args)
    setup_dict[templete_name][page_name].append(desc)

def setup_page(type_name:str, page_name:str, descs:list):
    templete = os.path.join(script_dir, type_name + '.templete')
    with open(templete, 'r') as filp:
        read_lines = filp.readlines()

    new_lines = []

    for line in read_lines:
        new_lines.append(line)
        for desc in descs:   
            path, pos, func, args = desc
            if pos in line:
                func(new_lines, args)

    fpath = '{}.html'.format(page_name)
    with open(fpath, 'w') as filp:
        filp.writelines(new_lines)
    os.system('chmod 777 ' + fpath)

# run from here
# get detail page name
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath(os.path.join(script_dir, 'out_pages'))
dir_filter = ('out_pages', '.git')
flush_filter = ('style.css', 'images')
css_path = os.path.join(output_dir, 'style.css')
img_types = ('PNG', 'SVG', 'JPG', 'JPEG')
excel_types = ('xlsx', 'xls')

# flush the output dir
for f in os.listdir(output_dir):
    if f not in flush_filter:
        flush_cmd = 'rm -rf {}'.format(os.path.join(output_dir, f))
        os.system(flush_cmd)

# register other pages
for root, subdirs, casefiles in os.walk(script_dir):
    relpath = os.path.relpath(root, script_dir)
    relpath_header = relpath.split('/')[0]
    if relpath_header in dir_filter:
        continue

    # added as dir
    # print('deal with root:', root)
    if len(subdirs) > 0:
        for subdir in sorted(subdirs):
            if relpath_header == '.' and subdir in dir_filter:
                continue
            dir_name = os.path.relpath(os.path.join(root, subdir), script_dir)
            dir_path = os.path.join(output_dir, dir_name)
            os.system('mkdir -p ' + dir_path)
            os.system('chmod 777 ' + dir_path)
            # print('creat output dir:', dir_path)

            is_leaf = True
            for p in os.listdir(os.path.join(script_dir, dir_name)):
                if os.path.isdir(os.path.join(script_dir, dir_name, p)):
                    is_leaf = False
                    break

            if is_leaf:
                # print('is leaf, continue')
                continue

            # print('creat detail page:', dir_path)
            init_setup_table('detailpage', dir_path, '<!-- detail name -->', setup_detailpage_name, dir_name)
            init_setup_table('detailpage', dir_path, '<!-- detail notes -->', setup_detailpage_notes, dir_name)
            init_setup_table('detailpage', dir_path, '<!-- add css -->', setup_css, css_path)

            # has detailpage father
            if relpath_header != '.':
                father_path = os.path.join(output_dir, relpath)
                dir_base, dir_relname = os.path.split(dir_name)
                init_setup_table('detailpage', father_path, '<!-- detail cases -->', setup_detailpage_cases, dir_relname, dir_path)
                # print('add a dir to father, dir name:', dir_path)
            # has homepage father
            else:
                init_setup_table('homepage', os.path.join(output_dir, 'homepage'), '<!-- add here -->', setup_homepage_items, dir_name)

        # support sheet file
        for cf in casefiles:
            suffix = cf.split('.')[-1]
            father_name = os.path.relpath(root, script_dir)
            father_path = os.path.join(output_dir, father_name)
            cf_path = os.path.abspath(os.path.join(root, cf))
            if suffix == 'sheet':
                init_setup_table('detailpage', father_path, '<!-- detail sheet -->', setup_detailpage_sheet, cf_path)
            if suffix.upper() == 'CSV':
                init_setup_table('detailpage', father_path, '<!-- detail sheet -->', setup_detailpage_csv, cf_path)
            if suffix.upper() in img_types:
                init_setup_table('detailpage', father_path, '<!-- detail image -->', setup_detailpage_image, cf_path)
                # print('add title img to:', father_path)
            if suffix in excel_types:
                init_setup_table('detailpage', father_path, '<!-- detail sheet -->', setup_detailpage_excel, cf_path)

    # added as case
    if len(subdirs) == 0 and len(casefiles) > 0:
        child_name = os.path.relpath(root, script_dir)
        child_base, child_relname = os.path.split(child_name)
        child_path = os.path.join(output_dir, child_name)
        father_name = os.path.dirname(child_name)
        father_path = os.path.join(output_dir, father_name)

        # print('add a case to father, case name:', child_path)
        init_setup_table('detailpage', father_path, '<!-- detail cases -->', setup_detailpage_cases, child_relname, child_path)
        init_setup_table('casepage', child_path, '<!-- case name -->', setup_casepage_name, child_name)
        init_setup_table('casepage', child_path, '<!-- add css -->', setup_css, css_path)

        setup_case_sheet = True
        for cf in casefiles:
            suffix = cf.split('.')[-1]
            f_path = os.path.abspath(os.path.join(root, cf))
            if suffix in excel_types:
                init_setup_table('casepage', child_path, '<!-- case sheet -->', setup_detailpage_excel, f_path)
            if suffix == 'sheet':
                init_setup_table('casepage', child_path, '<!-- case sheet -->', setup_detailpage_sheet, f_path)
            if suffix.upper() == 'CSV':
                init_setup_table('casepage', child_path, '<!-- case sheet -->', setup_detailpage_csv, f_path)
            # add image to one case page
            if suffix.upper() in img_types:
                init_setup_table('casepage', child_path, '<!-- case img -->', setup_casepage_img, f_path, cf)

# setup page
for templete in setup_list:
    for page in setup_dict[templete]:
        setup_page(templete, page, setup_dict[templete][page])
