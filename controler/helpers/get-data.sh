#!/bin/bash

# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/ /home/serchio/Documents/COAT/master-election-data/rpi3b+_idle_wifi_off_bt_on/

# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/ina219-ou_con_4-2019-05-14-* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_wifi_bt_off/
# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/info-ina219-ou_con_4-2019-05-14 /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_wifi_bt_off/

# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/ina219-ou_con_1-2019-05-14-* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_wifi_bt_off/
# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/info-ina219-ou_con_1-2019-05-14 /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_wifi_bt_off/

# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/ina219-ou_con_2-2019-05-16-* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_4g_rest_off/
# rsync -av lmi034@lmi034-1.cpsl.lan:/home/lmi034/master-election-data/info-ina219-ou_con_2-2019-05-16 /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_4g_rest_off/

rsync -av pi@192.168.100.1:/home/pi/data/power/wifi_range/* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_30/
rsync -av pi@192.168.100.210:/home/pi/web/* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_30/

rsync -av pi@192.168.100.4:/home/pi/data/power/wifi_range/* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_30/
rsync -av pi@192.168.100.214:/home/pi/web/* /home/serchio/Documents/COAT/master-election-experiments/data/energy/rpi3b_30/