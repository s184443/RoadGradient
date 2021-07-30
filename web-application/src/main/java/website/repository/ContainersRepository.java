package website.repository;

import website.model.Container;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ContainersRepository extends CrudRepository<Container,Long> {
	
	
}
