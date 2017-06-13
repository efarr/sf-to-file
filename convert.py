import argparse
import os
import csv
import json
from shutil import copy2
from dateutil import parser as dparse


parser = argparse.ArgumentParser(description='Turn SFDC CSV backup into file objects')
parser.add_argument('--source', help='directory where backup files are')
parser.add_argument('--dest', help='directory where file objects will go')

args = parser.parse_args()

print('Going to dump from %s to %s' % (args.source, args.dest))

accounts = {}
contacts = []
notes = []
attachments = []


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def dict_to_json_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)


def name_to_dir(name):
    return ''.join(e for e in name.replace(" ", "_") if e.isalnum() or e in "-_")


def account_name_to_path(account_name):
    return os.path.join(args.dest, name_to_dir(account_name))


def make_dirs():
    for _id, name in accounts.items():
        make_dir(account_name_to_path(name))
    make_dir(account_name_to_path('_NoAccount_'))


def get_account_name(id):
    if id in accounts.keys():
        return accounts[id]
    return '_NoAccount_'


def get_account_directory(account_id, entity_type):
    account_path = os.path.join(args.dest, account_name_to_path(get_account_name(account_id)))
    if entity_type:
        full_path = os.path.join(account_path, entity_type)
        make_dir(full_path)
        return full_path
    else:
        return account_path


def dump_contacts():
    for contact in contacts:
        filename = name_to_dir(contact['FirstName'] + contact['LastName']) + '.json'
        full_path = os.path.join(get_account_directory(contact['AccountId'], 'contacts'), filename)
        dict_to_json_file(contact, full_path)


def dump_notes():
    for note in notes:
        created = dparse.parse(note['CreatedDate'])
        filename = name_to_dir( '%s-%s-%s-%s' % (created.year, created.month, created.day, note['Title'])) + '.json'
        full_path = os.path.join(get_account_directory(note['AccountId'], 'notes'), filename)
        dict_to_json_file(note, full_path)


def dump_attachments():
    for attachment in attachments:
        filename = attachment['Name'].replace("?", "_")
        dst_path = os.path.join(get_account_directory(attachment['AccountId'], 'attachments'), filename)
        src_path = os.path.join(args.source, 'Attachments')
        src_path = os.path.join(src_path, attachment['Id'])
        copy2(src_path, dst_path)


def read_accounts():
    with open(os.path.join(args.source, 'account.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            accounts[row['Id']] = row['Name']
    print('Read %s accounts.' % len(accounts))


def read_entity(source, dest):
    with open(os.path.join(args.source, source)) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dest.append(row)
    print('Read %s from %s.' % (len(dest), source))


read_accounts()
read_entity('contact.csv', contacts)
read_entity('note.csv', notes)
read_entity('attachment.csv', attachments)

if args.dest:
    make_dir(args.dest)
    make_dirs()
    dump_contacts()
    dump_notes()
    dump_attachments()
