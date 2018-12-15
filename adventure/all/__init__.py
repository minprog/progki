import check50
import pkg_resources
if int(pkg_resources.get_distribution("check50").version[0]) < 3:
    raise ImportError("This check requires check50 version 3.0.0 or above.")

small = __import__("check50").import_checks("../small")

tiny = __import__("check50").import_checks("../tiny")

crowther = __import__("check50").import_checks("../crowther")
