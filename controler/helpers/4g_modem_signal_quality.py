RSSI_START = 0
RSSI_DBM_START = -120
RSSI_DBM_END = -25
RSSI_END = 96
RSSI_INTERVAL = 1

RSRP_START = 0
RSRP_DBM_START = -140
RSRP_DBM_END = -44
RSRP_END = 97
RSRP_INTERVAL = 1

SINR_START = 0
SINR_END = 251
SINR_DBM_START = -20.0
SINR_DBM_END = 30.0
SINR_INTERVAL = 0.2

RSRQ_START = 0
RSRQ_END = 34
RSRQ_DBM_START = -19.5
RSRQ_DBM_END = -3.0
RSRQ_INTERVAL = 0.5

def _create_matrix(start, end, dbm_start, dbm_end, dbm_interval):
    matrix = {}

    for x in range(start, end + 1):
        if x == start:
            matrix[x] = dbm_start
            continue

        if x == end:
            matrix[x] = dbm_end
            continue

        dbm_l = dbm_start + (x * dbm_interval) - dbm_interval
        dbm_r = dbm_l + dbm_interval

        matrix[x] = (dbm_l, dbm_r)

    return matrix


rssi_matrix = _create_matrix(RSSI_START, RSSI_END, RSSI_DBM_START, RSSI_DBM_END, RSSI_INTERVAL)
rsrp_matrix = _create_matrix(RSRP_START, RSRP_END, RSRP_DBM_START, RSRP_DBM_END, RSRP_INTERVAL)
sinr_matrix = _create_matrix(SINR_START, SINR_END, SINR_DBM_START, SINR_DBM_END, SINR_INTERVAL)
rsrq_matrix = _create_matrix(RSRQ_START, RSRQ_END, RSRQ_DBM_START, RSRQ_DBM_END, RSRQ_INTERVAL)


print(rssi_matrix[87])
print(rsrp_matrix[59])
print(sinr_matrix[176])
print(rsrq_matrix[32])