#!/usr/bin/env python3
import argparse
import logging
from ldap3 import Server, Connection, ALL, NTLM, KERBEROS, SUBTREE
from ldap3.core.exceptions import LDAPSocketOpenError, LDAPBindError, LDAPObjectClassError
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def base_creator(domain):
    return ','.join([f"DC={part}" for part in domain.split('.')])

def setup_logging(debug=False):
    logging_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection(server_address, user, password, use_ssl=False, auth_method=NTLM, ccache_file=None, verbose=False):
    try:
        # Use LDAPS (port 636) if use_ssl=True
        server = Server(server_address, get_info=ALL, use_ssl=use_ssl)
        if auth_method == KERBEROS and ccache_file:
            if verbose:
                console.log(f"[yellow][D][/yellow] Using Kerberos with ccache file: {ccache_file}")
            conn = Connection(server, authentication=KERBEROS, sasl_mechanism='GSSAPI', sasl_credentials=(None, None, ccache_file))
        else:
            conn = Connection(server, user=user, password=password, authentication=auth_method, auto_bind=True)

        if verbose:
            console.log(f"[green][+][/green] Connected to {server_address} with {auth_method}")
        return conn
    except LDAPSocketOpenError:
        if verbose:
            console.log(f"[bold red][-][/bold red] Could not connect to {server_address}")
        return None
    except LDAPBindError as e:
        if verbose:
            console.log(f"[bold red][-][/bold red] Failed to bind to {server_address}: {str(e)}")
        return None

class ADSiloManager:
    def __init__(self, username, password, domain, dc_ip=None, kerberos=False, ccache_file=None, verbose=False):
        self.username = f'{domain}\\{username}' if not kerberos else None
        self.password = password
        self.server_address_ldap = f'{dc_ip}:389' if dc_ip else f'{domain}:389'
        self.server_address_ldaps = f'{dc_ip}:636' if dc_ip else f'{domain}:636'
        self.domain = domain
        self.kerberos = kerberos
        self.ccache_file = ccache_file
        self.verbose = verbose
        self.connection = None

    def create_connection(self):
        """Tries to connect via LDAP, then LDAPS if it fails."""
        self.connection = create_connection(self.server_address_ldap, self.username, self.password, auth_method=KERBEROS if self.kerberos else NTLM, ccache_file=self.ccache_file, verbose=self.verbose)
        if not self.connection:
            console.log(f"[bold red][-][/bold red] Trying LDAPS...")
            self.connection = create_connection(self.server_address_ldaps, self.username, self.password, use_ssl=True, auth_method=KERBEROS if self.kerberos else NTLM, ccache_file=self.ccache_file, verbose=self.verbose)

        if not self.connection:
            console.log(f"[bold red][-][/bold red] Both LDAP and LDAPS connection attempts failed.")
            return False
        return True

    def extract_cn(self, dn):
        """Extracts the CN (common name) from a DN."""
        parts = dn.split(',')
        for part in parts:
            if part.startswith('CN='):
                return part[3:]  # Returns the part after "CN="
        return dn  # If no CN is found, returns the full DN (to avoid errors)

    def list_silos_and_members(self):
        """Lists the users and computers associated with silos, displaying only the names."""
        try:
            # Search for authentication silos
            base_dn = f"CN=AuthN Policy Configuration,CN=Services,CN=Configuration,{base_creator(self.domain)}"
            search_filter = "(objectClass=msDS-AuthNPolicySilo)"
            self.connection.search(base_dn, search_filter, SUBTREE, attributes=["cn", "msDS-AuthNPolicySiloMembers", "msDS-AuthNPolicySiloMembersBL"])

            if not self.connection.entries:
                console.log("[bold yellow]No authentication silos found.[/bold yellow]")
                return

            # Display users
            user_table = Table(title="Users - SILOS", box=box.ROUNDED)
            user_table.add_column("Users", style="green", no_wrap=True)
            user_table.add_column("SILO", style="cyan")

            # Display computers
            computer_table = Table(title="Computers - SILOS", box=box.ROUNDED)
            computer_table.add_column("Computers", style="green", no_wrap=True)
            computer_table.add_column("SILO", style="cyan")

            for entry in self.connection.entries:
                silo_name = entry.cn.value
                users, computers = [], []

                # List users and computers associated with the silo
                if 'msDS-AuthNPolicySiloMembers' in entry:
                    for member_dn in entry['msDS-AuthNPolicySiloMembers']:
                        # Get the object class of each member
                        object_class = self.get_object_class(member_dn)
                        member_name = self.extract_cn(member_dn)

                        if object_class == 'computer':
                            computers.append(member_name)
                        elif object_class == 'user':
                            users.append(member_name)

                # Add users to the table
                if users:
                    for user in users:
                        user_table.add_row(user, silo_name)
                else:
                    user_table.add_row("No users found", silo_name)

                # Add computers to the table
                if computers:
                    for computer in computers:
                        computer_table.add_row(computer, silo_name)
                else:
                    computer_table.add_row("No computers found", silo_name)

            console.print(user_table)
            console.print(computer_table)

        except LDAPObjectClassError as e:
            console.log(f"[bold red]Error: {e}. The domain functional level might be too old.[/bold red]")
        except Exception as e:
            console.log(f"[bold red]Error retrieving silos and members: {e}[/bold red]")

    def get_object_class(self, member_dn):
        """Retrieves the object class (user, computer, etc.) of an entry in AD."""
        try:
            self.connection.search(member_dn, "(objectClass=*)", SUBTREE, attributes=["objectClass"])
            if self.connection.entries:
                entry = self.connection.entries[0]
                object_classes = entry.objectClass
                if 'computer' in object_classes:
                    return 'computer'
                elif 'user' in object_classes:
                    return 'user'
        except Exception as e:
            console.log(f"[bold red]Error retrieving object class for {member_dn}: {e}[/bold red]")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Script to query authentication silos in Active Directory and list associated members."
    )
    parser.add_argument('-u', '--username', required=True, help="Active Directory username")
    parser.add_argument('-p', '--password', required=True, help="Active Directory password")
    parser.add_argument('-d', '--domain', required=True, help="Active Directory domain")
    parser.add_argument('--dc-host', required=True, help="Domain controller hostname or IP address")
    parser.add_argument('--kerberos', action='store_true', help='Use Kerberos authentication')
    parser.add_argument('--ccache', help='Path to Kerberos ccache file')
    parser.add_argument('-v', '--debug', action='store_true', help='Enable debug logging for more details')

    args = parser.parse_args()

    # Setup logging based on the debug option
    setup_logging(args.debug)

    # Create the AD silo manager instance
    manager = ADSiloManager(args.username, args.password, args.domain, args.dc_host, kerberos=args.kerberos, ccache_file=args.ccache, verbose=args.debug)

    # Attempt connection
    if manager.create_connection():
        # List silos and associated users/computers
        manager.list_silos_and_members()
    else:
        console.log("[bold red]Failed to connect via LDAP/LDAPS.[/bold red]")
if __name__ == "__main__":
    main()
