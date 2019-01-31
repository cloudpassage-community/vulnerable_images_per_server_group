import os
import sys
from multiprocessing.dummy import Pool

import locallib


FILE_PATH = "./csv.out"
# Number of servers to concurrenty retrieve scans for.
THREAD_POOL_SIZE = 20


def main():
    csv_file_abspath = os.path.abspath(FILE_PATH)
    print("Will write CSV data to {}".format(csv_file_abspath))

    # If these are unset, script will bail before pushing to gsheets.
    workbook_id = os.getenv("WORKBOOK_ID")
    g_svc_acct_json = os.getenv("G_SVC_ACCT_JSON")

    utility = locallib.Utility()
    all_servers = utility.get_all_servers()
    print("Total servers: {}".format(len(all_servers)))

    # Threaded collection of server scan information
    pool = Pool(THREAD_POOL_SIZE)
    results = pool.map(utility.get_scan_results, all_servers)
    pool.close()

    final = utility.results_to_tabular(results)
    utility.write_csv_file(final, FILE_PATH)

    # Make sure that Gsheets info is good before uploading
    g_req = {"WORKBOOK_ID": workbook_id,
             "G_SVC_ACCT_JSON": g_svc_acct_json}
    if None in g_req.values():
        miss = ", ".join([x for x in g_req.keys() if g_req[x] is None])
        print("Missing some gdoc config info ({}), try again...".format(miss))
        sys.exit(1)
    print("Uploading to Google sheets...")
    with open(csv_file_abspath) as c_file:
        csv_lines = c_file.readlines()
    locallib.CsvToPage.update_cells(workbook_id, "".join(csv_lines))


if __name__ == "__main__":
    main()
