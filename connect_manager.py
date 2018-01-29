import urllib3
import json
from re import search

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def url_join(*args):

    return '/'.join(x.strip('/') for x in args)


class HiveApi(object):
    """ Connect to the different Hive nodes accross a cluster and 
    monitor/interact with the nodes and the node guests. Only one instance
    of this class can exist at a time
    """
    
    singleton = None
    username = "admin"
    password = "admin"
    realm = "local"

    pool_manager = urllib3.PoolManager

    @classmethod
    def get_token(cls, node):
        """connect to a node in the cluster

        return: instance of class that can be used to 
        """
        node = url_join(node, 'auth')

        assert(search(".+/api/auth/?$", node))

        http = cls.pool_manager()

        response = http.request('POST', node, fields={
            'username': cls.username, 'password': cls.password, 'realm': cls.realm
        })
        assert(response.decode_content is True)

        response = json.loads(response.data)

        if "token" not in response:
            return None
        http.clear()

        return response['token']

    @classmethod
    def guest_inventory_get(cls, node):
        token = cls.get_token(node)

        node = url_join(node, 'guests')

        http = cls.pool_manager()
        response = http.request('GET', node)

        assert(response.decode_content is True)
        http.clear()
        return json.loads(response.data)

    @classmethod
    def guest_names_get(cls, node):

        guests = cls.guest_inventory_get(node)
        
        return [guest['name'] for guest in guests]


    @classmethod
    def guest_get_by_name(cls, node, name):

        node = url_join(node, 'guest', name)
        http = cls.pool_manager()
        response = http.request('GET', node)
 
        assert(response.decode_content is True)

        return json.loads(response.data)
        

