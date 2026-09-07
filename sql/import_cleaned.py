"""Import the cleaned CSV to a verified staging table; preserve the old apps table."""
import csv
import pathlib
import subprocess
from datetime import datetime
from decimal import Decimal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mysql", default=r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe")
parser.add_argument("--login-path", default="app_marketplace")
args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((root / "data/googleplaystore_cleaned.csv").open(encoding="utf-8-sig", newline="")))
source = "app category rating reviews size installs type price content_rating genres last_updated current_ver android_ver".split()
target = "app_name category rating reviews size installs app_type price content_rating genres last_updated current_version android_version".split()
numeric = {"rating", "reviews", "installs", "price"}
assert rows and set(rows[0]) == set(source), "Unexpected CSV columns"
def run(sql):
    p = subprocess.run([args.mysql, "--login-path="+args.login_path, "--default-character-set=utf8mb4",
                        "--batch", "--raw", "app_marketplace"], input=sql,
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout
def literal(k, value):
    if value == "":
        return "NULL"
    if k in numeric:
        number = Decimal(value)
        assert number.is_finite(), (k, value)
        return str(number)
    return "CONVERT(X'" + value.encode("utf-8").hex() + "' USING utf8mb4)"
stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
stage, backup = "apps_verified_"+stamp, "apps_backup_"+stamp
run("CREATE TABLE "+stage+" LIKE apps;")
# A failure leaves apps untouched and the stage available for diagnosis.
for offset in range(0, len(rows), 250):
    values = ["("+",".join(literal(k, row[k]) for k in source)+")" for row in rows[offset:offset+250]]
    run("INSERT INTO "+stage+" ("+",".join(target)+") VALUES "+",".join(values)+";")
select = [column if key in numeric else "HEX("+column+")" for key, column in zip(source, target)]
actual = run("SELECT "+",".join(select)+" FROM "+stage+" ORDER BY app_id;").splitlines()[1:]
assert len(actual) == len(rows), "Row count mismatch"
for line, row in zip(actual, rows):
    fields = line.split("\t")
    assert len(fields) == len(source)
    for key, value in zip(source, fields):
        expected = row[key]
        if expected == "":
            assert value == "NULL", key
        elif key in numeric:
            assert Decimal(value) == Decimal(expected), key
        else:
            assert bytes.fromhex(value).decode("utf-8") == expected, key
run("RENAME TABLE apps TO "+backup+", "+stage+" TO apps;")
print("Verified", len(rows), "rows across all 13 fields. Previous table:", backup)
