import csv
import os

import cloudpassage


class Utility(object):
    def __init__(self):
        self.key = os.getenv("HALO_API_KEY")
        self.secret = os.getenv("HALO_API_SECRET_KEY")
        self.session = cloudpassage.HaloSession(self.key, self.secret)
        # We go ahead and grab an auth token for all abstractions to use.
        self.session.authenticate_client()
        self.servers = cloudpassage.Server(self.session)
        self.scans = cloudpassage.Scan(self.session)
        return

    def get_all_servers(self):
        """Return a list of all active servers from Halo."""
        return self.servers.list_all()

    @classmethod
    def write_csv_file(cls, csv_data, csv_file):
        """Write ``csv_data`` to ``csv_file``."""
        with open(csv_file, 'w') as c_file:
            fieldnames = sorted(csv_data[0].keys())
            writer = csv.DictWriter(c_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)

    @classmethod
    def results_to_tabular(cls, results):
        """Return dict results in tabular form (flat list of dict) for CSV."""
        finals = {}
        for r in results:
            s_crit = r["svm_critical"]
            s_ncrit = r["svm_non_critical"]
            c_crit = r["csm_critical"]
            c_ncrit = r["csm_non_critical"]
            if r["primary_column"] not in finals:
                finals[r["primary_column"]] = {"svm_critical": s_crit,
                                               "svm_non_critical": s_ncrit,
                                               "csm_critical": c_crit,
                                               "csm_non_critical": c_ncrit}
            else:
                finals[r["primary_column"]]["svm_critical"] += s_crit
                finals[r["primary_column"]]["svm_non_critical"] += s_ncrit
                finals[r["primary_column"]]["csm_critical"] += c_crit
                finals[r["primary_column"]]["csm_non_critical"] += c_ncrit

        tabular = [{"group_image": x,
                    "svm_critical": y["svm_critical"],
                    "svm_non_critical": y["svm_non_critical"],
                    "csm_critical": y["csm_critical"],
                    "csm_non_critical": y["csm_non_critical"]}
                   for x, y in finals.items()]
        return tabular

    def get_scan_results(self, server_object):
        """Return a dictionary describing CSM and SVM vulns per group-AMI."""
        s_id = server_object["id"]
        csm_scan = self.scans.last_scan_results(s_id, "csm")
        svm_scan = self.scans.last_scan_results(s_id, "svm")
        group_path = server_object["group_path"]
        ami_id = (server_object["csp_image_id"]
                  if "csp_image_id" in server_object
                  else "NO_IMAGE_ID")
        results = {"primary_column": "{} --- {}".format(group_path, ami_id),
                   "svm_critical": 0,
                   "csm_critical": 0,
                   "svm_non_critical": 0,
                   "csm_non_critical": 0}
        for scan in [("csm", csm_scan), ("svm", svm_scan)]:
            scan_type = scan[0]
            if "scan" not in scan[1]:
                continue
            crit = (scan[1]["scan"]["critical_findings_count"]
                    if "critical_findings_count" in scan[1]["scan"]
                    else 0)
            results["{}_critical".format(scan_type)] = crit
            non_crit = (scan[1]["scan"]["non_critical_findings_count"]
                        if "non_critical_findings_count" in scan[1]["scan"]
                        else 0)
            results["{}_non_critical".format(scan_type)] = non_crit
        return results
