import argparse
import csv
import os
from pep_repo import PepRepo


def get_pep_records(pep_file):
    pep_100_recs = []
    pep_200_recs = []
    for row in pep_file:
        rec_type = row[3:6]
        if rec_type == '100': pep_100_recs.append(row)
        if rec_type == '200': pep_200_recs.append(row)
    return (pep_100_recs, pep_200_recs)


def get_schedule_2_recs(repo):
    output = []
    keys = repo.get_all_keys()
    for key in keys:
        # Any invalid salaries may indicate a damaged file, error out
        repo.validate_salary(key)
        rec = {}
        rec['name'] = repo.get_name(key)
        rec['ssn'] = key
        rec['years_experience'] = repo.get_years_xp(key)
        rec['obj_code'] = repo.get_obj_code(key)
        rec['func_code'] = repo.get_func_code(key)
        rec['cert_number'] = repo.get_cert_num(key)
        rec['cert_type'] = repo.get_cert_type(key)
        rec['education_level'] = repo.get_ed_level(key)
        output.append(rec)
    return output


def get_schedule_5_recs(repo):
    output = []
    keys = repo.get_all_keys()
    for key in keys:
        rec = {}
        rec['name'] = repo.get_name(key)
        rec['ssn'] = key
        rec['days_employed'] = repo.get_days_employed(key)
        rec['employment_type'] = repo.get_emp_type(key)
        rec['base_salary'] = repo.get_base_salary(key)
        rec['pip_salary'] = repo.get_pip_salary(key)
        rec['extra_compensation'] = repo.get_extra_compensation(key)
        rec['retiree_code'] = repo.get_retiree_code(key)
        rec['cert_exception_code'] = repo.get_cert_exc_code(key)
        output.append(rec)
    return output


def write_output_files(schedule_2, schedule_5, output_dir):
    s2_headers = ['name',
                  'ssn',
                  'years_experience',
                  'obj_code',
                  'func_code',
                  'cert_number',
                  'cert_type',
                  'education_level']
    s5_headers = ['name',
                  'ssn',
                  'days_employed',
                  'employment_type',
                  'base_salary',
                  'pip_salary',
                  'extra_compensation',
                  'retiree_code',
                  'cert_exception_code']
    write_output_file(schedule_2, s2_headers, 'schedule_2.csv', output_dir)
    write_output_file(schedule_5, s5_headers, 'schedule_5.csv', output_dir)


def write_output_file(records, headers, filename, output_dir):
    with open(os.path.join(output_dir, filename), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for i in records:
            writer.writerow(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("pep_file", type=argparse.FileType('r'), help="Path to a file containing PEP 100 and 200 records.  Other types of PEP records may be included, but will be ignored")
    parser.add_argument("output_dir", help="Output directory for the generated schedule files")
    args = parser.parse_args()

    pep_100_recs, pep_200_recs = get_pep_records(args.pep_file)
    args.pep_file.close()
    print(f'pep_100 records found: {len(pep_100_recs)}')
    print(f'pep_200 records found: {len(pep_200_recs)}')

    repo = PepRepo()
    for i in pep_100_recs:
        repo.add_100(i)
    for i in pep_200_recs:
        repo.add_200(i)
    print(f'Repo state: {repo.to_str()}')

    schedule_2 = get_schedule_2_recs(repo)
    schedule_5 = get_schedule_5_recs(repo)
    print(f'schedule_2 records created: {len(schedule_2)}')
    print(f'schedule_5 records created: {len(schedule_2)}')
    # No need to generate schedule 6, just give your auditors the SISR21 report
    write_output_files(schedule_2, schedule_5, args.output_dir)
    print('\nOutput files created')
