import argparse
import os
import csv
import json


parser = argparse.ArgumentParser(description='Turn SFDC CSV backup into file objects')
parser.add_argument('--source', help='directory where backup files are')
parser.add_argument('--dest', help='directory where file objects will go')

args = parser.parse_args()

print('Going to dump from %s to %s' % (args.source, args.dest))

accounts = {}
contacts = []


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def dict_to_json_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)


def name_to_dir(name):
    return ''.join(e for e in name if e.isalnum())


def account_name_to_path(account_name):
    return os.path.join(args.dest, name_to_dir(account_name))


def make_dirs():
    for _id, name in accounts.items():
        make_dir(account_name_to_path(name))


def get_account_directory(account_id):
    return os.path.join(args.dest, account_name_to_path(accounts[account_id]))


def dump_contacts():
    for contact in contacts:
        filename = name_to_dir(contact['FirstName'] + contact['LastName']) + '.json'
        full_path = os.path.join(get_account_directory(contact['AccountId']), filename)
        dict_to_json_file(contact, full_path)


with open(os.path.join(args.source, 'account.csv')) as f:
    reader = csv.DictReader(f)
    for row in reader:
        accounts[row['Id']] = row['Name']

with open(os.path.join(args.source, 'contact.csv')) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['AccountId'] in accounts.keys():
            print('%s: %s %s' % (accounts[row['AccountId']], row['FirstName'], row['LastName']))
            contacts.append(row)

if args.dest:
    make_dir(args.dest)
    make_dirs()
    dump_contacts()
