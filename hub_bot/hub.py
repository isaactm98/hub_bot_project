import os
import subprocess
from datetime import datetime

JOB_FILE_NAME_PREFIX = 'job_to_process'


def work_order_separator(file_name):
    work_order = open(file_name, 'r')
    work_order_contents = work_order.readlines()

    num_of_jobs = 0

    # user and date will be first two lines of work order seperated by a space
    # a la User: sample
    user = work_order_contents[0].split()[1]
    date = work_order_contents[1].split()[1:]


    file_to_write_contents = []

    # skip the user, date, and separating line.. start on line 4
    for line in work_order_contents[3:]:
        # * indicates end of job
        if '*END~*' in line:
            num_of_jobs += 1
            file_to_write = JOB_FILE_NAME_PREFIX + '_' + str(num_of_jobs) + '.txt'
            write_file = open(file_to_write, 'w')
            write_file.write('User: {}\nDate: {}\n'.format(user, date))
            for line_to_write in file_to_write_contents:
                write_file.write(line_to_write)
            write_file.close()
            file_to_write_contents = []
        else:
            file_to_write_contents.append(line)

def job_file_processor(dir = os.getcwd()):#if dir is passed, it must contain full path to directory
    files_to_process = []
    for x in os.listdir(dir):#acquire the .txt individual job files in directory specified or current dir default
        if JOB_FILE_NAME_PREFIX in x:
            files_to_process.append(x)

    print(files_to_process)
    #open and read in files
    for read_file in files_to_process:
        job_file = open(read_file, 'r')
        job_file_contents = job_file.readlines()#open first job file and read all lines

        curr_time_and_date = datetime.now()#log info to user and console
        submitting_user = str.strip(job_file_contents[0][6:], '\n')
        date_submitted = str.strip(job_file_contents[1][6:], '\n')
        log_file = open(str.strip(read_file, '.txt') + '_log.txt', 'w')
        log_file.write("{} submitted job at {} for processing.\nExecution began at {}.\n\n".format(submitting_user,
                                                                                           date_submitted,
                                                                                           curr_time_and_date))
        print("{} submitted job at {} for processing.\nExecution began at {}.\n\n".format(submitting_user,
                                                                                           date_submitted,
                                                                                    curr_time_and_date))

        try:
            job_file_contents = job_file_contents[2:]# skip first 2 lines
            for index, line in enumerate(job_file_contents):
                user_script_contents = []
                if line[0] == '$':
                    process = subprocess.Popen(str.strip(line[1:], '\n'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    output, error = process.communicate()
                    log_file.write(str(output))
                    log_file.write(str(error))
                elif line[0] == '@':
                    user_script_name = line[1:]
                    while job_file_contents[index + 1][0] == '~':
                        user_script_contents.append(job_file_contents[index + 1][1:])
                        index += 1
                    write_file = open(str.strip(user_script_name, '\n'), 'w')
                    write_file.writelines(user_script_contents)
                    write_file.close()

        except Exception as e:
            print(e)
            log_file.write(str(e))
            pass




def main():
    #get work order file here

    work_order_separator('test.txt')
    job_file_processor()


if __name__ == '__main__':
    main()