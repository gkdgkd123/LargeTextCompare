import argparse
import sys
import time
import datetime
import difflib
import os

def readfile(filename):
    try:
        with open(filename, 'r', encoding='UTF-8') as fileHandle:
            text = fileHandle.read().splitlines()
        return text
    except IOError as e:
        print("Read file Error:", e)
        sys.exit()

def diff_file(filename1, filename2):
    text1_lines = readfile(filename1)
    text2_lines = readfile(filename2)

    differ = difflib.HtmlDiff()
    html_content = differ.make_file(text1_lines, text2_lines)

    with open('diff.html', 'w', encoding='UTF-8') as result_file:
        result_file.write(html_content)

def split_large_file(filename, chunk_size):
    with open(filename, 'r', encoding='UTF-8') as file:
        base_name = os.path.basename(filename)
        file_index = 1
        line_counter = 0
        chunk_lines = []
        
        for line in file:
            chunk_lines.append(line)
            line_counter += 1
            
            if line_counter >= chunk_size:
                chunk_filename = f'{base_name}_{file_index}.txt'
                with open(chunk_filename, 'w', encoding='UTF-8') as chunk_file:
                    chunk_file.write(''.join(chunk_lines))
                
                chunk_lines = []
                line_counter = 0
                file_index += 1
        
        if chunk_lines:
            chunk_filename = f'{base_name}_{file_index}.txt'
            with open(chunk_filename, 'w', encoding='UTF-8') as chunk_file:
                chunk_file.write(''.join(chunk_lines))

def perform_diff_on_large_file(filename1, filename2):
    split_large_file(filename1, 100000)
    split_large_file(filename2, 100000)
    
    for file_index in range(1, sys.maxsize):
        chunk_filename1 = f'{filename1}_{file_index}.txt'
        chunk_filename2 = f'{filename2}_{file_index}.txt'
        
        if not (os.path.isfile(chunk_filename1) and os.path.isfile(chunk_filename2)):
            break
        
        diff_file(chunk_filename1, chunk_filename2)
        
        os.remove(chunk_filename1)
        os.remove(chunk_filename2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="传入两个文件参数")
    parser.add_argument('-f1', action='store', dest='filename1', required=True)
    parser.add_argument('-f2', action='store', dest='filename2', required=True)
    given_args = parser.parse_args()
    filename1 = given_args.filename1
    filename2 = given_args.filename2
    begin = datetime.datetime.now()
    print('任务开始：'+ str(begin))

    perform_diff_on_large_file(filename1, filename2)

    end = datetime.datetime.now()
    print('任务结束，耗时：'+ str((end-begin)))
