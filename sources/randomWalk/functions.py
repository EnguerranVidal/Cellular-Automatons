import time


def gif_name():
    t0 = time.time()
    struct = time.localtime(t0)
    string = str(struct.tm_year) + '-'
    n_months = str(struct.tm_mon)  # MONTHS
    if len(n_months) == 1:
        n_months = '0' + n_months
    string = string + n_months + '-'
    n_days = str(struct.tm_mday)  # DAYS
    if len(n_months) == 1:
        n_days = '0' + n_days
    string = string + n_days + '-'
    n_hours = str(struct.tm_hour)  # HOURS
    if len(n_hours) == 1:
        n_hours = '0' + n_hours
    string = string + n_hours + '-'
    n_mins = str(struct.tm_min)  # MINUTES
    if len(n_mins) == 1:
        n_mins = '0' + n_mins
    string = string + n_mins + '-'
    n_secs = str(struct.tm_sec)  # SECONDS
    if len(n_secs) == 1:
        n_secs = '0' + n_secs
    string = string + n_secs + '.gif'
    return string


def select_list(l, n):
    m = len(l)
    skip = int(m / n)
    new_l = []
    for i in range(m):
        if i % skip == 0:
            new_l.append(l[i])
    return new_l
