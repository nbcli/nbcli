import pkgutil
import sys
from .core import get_session, add_detail_endpoints
import requests
import pynetbox

def main():

    netbox = get_session()

    add_detail_endpoints()

    apps = ['Circuits',
            'DCIM',
            'Extras',
            'IPAM',
            'Secrets',
            'Tenancy',
            'Virtualization']
    
    ns = dict(Netbox=netbox)
    nbvars = dict(Netbox=dict())
    
    for app in apps:
        nbvars['Netbox'][app] = list()
        appobj = getattr(netbox, app.lower())
        ns[app] = appobj
        for endpoint in requests.get(netbox.base_url+'/'+app.lower(), verify=False).json().keys():
            if endpoint[0] != '_':
                endpointname = endpoint.title().replace('-', '')
                endpointobj = getattr(appobj, endpoint.replace('-', '_'))
                if app == 'Virtualization' and endpoint == "interfaces":
                    endpointname = 'VirtualInterfaces'
                nbvars['Netbox'][app].append(endpointname)
                ns[endpointname] = endpointobj
    
    ns['nbvars'] = nbvars
    
    def lsnb():
        for api in nbvars.keys():
            print(api + ':')
            for app in nbvars[api].keys():
                print('  ' + app + ":")
                for ep in nbvars[api][app]:
                    print('    ' + ep)
    
    ns['lsnb'] = lsnb
    
    banner = ''
    banner += 'NetBox version {}\n'.format(netbox.version)
    banner += 'pynetbox version {}\n'.format(pynetbox.__version__)
    banner += 'Run lsnb() to view available pynetbox objects.\n'
    
    if pkgutil.find_loader('IPython'):
        from IPython import start_ipython
        from traitlets.config.loader import Config

        c = Config()
        c.TerminalInteractiveShell.banner2 = banner

        start_ipython(argv=[], user_ns=ns, config=c)
    else:
        banner = '\nPython version {}\n'.format(sys.version) + banner
        from code import interact
        interact(banner=banner, local=ns)

if __name__ == '__main__':
    main()
