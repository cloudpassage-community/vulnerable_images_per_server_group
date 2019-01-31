"""Set a CSV as the contents of a page."""
import base64
import csv
import os
import sys
import tempfile

import pygsheets


class CsvToPage(object):
    @classmethod
    def update_cells(cls, sheet_id, csv_string):
        """Batch update cells in ``sheet_id`` with ``csv_string``."""
        creds_json = base64.b64decode(os.getenv("G_SVC_ACCT_JSON"))
        reader = csv.reader(csv_string.splitlines())
        values = list(reader)
        (f_handle, temp_file) = tempfile.mkstemp()
        with open(temp_file, 'w') as t_f:
            t_f.write(creds_json)
        try:
            client = pygsheets.authorize(service_file=temp_file)
        except Exception as e:  # No matter what, we clean up the auth file.
            print("Exception caught while authenticating with Google API.")
            print("Details: {}".format(e))
            os.remove(temp_file)
            sys.exit(1)
        os.remove(temp_file)
        worksheet = client.open_by_key(sheet_id)
        page = worksheet.sheet1
        page.clear()
        page.update_values(crange="A1", values=values)
        print("Worksheet %s has been updated." % (sheet_id))
        return
