import re
import csv


if __name__ == '__main__':

    contacts_dict_result = {}
    contacts_list_result = []

    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

        # lastname, firstname, surname, organization, position, phone, email
        #    0           1          2       3           4         5      6
        for contact in contacts_list:
            # номер телефона +
            tel_new = re.sub(
                r'(\+7|8)[\s ]?[\s(]?(\d{3})[\s)]?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\ )?[\s(]?(доб)?(\ )?(\.)?[\s ]?(\d{1,4})?[\s)]?',
                r'+7(\2)\3-\4-\5\6\7\8\9\10',
                contact[5])

            #ФИО
            str_fio = contact[0] + contact[1] + contact[2]
            pattern = re.compile(r'([А-ЯЁ][а-яё]+)[\ |\,]?([А-ЯЁ][а-яё]+)[\ |\,]?([А-ЯЁ][а-яё]+)?')
            str_fio_splitted = re.split(pattern, str_fio)

            if len(str_fio_splitted) > 1:
                str_fio = ' '.join(str(x) for x in str_fio_splitted)
                if str_fio in contacts_dict_result:
                    # если по фио совпадет уже человек, то обновим данные
                    info_old = contacts_dict_result[str_fio]
                    info_old[0] = str_fio_splitted[1]
                    info_old[1] = str_fio_splitted[2]
                    info_old[2] = str_fio_splitted[3]
                    if contact[3] != "":
                        info_old[3] = contact[3]
                    if contact[4] != "":
                        info_old[4] = contact[4]
                    if tel_new != "":
                        info_old[5] = tel_new
                    if tel_new != "":
                        info_old[6] = contact[6]
                else:
                    # добавить уникального человека
                    contacts_dict_result[str_fio] = [str_fio_splitted[1], str_fio_splitted[2], str_fio_splitted[3],
                                                     contact[3], contact[4], tel_new, contact[6]]

    for key in contacts_dict_result:
        contacts_list_result.append(contacts_dict_result[key])

    with open("phonebook.csv", "w", newline='') as f:
        dwr = csv.writer(f, delimiter=',')
        dwr.writerows(contacts_list_result)
