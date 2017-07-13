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
        if '*' in line:
            print('test')
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


def main():
    #get work order file here

    work_order_separator('test.txt')


if __name__ == '__main__':
    main()