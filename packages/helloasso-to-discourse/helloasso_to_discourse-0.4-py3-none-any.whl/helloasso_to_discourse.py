"""Sync script between HelloAsso payments and Discourse badges."""

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from itertools import count, groupby
from urllib.parse import urljoin

import requests
from helloasso_api import HaApiV5
from tabulate import tabulate


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Hello backup to Discourse badge")
    subparsers = parser.add_subparsers(help="Choose a command")

    sync_parser = subparsers.add_parser(
        "sync", help="Sync the backup file to a given Discourse instance"
    )
    sync_parser.add_argument("--ha-client-id", required=True)
    sync_parser.add_argument("--ha-client-secret", required=True)
    sync_parser.add_argument("--ha-org", required=True)
    sync_parser.add_argument(
        "--ha-form-slug",
        help="See the `list-forms` subcommand to learn which one you can use.",
        required=True,
    )
    sync_parser.add_argument("--discourse-url", required=True)
    sync_parser.add_argument("--discourse-api-key", required=True)
    sync_parser.add_argument(
        "--discourse-badge-slug",
        help="See the `list-badges` subcommand to learn which one you can use.",
        required=True,
    )
    sync_parser.set_defaults(func=main_sync)

    list_form_parser = subparsers.add_parser(
        "list-forms", help="List HelloAsso forms, to use with `sync`"
    )
    list_form_parser.add_argument("--ha-client-id", required=True)
    list_form_parser.add_argument("--ha-client-secret", required=True)
    list_form_parser.add_argument("--ha-org", required=True)
    list_form_parser.set_defaults(func=main_list_form)

    list_badges_parser = subparsers.add_parser(
        "list-badges", help="List Discourse badges, to use with `sync`"
    )
    list_badges_parser.set_defaults(func=main_list_badges)
    list_badges_parser.add_argument("--discourse-url", required=True)
    list_badges_parser.add_argument("--discourse-api-key", required=True)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    return args


class Discourse:
    """Discourse API client."""

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.session = None
        self._email_to_users_map = None

    def __enter__(self):
        self.session = requests.Session()
        self.session.headers.update({"Api-Key": self.api_key, "Api-Username": "system"})
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def post(self, url, data=None, json=None, **kwargs):
        """Send a POST request to the Discourse API."""
        response = self.session.post(urljoin(self.url, url), data, json, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, url, **kwargs):
        """Send a GET request to the Discourse API."""
        response = self.session.get(urljoin(self.url, url), **kwargs)
        response.raise_for_status()
        return response.json()

    def get_badge(self, badge_id):
        """List the user currently having badge (badge_id) assigned."""
        return self.get(f"/user_badges.json?badge_id={badge_id}")

    def get_badges(self):
        """List all badges."""
        badges_info = self.get("/badges.json")
        badge_types = {
            badge_type["id"]: badge_type for badge_type in badges_info["badge_types"]
        }
        badge_groups = {
            badge_group["id"]: badge_group
            for badge_group in badges_info["badge_groupings"]
        }
        badges = badges_info["badges"]
        for badge in badges:
            badge["type"] = badge_types[badge["badge_type_id"]]
            badge["group"] = badge_groups[badge["badge_grouping_id"]]
        return {badge["slug"]: badge for badge in badges}

    def users(self, flag="active"):
        """List all users."""
        all_users = []
        for page in count(1):
            users = self.get(
                f"/admin/users/list/{flag}.json",
                params={"page": page, "show_emails": "true"},
            )
            if not users:
                break
            all_users.extend(users)
        return all_users

    @property
    def email_to_users_map(self) -> dict[str, set[str]]:
        """Returns a dict of user emails to set of usernames.

        One email can give multiple username in case of users using
        `+` in their emails.
        """

        if self._email_to_users_map:
            return self._email_to_users_map
        email_to_users = defaultdict(set)
        for user in self.users():
            email_to_users[remove_email_tag(user["email"])].add(user["username"])
            for secondary_email in user["secondary_emails"]:
                email_to_users[remove_email_tag(secondary_email)].add(user["username"])
        self._email_to_users_map = dict(email_to_users)
        return self._email_to_users_map

    def assign_badge(self, badge_id, username):
        """Assign a badge to a user."""
        return self.post(
            "/user_badges", data={"badge_id": badge_id, "username": username}
        )


def remove_email_tag(email):
    """Many of our users are using tags in email, remove them for better matches.

    like john+helloasso@example.com should match john+discourse@example.com.
    """
    return re.sub(r"\+.*@", "@", email)


def main():
    """Module entry-point, dispatching to a subdommand."""
    args = parse_args()
    return args.func(args)


def main_list_form(args):
    """List all HelloAsso "forms" that can be used to sync.

    We sync one "form" to one "badge".
    """
    helloasso = HelloAsso(args.ha_client_id, args.ha_client_secret, args.ha_org)
    forms = [
        (item.order_formtype, item.order_formslug)
        for item in helloasso.items()
        if item.state == "Processed" and item.payer_email
    ]
    table = [key + (len(list(group)),) for key, group in groupby(sorted(forms))]
    print(
        "Here are the available HelloAsso forms you can you with the `sync` command ",
        "to link a form to a badge:\n",
        sep="\n",
    )
    print(tabulate(table, headers=("Type", "Name", "Members")))
    print()
    print("Use the `name` for the `sync` command, like:")
    print(
        "helloasso-to-discourse sync "
        '--ha-client-id="$(pass helloasso-clientid)" '
        '--ha-client-secret="$(pass helloasso-clientsecret)" '
        "--ha-org=afpy "
        "--discourse-url=https://discuss.afpy.org "
        '--discourse-api-key="$(pass afpy/discuss.afpy.org-api-key)" '
        "--ha-form-slug=REPLACE_ME "
        "--discourse-badge-slug=REPLACE_ME_TOO "
    )


def main_list_badges(args):
    """List discourse badges.

    We sync HelloAsso form slugs to Discourse badges.
    """
    discourse = Discourse(args.discourse_url, args.discourse_api_key)
    table = []
    with discourse:
        for slug, badge in discourse.get_badges().items():
            table.append(
                (
                    badge["group"]["name"],
                    badge["type"]["name"],
                    slug,
                    badge["grant_count"],
                )
            )
    table.sort()
    print(tabulate(table, headers=("Group", "Type", "Slug", "Grant count")))
    print()
    print("Use the tag `slug` for the `sync` command, like:")
    print(
        "helloasso-to-discourse sync "
        '--ha-client-id="$(pass helloasso-clientid)" '
        '--ha-client-secret="$(pass helloasso-clientsecret)" '
        "--ha-org=afpy "
        "--discourse-url=https://discuss.afpy.org "
        '--discourse-api-key="$(pass afpy/discuss.afpy.org-api-key)" '
        "--ha-form-slug=REPLACE_ME "
        "--discourse-badge-slug=REPLACE_ME_TOO "
    )


@dataclass
class HelloAssoRecord:
    """Represent one line as returned by /v5/organizations/{org}/items."""

    payer_email: str
    order_formtype: str
    order_formslug: str
    state: str

    @classmethod
    def from_api(cls, item):
        """Alternative ctor to create an HelloAssoRecord from an API answer."""
        return cls(
            payer_email=item.get("payer", {}).get("email"),
            order_formtype=item.get("order", {}).get("formType"),
            order_formslug=item.get("order", {}).get("formSlug"),
            state=item["state"],
        )


@dataclass
class HelloAsso:
    """HelloAsso API connection settings."""

    client_id: str
    client_secret: str
    org: str

    def items(self) -> list[HelloAssoRecord]:
        """Fetch /v5/organizations/{self.org}/items from the HelloAsso API."""
        api = HaApiV5(
            api_base="api.helloasso.com",
            client_id=self.client_id,
            client_secret=self.client_secret,
            timeout=60,
        )

        records = []
        endpoint = f"/v5/organizations/{self.org}/items"
        params = {"pageSize": 100}
        items = api.call(endpoint, params=params).json()
        while items["data"]:
            for item in items["data"]:
                records.append(HelloAssoRecord.from_api(item))
            params["continuationToken"] = items["pagination"]["continuationToken"]
            items = api.call(endpoint, params=params).json()
        return records


def sync(
    helloasso: HelloAsso,
    discourse: Discourse,
    ha_form_slug: str,
    badge_slug: str,
) -> None:
    """Main sync function that syncs an helloasso form slug to a discourse badge."""
    with discourse:
        from_helloasso = {
            remove_email_tag(record.payer_email)
            for record in helloasso.items()
            if record.order_formslug == ha_form_slug
            and record.state == "Processed"
            and record.payer_email
        }
        print(f"Found {len(from_helloasso)} emails in HelloAsso")
        badges = discourse.get_badges()
        badge = badges[badge_slug]
        badge_users = discourse.get_badge(badges[badge_slug]["id"]).get("users", ())
        already_assigned = {user["username"] for user in badge_users}
        print(f"Found {len(discourse.email_to_users_map)} emails in Discourse")
        common_emails = set(discourse.email_to_users_map) & from_helloasso
        print(f"Found {len(common_emails)} in common")
        already_assigned_count = 0
        for email in common_emails:
            for discourse_username in discourse.email_to_users_map[email]:
                if discourse_username in already_assigned:
                    already_assigned_count += 1
                    continue
                print(f"Assigning {badge['name']!r} to {discourse_username!r}")
                discourse.assign_badge(badge["id"], discourse_username)
        print(
            f"{already_assigned_count} Discourse users already have the badge {badge['name']!r}"
        )


def main_sync(args):
    """Setup needed HelloAsso and Discourse to start a sync."""
    hello_asso = HelloAsso(
        client_id=args.ha_client_id,
        client_secret=args.ha_client_secret,
        org=args.ha_org,
    )
    discourse = Discourse(url=args.discourse_url, api_key=args.discourse_api_key)
    sync(hello_asso, discourse, args.ha_form_slug, args.discourse_badge_slug)


if __name__ == "__main__":
    main()
