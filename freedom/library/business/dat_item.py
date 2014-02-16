import os
from freedom.library.utilities import victorinox
from pylytics.library import connection

class DatItems():
    def __init__(self):
        self.items_table = 'items'
        self.collections_table = 'collections'
        self.location_table = 'locations'

    def retrieve_items(self, user_id):
        query_items = 'SELECT * from %s where user_id = %s'%(self.items_table, user_id)
        query_collections = 'SELECT * from %s'%(self.collections_table)
        query_locations = 'SELECT * from %s'%(self.location_table)

        items = connection.run_query('storage',query_items)
        collections = connection.run_query('storage', query_collections)
        locations = connection.run_query('storage', query_locations)
        item_list = []

        for item in items:
            name = item[2]
            item_type = item[1]
            picture_location = item[3]
            item_collection = item[5]
            item_collection_label = False
            item_location = item[7]
            for collection in collections:
                collection_id = collection[0]
                collection_label = collection[2]
                if item_collection == collection_id:
                    item_collection_label = collection_label

            if item_collection_label is False:
                item_collection_label = 'No Collection'

            for location in locations:
                location_id = location[0]
                location_label = location[1]
                if item_location == location_id:
                    item_location_label = location_label
                #import pdb; pdb.set_trace()
            item_dict = {
                        'name':name, 
                        'item_type':item_type,
                        'picture_location':picture_location,
                        'collection':item_collection_label,
                        'location':item_location_label
                        }

            item_list.append(item_dict)
        return item_list

    def items_by_collection(self, items):
        items_by_collection = {}
        loose_items = []
        for item in items:
            if item['collection'] != 'No Collection':
                if item['collection'] in items_by_collection.keys():
                    items_by_collection[item['collection']].append(item)
                else:
                    items_by_collection[item['collection']] = [item]

            else:
                loose_items.append(item)

        loose_items = sorted(loose_items, key=lambda k: k['name']) 

        return loose_items, items_by_collection

    




class DatItem():

    def __init__(self):

        self.upload_folder = '/home/diaphel/mac/Documents/freedom/freedom/web_app/static/uploads'
        self.items_table = 'items'
        self.allowed_extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def upload_item(self, file, item_info, app):

        item_name = item_info.form.get('item_name')
        item_type = item_info.form.get('item_type')
        collection = item_info.form.get('collection')
        user_id = item_info.form.get('user')
        
        app.config['UPLOAD_FOLDER'] = self.upload_folder
        if file and self.allowed_file(file.filename):
            filename_org = file.filename
            filetype_finder = filename_org.split('.')

            filetype = filetype_finder[len(filetype_finder)-1]
            filename = victorinox.id_generator(15) + '.' + filetype
            newpath = self.upload_folder + str(user_id) 
            if not os.path.exists(newpath): os.makedirs(newpath)

            file.save(os.path.join(newpath, filename))


            picture_location = newpath[51:] + '/' + filename
            

            query = "INSERT INTO %s (name, type, picture_location, user_id, collection) \
                VALUES ('%s', '%s', '%s', '%s', '%s')"%(self.items_table, \
                    item_name, item_type, picture_location, str(user_id), collection)

            connection.run_query('storage',query)


    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.allowed_extensions

