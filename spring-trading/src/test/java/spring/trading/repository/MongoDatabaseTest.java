package spring.trading.repository;

import com.mongodb.*;
import com.mongodb.client.*;
import com.mongodb.client.model.Filters;
import com.mongodb.client.result.InsertOneResult;
import org.bson.Document;
import org.bson.conversions.Bson;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;


public class MongoDatabaseTest {

    private MongoClient mongoClient;
    private MongoDatabase database;
    @BeforeEach
    public void setUp() {
        String uri = "mongodb://admin:password123@localhost:27017/test?authSource=admin";
        mongoClient = MongoClients.create(uri);
        database = mongoClient.getDatabase("test");


    }
    @Test
    public void ConnectTestandMakeDatabase(){


        MongoDatabase database = mongoClient.getDatabase("test");
        database.createCollection("exampleCollection");

    }

    @Test
    public void getAllCollection(){

        for (String name : database.listCollectionNames()) {
            System.out.println(name);
        }
    }

    @Test
    public void getCollection(){
        MongoDatabase database = mongoClient.getDatabase("test");
        MongoCollection<Document> collection = database.getCollection("exampleCollection");
        System.out.println("getCollection success");
    }

    @Test
    public void InsertDocument(){
        MongoDatabase database = mongoClient.getDatabase("test");
        MongoCollection<Document> collection = database.getCollection("exampleCollection");

        Document doc1 = new Document("color", "black").append("qty", 10).append("shape", "heart");
        InsertOneResult result = collection.insertOne(doc1);
        System.out.println("Inserted a document with the following id: "
                + result.getInsertedId().asObjectId().getValue());
    }

    @Test
    public void deleteOneDocument(){
        MongoCollection<Document> collection = database.getCollection("exampleCollection");
        String result = collection.deleteOne(Filters.eq("color", "black")).toString();
        System.out.println(result);
    }

    @Test
    public void deleteManyDocuments(){
        MongoCollection<Document> collection = database.getCollection("exampleCollection");
        String result = collection.deleteMany(Filters.empty()).toString();
        System.out.println(result);
    }

    @Test
    public void getAlldocument(){
        MongoCollection<Document> collection = database.getCollection("exampleCollection");
        Bson filter= Filters.empty();
        collection.find(filter).forEach(doc-> System.out.println(doc.toJson()));

    }
}

