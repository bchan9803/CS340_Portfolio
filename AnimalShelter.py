# Bryan Chan
# CS 340
# Prof. Othman

from bson.objectid import ObjectId
from pymongo import MongoClient


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user, password, host, port, db, col):

        # Initialize Connection (CS340 DB) #
        # Connection Variables
        # USER = "aacuser"
        # PASS = "snhu1234"
        # HOST = "nv-desktop-services.apporto.com"
        # PORT = 32327
        # DB = "AAC"
        # COL = "animals"
          
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.col = col
        

        self.client = MongoClient('mongodb://%s:%s@%s:%d' %
                                   (self.user, self.password, self.host, self.port))
        self.database = self.client['%s' % (self.db)]
        self.collection = self.database['%s' % (self.col)]


        #self.database = self.client[self.db]
        #self.collection = self.database[self.col]

    # containsKey(self, query)
    # query: the value in which the documents in the collection will be queried by
    # return: Return True(if query contains key), otherwise return False

    def containsKey(self, query):
        try:
            # seperate key from query
            queryKey = list(query.keys()).pop()

            # if document id is passed
            if queryKey == "_id":
                return True
            else:
                False

        except:
            print("Error. Could not determine if the query contains a key.")

    # create(self, data)
    # data: document to be added to DB
    # returns: True if document successfully added,
    #           Raise exception if not successful

    def create(self, data):
        try:
            if data is not None:
                self.database.animals.insert_one(
                    data)  # data should be dictionary
                return True
        except:
            print("Nothing to save, because data parameter is empty")
            return False

    # read(self, query)
    # query: the value in which the documents in
    #        the collection will be queried by
    # returns: prints contents of queried document,
    #          empty list if no documents are found

    def read(self, query):
        try:
            if len(query) != 0:
                queryRes = []
                # # seperate val from query
                queryVal = list(query.values()).pop()
                # # store query results in a list

                # if document id is in query
                if self.containsKey(query):
                    docs = self.database.animals.find(
                        {"_id": ObjectId(queryVal)})
                # if document id is not in query
                else:
                    docs = self.database.animals.find(query)

                if docs is None:
                    print('Invalid query.')
                    return []
                else:
                    # print content of each document
                    for item in docs:
                        queryRes.append(item)
                        print(item)

                return queryRes
            # read every document in collection
            else:
                docs = self.database.animals.find({})
                queryRes = list(docs)

                # print contents of every document in collection
                #for item in docs:
                    #print(item)

                return queryRes
        except:
            print("Could not query document.")
            return False

    # update(self, query, newVal)
    # query: the query value that will be used to fetched the documents to be updated
    # newVal: new value to be updated to the document
    # returns: updates documents (returns the number of documents updated)
    #          raises exception if update unsuccessful

    def update(self, query, newVal):
        print('Documents to be updated: ')

        try:
            if query is not None:
                # if document id is in query
                if self.containsKey(query):
                    queryVal = list(query.values()).pop()
                    queryWithId = {"_id": ObjectId(queryVal)}

                    updatedDocs = self.database.animals.update_one(
                        queryWithId, newVal)
                    numOfDocsUpdated = updatedDocs.modified_count
                # if document id is not in query
                else:
                    updatedDocs = self.database.animals.update_many(
                        query, newVal)
                    numOfDocsUpdated = updatedDocs.modified_count

                print(f'{numOfDocsUpdated} documents have been updated.')
                return numOfDocsUpdated
        except:
            print('Could not update document.')
            return False

    # delete(self, query)
    # query: the query value that will be used to fetched the documents to be deleted
    # returns: deletes document (returns the number of documents deleted)
    #          raises exception if deletion unsuccessful

    def delete(self, query):
        print('Documents to be deleted: ')
        try:
            if query is not None:
                # if document id is in query
                if self.containsKey(query):
                    queryVal = list(query.values()).pop()
                    queryWithId = {"_id": ObjectId(queryVal)}

                    deletedDocs = self.database.animals.delete_one(queryWithId)
                    numOfDocsDeleted = deletedDocs.deleted_count
                # if document id is NOT in query
                else:
                    deletedDocs = self.database.animals.delete_many(query)
                    numOfDocsDeleted = deletedDocs.deleted_count

                print(f'{numOfDocsDeleted} documents have been deleted.')
                return numOfDocsDeleted
        except:
            print("Could not delete document.")
