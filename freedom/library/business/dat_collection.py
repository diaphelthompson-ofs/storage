from pylytics.library import connection

class DatCollections():
    def __init__(self):
        self.collections_table = "collections"

    def retrieve_by_user(self, user_id):
        query = 'SELECT * from %s where user_id = %s'%(self.collections_table, user_id)

        collections = connection.run_query('storage',query)

        collection_list = []

        for collection in collections:

            label = collection[2]
            collection_id = collection[0]

            collection_dict = {
                                'label':label,
                                'collection_id':collection_id
                                }

            collection_list.append(collection_dict)

        return collection_list

class DatCollection():
    def __init__(self):
        self.collections_table = "collections"

    def add_collection(self, collection, user):

        query = 'INSERT INTO %s (label, user_id) VALUES ("%s", "%s")'%(self.collections_table,\
                 collection, str(user))

        connection.run_query('storage',query)

        return True

    def delete_collection(self, collection, user):

        query_delete_collection = 'DELETE from collections where id=%s \
        and user_id=%s'%(collection, user)

        query_set_item_collections_to_zero = 'UPDATE items set collection=0\
        where collection=%s and user_id=%s'%(collection, user)

        connection.run_query('storage',query_delete_collection)

        connection.run_query('storage',query_set_item_collections_to_zero)

        return True





