package spring.trading.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import spring.trading.domain.Request;

public interface RequestRepository extends MongoRepository<Request,String> {
}
